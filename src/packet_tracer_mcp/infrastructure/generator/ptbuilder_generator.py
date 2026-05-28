"""
Generador de scripts PTBuilder.

Convierte un TopologyPlan validado en JavaScript compatible
con la extensión PTBuilder de Packet Tracer.
"""

from __future__ import annotations
import json
from ...domain.models.plans import TopologyPlan


def generate_ptbuilder_script(plan: TopologyPlan) -> str:
    """Genera un script JS de PTBuilder a partir de un plan validado."""
    lines: list[str] = []

    for dev in plan.devices:
        lines.append(f'addDevice("{dev.name}", "{dev.model}", {dev.x}, {dev.y});')

    for mod in plan.modules:
        lines.append(f'addModule("{mod.device}", "{mod.slot}", "{mod.module}");')

    for link in plan.links:
        lines.append(
            f'addLink("{link.device_a}", "{link.port_a}", '
            f'"{link.device_b}", "{link.port_b}", "{link.cable}");'
        )

    return "\n".join(lines)


def generate_executable_script(plan: TopologyPlan) -> str:
    """
    Genera script JS completo y ejecutable line-by-line:
    - Dispositivos y enlaces via PTBuilder (addDevice/addLink)
    - IPs de routers via IPC directo (getPort().setIpSubnetMask() + setPower(true))
    - Protocolos de routing via enterCommand uno por línea (confiable con sleep entre calls)
    - PCs via configurePcIp()

    Cada línea se envía como un POST separado al bridge con ~1s de delay entre ellas.
    """
    from ...shared.utils import prefix_to_mask

    lines: list[str] = []
    lines.append(generate_ptbuilder_script(plan))

    # --- Routers: IPs via IPC directo + routing protocols via enterCommand ---
    routers = [d for d in plan.devices if d.category == "router"]
    for router in routers:
        name = json.dumps(router.name)

        # Interfaces: IPC directo (no usa CLI, no tiene problemas de modo)
        for iface, ip_cidr in router.interfaces.items():
            ip, prefix = ip_cidr.split("/")
            mask = prefix_to_mask(int(prefix))
            port_name = json.dumps(iface)
            ip_js = json.dumps(ip)
            mask_js = json.dumps(mask)
            lines.append(
                f'(function(){{ var p=ipc.network().getDevice({name}).getPort({port_name});'
                f' if(p){{ p.setIpSubnetMask({ip_js},{mask_js}); p.setPower(true); }} }})();'
            )

        # Hostname + no ip domain-lookup via enterCommand
        lines.append(f'ipc.network().getDevice({name}).getCommandLine().enterCommand("enable");')
        lines.append(f'ipc.network().getDevice({name}).getCommandLine().enterCommand("conf t");')
        lines.append(f'ipc.network().getDevice({name}).getCommandLine().enterCommand("hostname {router.name}");')
        lines.append(f'ipc.network().getDevice({name}).getCommandLine().enterCommand("no ip domain-lookup");')

        # RIP
        for rip in plan.rip_configs:
            if rip.router != router.name:
                continue
            lines.append(f'ipc.network().getDevice({name}).getCommandLine().enterCommand("router rip");')
            lines.append(f'ipc.network().getDevice({name}).getCommandLine().enterCommand("version {rip.version}");')
            for net in rip.networks:
                lines.append(f'ipc.network().getDevice({name}).getCommandLine().enterCommand("network {net}");')
            if rip.no_auto_summary:
                lines.append(f'ipc.network().getDevice({name}).getCommandLine().enterCommand("no auto-summary");')
            lines.append(f'ipc.network().getDevice({name}).getCommandLine().enterCommand("exit");')

        # OSPF
        for ospf in plan.ospf_configs:
            if ospf.router != router.name:
                continue
            lines.append(f'ipc.network().getDevice({name}).getCommandLine().enterCommand("router ospf {ospf.process_id}");')
            if ospf.router_id:
                lines.append(f'ipc.network().getDevice({name}).getCommandLine().enterCommand("router-id {ospf.router_id}");')
            for net in ospf.networks:
                net_addr = net['network']
                wildcard = net['wildcard']
                area = net['area']
                lines.append(
                    f'ipc.network().getDevice({name}).getCommandLine().enterCommand('
                    f'"network {net_addr} {wildcard} area {area}");'
                )
            lines.append(f'ipc.network().getDevice({name}).getCommandLine().enterCommand("exit");')

        # EIGRP
        for eigrp in plan.eigrp_configs:
            if eigrp.router != router.name:
                continue
            lines.append(f'ipc.network().getDevice({name}).getCommandLine().enterCommand("router eigrp {eigrp.as_number}");')
            for net in eigrp.networks:
                net_addr = net['network']
                wildcard = net['wildcard']
                lines.append(
                    f'ipc.network().getDevice({name}).getCommandLine().enterCommand('
                    f'"network {net_addr} {wildcard}");'
                )
            if eigrp.no_auto_summary:
                lines.append(f'ipc.network().getDevice({name}).getCommandLine().enterCommand("no auto-summary");')
            lines.append(f'ipc.network().getDevice({name}).getCommandLine().enterCommand("exit");')

        # Rutas estáticas
        for route in plan.static_routes:
            if route.router != router.name:
                continue
            cmd = f"ip route {route.destination} {route.mask} {route.next_hop}"
            if route.admin_distance != 1:
                cmd += f" {route.admin_distance}"
            lines.append(f'ipc.network().getDevice({name}).getCommandLine().enterCommand("{cmd}");')

        lines.append(f'ipc.network().getDevice({name}).getCommandLine().enterCommand("end");')

    # --- PCs / Servers / Laptops: configurePcIp (ya confiable) ---
    pcs = [d for d in plan.devices if d.category in ("pc", "server", "laptop")]
    for pc in pcs:
        if pc.interfaces:
            iface_ip = next(iter(pc.interfaces.values()), None)
            if iface_ip:
                ip, prefix = iface_ip.split("/")
                mask = prefix_to_mask(int(prefix))
                gw = pc.gateway or ""
                if plan.dhcp_pools:
                    lines.append(f'configurePcIp({json.dumps(pc.name)}, true);')
                else:
                    lines.append(
                        f'configurePcIp({json.dumps(pc.name)}, false, '
                        f'{json.dumps(ip)}, {json.dumps(mask)}, {json.dumps(gw)});'
                    )

    return "\n".join(lines)


def generate_full_script(plan: TopologyPlan) -> str:
    """
    Genera el script completo: PTBuilder + bloque de configuración CLI
    como comentarios (para referencia visual).
    """
    from .cli_config_generator import generate_all_configs

    parts: list[str] = []
    parts.append(generate_ptbuilder_script(plan))

    configs = generate_all_configs(plan)
    if configs:
        parts.append("/* === Configuraciones CLI por dispositivo ===")
        parts.append("Copiar y pegar en la CLI de cada dispositivo. */")
        for device_name, cli_block in configs.items():
            parts.append(f"/* --- {device_name} ---")
            for line in cli_block.splitlines():
                parts.append(line)
            parts.append("*/ ")

    return "\n".join(parts)
