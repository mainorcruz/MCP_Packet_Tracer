"""
Catálogo de dispositivos de Packet Tracer.

Puertos verificados contra PT 8.x en vivo — NO incluimos Vlan1
porque no se usa para cableado físico (es SVI).
"""

from __future__ import annotations
from dataclasses import dataclass

from ...shared.enums import PortSpeed


@dataclass(frozen=True)
class PortSpec:
    """Especificación de un puerto físico."""
    speed: str
    slot: str
    full_name: str = ""

    def __post_init__(self):
        if not self.full_name:
            speed_str = self.speed.value if hasattr(self.speed, "value") else self.speed
            object.__setattr__(self, "full_name", f"{speed_str}{self.slot}")


@dataclass(frozen=True)
class DeviceModel:
    """Modelo de dispositivo de Packet Tracer."""
    pt_type: str
    category: str
    ports: tuple[PortSpec, ...]
    display_name: str = ""


def _gig(slot: str) -> PortSpec:
    return PortSpec(PortSpeed.GIGABIT_ETHERNET, slot)

def _fast(slot: str) -> PortSpec:
    return PortSpec(PortSpeed.FAST_ETHERNET, slot)

def _serial(slot: str) -> PortSpec:
    return PortSpec(PortSpeed.SERIAL, slot)


# --- ROUTERS (verified — no serial ports without HWIC modules) ---
ROUTER_1841 = DeviceModel(
    pt_type="1841", category="router", display_name="Cisco 1841",
    ports=(_fast("0/0"), _fast("0/1")),
)
ROUTER_1941 = DeviceModel(
    pt_type="1941", category="router", display_name="Cisco 1941",
    ports=(_gig("0/0"), _gig("0/1")),
)
ROUTER_2811 = DeviceModel(
    pt_type="2811", category="router", display_name="Cisco 2811",
    ports=(_fast("0/0"), _fast("0/1")),
)
ROUTER_2901 = DeviceModel(
    pt_type="2901", category="router", display_name="Cisco 2901",
    ports=(_gig("0/0"), _gig("0/1")),
)
ROUTER_2911 = DeviceModel(
    pt_type="2911", category="router", display_name="Cisco 2911",
    ports=(_gig("0/0"), _gig("0/1"), _gig("0/2")),
)
ROUTER_4321 = DeviceModel(
    pt_type="ISR4321", category="router", display_name="Cisco ISR 4321",
    ports=(_gig("0/0/0"), _gig("0/0/1")),
)
ROUTER_4331 = DeviceModel(
    pt_type="ISR4331", category="router", display_name="Cisco ISR 4331",
    ports=(_gig("0/0/0"), _gig("0/0/1"), _gig("0/0/2")),
)
ROUTER_PT = DeviceModel(
    pt_type="Router-PT", category="router", display_name="Generic Router",
    ports=(_fast("0/0"), _fast("0/1")),
)

# --- SWITCHES L2 ---
def _switch_2950_ports() -> tuple[PortSpec, ...]:
    return tuple(_fast(f"0/{i}") for i in range(1, 25))

def _switch_2950T_ports() -> tuple[PortSpec, ...]:
    fast = tuple(_fast(f"0/{i}") for i in range(1, 25))
    gig = (_gig("0/1"), _gig("0/2"))
    return fast + gig

def _switch_2960_ports() -> tuple[PortSpec, ...]:
    fast = tuple(_fast(f"0/{i}") for i in range(1, 25))
    gig = (_gig("0/1"), _gig("0/2"))
    return fast + gig

SWITCH_2950 = DeviceModel(
    pt_type="2950-24", category="switch", display_name="Cisco 2950-24",
    ports=_switch_2950_ports(),
)
SWITCH_2950T = DeviceModel(
    pt_type="2950T-24", category="switch", display_name="Cisco 2950T-24",
    ports=_switch_2950T_ports(),
)
SWITCH_2960 = DeviceModel(
    pt_type="2960-24TT", category="switch", display_name="Cisco 2960-24TT",
    ports=_switch_2960_ports(),
)
SWITCH_PT = DeviceModel(
    pt_type="Switch-PT", category="switch", display_name="Generic Switch",
    ports=tuple(_fast(f"0/{i}") for i in range(1, 9)),
)

# --- SWITCHES L3 ---
def _switch_3560_ports() -> tuple[PortSpec, ...]:
    fast = tuple(_fast(f"0/{i}") for i in range(1, 25))
    gig = (_gig("0/1"), _gig("0/2"))
    return fast + gig

def _switch_3650_ports() -> tuple[PortSpec, ...]:
    fast = tuple(_fast(f"0/{i}") for i in range(1, 25))
    gig = (_gig("0/1"), _gig("0/2"))
    return fast + gig

SWITCH_3560 = DeviceModel(
    pt_type="3560-24PS", category="switch", display_name="Cisco 3560-24PS",
    ports=_switch_3560_ports(),
)
SWITCH_3650 = DeviceModel(
    pt_type="3650-24PS", category="switch", display_name="Cisco 3650-24PS",
    ports=_switch_3650_ports(),
)

# --- END DEVICES (verified) ---
PC_PT = DeviceModel(pt_type="PC-PT", category="pc", display_name="PC", ports=(_fast("0"),))
SERVER_PT = DeviceModel(pt_type="Server-PT", category="server", display_name="Server", ports=(_fast("0"),))
LAPTOP_PT = DeviceModel(pt_type="Laptop-PT", category="laptop", display_name="Laptop", ports=(_fast("0"),))
TABLET_PT = DeviceModel(pt_type="TabletPC-PT", category="pc", display_name="Tablet PC", ports=(_fast("0"),))
SMARTPHONE_PT = DeviceModel(pt_type="SMARTPHONE-PT", category="pc", display_name="Smartphone", ports=(_fast("0"),))
PRINTER_PT = DeviceModel(pt_type="Printer-PT", category="pc", display_name="Printer", ports=(_fast("0"),))

# --- CLOUD / WAN (verified: Ethernet6 is the usable Ethernet port) ---
CLOUD_PT = DeviceModel(
    pt_type="Cloud-PT", category="cloud", display_name="Cloud",
    ports=(PortSpec(PortSpeed.FAST_ETHERNET, "6", full_name="Ethernet6"),),
)

# --- ACCESS POINTS (verified: Port 0) ---
AP_PT = DeviceModel(
    pt_type="AccessPoint-PT", category="accesspoint", display_name="Access Point",
    ports=(PortSpec(PortSpeed.FAST_ETHERNET, "0", full_name="Port 0"),),
)
AP_PT_N = DeviceModel(
    pt_type="AccessPoint-PT-N", category="accesspoint", display_name="Access Point-N",
    ports=(PortSpec(PortSpeed.FAST_ETHERNET, "0", full_name="Port 0"),),
)
AP_PT_AC = DeviceModel(
    pt_type="AccessPoint-PT-AC", category="accesspoint", display_name="Access Point-AC",
    ports=(PortSpec(PortSpeed.FAST_ETHERNET, "0", full_name="Port 0"),),
)
LAP_PT = DeviceModel(
    pt_type="LAP-PT", category="accesspoint", display_name="Lightweight AP",
    ports=(PortSpec(PortSpeed.FAST_ETHERNET, "0", full_name="Port 0"),),
)

# --- HUB ---
HUB_PT = DeviceModel(
    pt_type="Hub-PT", category="hub", display_name="Hub",
    ports=tuple(PortSpec(PortSpeed.FAST_ETHERNET, str(i), full_name=f"Port {i}") for i in range(8)),
)

# --- FIREWALLS (Cisco ASA) ---
ASA_5505 = DeviceModel(
    pt_type="5505", category="firewall", display_name="Cisco ASA 5505",
    ports=tuple(_fast(f"0/{i}") for i in range(8)),
)
ASA_5506 = DeviceModel(
    pt_type="5506-X", category="firewall", display_name="Cisco ASA 5506-X",
    ports=tuple(_gig(f"1/{i}") for i in range(8)),
)

# --- WIRELESS LAN CONTROLLER ---
WLC_PT = DeviceModel(
    pt_type="WLC-PT", category="wlc", display_name="Wireless LAN Controller",
    ports=tuple(_gig(str(i)) for i in range(1, 9)),
)
WLC_2504 = DeviceModel(
    pt_type="WLC-2504", category="wlc", display_name="Cisco WLC 2504",
    ports=tuple(_gig(str(i)) for i in range(1, 5)),
)
WLC_3504 = DeviceModel(
    pt_type="WLC-3504", category="wlc", display_name="Cisco WLC 3504",
    ports=tuple(_gig(str(i)) for i in range(1, 5)),
)

# --- DSL / CABLE MODEMS ---
DSL_MODEM_PT = DeviceModel(
    pt_type="DSL-Modem-PT", category="modem", display_name="DSL Modem",
    ports=(
        PortSpec(PortSpeed.FAST_ETHERNET, "0", full_name="Ethernet0"),
        PortSpec(PortSpeed.FAST_ETHERNET, "1", full_name="Coaxial0"),
    ),
)
CABLE_MODEM_PT = DeviceModel(
    pt_type="Cable-Modem-PT", category="modem", display_name="Cable Modem",
    ports=(
        PortSpec(PortSpeed.FAST_ETHERNET, "0", full_name="Ethernet0"),
        PortSpec(PortSpeed.FAST_ETHERNET, "1", full_name="Coaxial0"),
    ),
)


# --- CATÁLOGO INDEXADO ---
ALL_MODELS: dict[str, DeviceModel] = {
    m.pt_type: m for m in [
        # Routers
        ROUTER_1841, ROUTER_1941, ROUTER_2811, ROUTER_2901, ROUTER_2911,
        ROUTER_4321, ROUTER_4331, ROUTER_PT,
        # Switches L2
        SWITCH_2950, SWITCH_2950T, SWITCH_2960, SWITCH_PT,
        # Switches L3
        SWITCH_3560, SWITCH_3650,
        # End devices
        PC_PT, SERVER_PT, LAPTOP_PT, TABLET_PT, SMARTPHONE_PT, PRINTER_PT,
        # Cloud / WAN
        CLOUD_PT,
        # Access Points
        AP_PT, AP_PT_N, AP_PT_AC, LAP_PT,
        # Hub
        HUB_PT,
        # Firewalls
        ASA_5505, ASA_5506,
        # WLC
        WLC_PT, WLC_2504, WLC_3504,
        # Modems
        DSL_MODEM_PT, CABLE_MODEM_PT,
    ]
}


def resolve_model(name: str) -> DeviceModel | None:
    """Resuelve un nombre/alias a un DeviceModel."""
    from .aliases import MODEL_ALIASES
    key = MODEL_ALIASES.get(name.lower(), name)
    return ALL_MODELS.get(key)


def get_ports_by_speed(model: DeviceModel, speed: str) -> list[PortSpec]:
    """Devuelve los puertos de un modelo filtrados por velocidad."""
    return [p for p in model.ports if p.speed == speed]


def get_valid_ports(model_name: str) -> set[str]:
    """Devuelve el set de nombres de puertos válidos para un modelo."""
    model = resolve_model(model_name)
    if not model:
        return set()
    return {p.full_name for p in model.ports}
