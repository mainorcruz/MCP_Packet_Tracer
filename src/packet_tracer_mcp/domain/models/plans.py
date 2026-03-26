"""Modelos de plan — el resultado validado y completo."""

from __future__ import annotations
from pydantic import BaseModel, Field

from ...shared.enums import DeviceRole


class DevicePlan(BaseModel):
    """Un dispositivo concreto en el plan."""
    name: str
    model: str
    category: str
    role: DeviceRole = DeviceRole.END_HOST
    x: int = 0
    y: int = 0
    interfaces: dict[str, str] = Field(default_factory=dict)
    gateway: str = ""


class LinkPlan(BaseModel):
    """Un enlace entre dos dispositivos."""
    device_a: str
    port_a: str
    device_b: str
    port_b: str
    cable: str = "straight"


class ModulePlan(BaseModel):
    """Un módulo de expansión a instalar en un dispositivo."""
    device: str
    slot: int
    module: str  # e.g. "HWIC-2T", "NIM-2T"


class DHCPPool(BaseModel):
    """Un pool DHCP en un router."""
    router: str
    pool_name: str
    network: str
    mask: str
    gateway: str
    dns: str = "8.8.8.8"
    excluded_start: str = ""
    excluded_end: str = ""


class StaticRoute(BaseModel):
    """Una ruta estática. admin_distance > 1 la convierte en ruta flotante."""
    router: str
    destination: str
    mask: str
    next_hop: str
    admin_distance: int = 1


class OSPFConfig(BaseModel):
    """Configuración OSPF para un router."""
    router: str
    process_id: int = 1
    router_id: str = ""
    networks: list[dict] = Field(default_factory=list)


class RIPConfig(BaseModel):
    """Configuración RIP v2 para un router."""
    router: str
    version: int = 2
    networks: list[str] = Field(default_factory=list)
    no_auto_summary: bool = True


class EIGRPConfig(BaseModel):
    """Configuración EIGRP para un router."""
    router: str
    as_number: int = 100
    networks: list[dict] = Field(default_factory=list)  # [{network, wildcard}]
    no_auto_summary: bool = True


class ValidationCheck(BaseModel):
    """Una verificación a ejecutar post-deploy."""
    check_type: str
    from_device: str
    to_target: str = ""
    expected: str = ""


class TopologyPlan(BaseModel):
    """Plan completo, validado, listo para generar scripts."""
    name: str = "topology"
    devices: list[DevicePlan] = Field(default_factory=list)
    modules: list[ModulePlan] = Field(default_factory=list)
    links: list[LinkPlan] = Field(default_factory=list)
    dhcp_pools: list[DHCPPool] = Field(default_factory=list)
    static_routes: list[StaticRoute] = Field(default_factory=list)
    ospf_configs: list[OSPFConfig] = Field(default_factory=list)
    rip_configs: list[RIPConfig] = Field(default_factory=list)
    eigrp_configs: list[EIGRPConfig] = Field(default_factory=list)
    validations: list[ValidationCheck] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def device_by_name(self, name: str) -> DevicePlan | None:
        for d in self.devices:
            if d.name == name:
                return d
        return None

    def devices_by_category(self, category: str) -> list[DevicePlan]:
        return [d for d in self.devices if d.category == category]
