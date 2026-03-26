"""
Catálogo de módulos de expansión para Packet Tracer.

Los módulos se instalan en slots de dispositivos para agregar puertos
adicionales (serial, ethernet, wireless, etc.)

Cada módulo tiene un tipo numérico que PTBuilder usa internamente,
y uno o más puertos que agrega al dispositivo.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class ModuleSpec:
    """Especificación de un módulo de expansión."""
    name: str           # Nombre del módulo (e.g. "HWIC-2T")
    module_type: int    # Tipo numérico de PT
    category: str       # router_nm, router_wic, switch_nm, etc.
    ports_added: tuple[str, ...]  # Puertos que agrega (e.g. ("Serial0/0/0", "Serial0/0/1"))
    description: str = ""
    compatible_with: tuple[str, ...] = ()  # pt_types compatibles (vacío = genérico)


# --- Router NM Modules (slot 0) ---
NM_1FE_TX = ModuleSpec(
    name="NM-1FE-TX", module_type=1, category="router_nm",
    ports_added=("FastEthernet1/0",),
    description="1-port FastEthernet (copper)",
)
NM_2FE2W = ModuleSpec(
    name="NM-2FE2W", module_type=1, category="router_nm",
    ports_added=("FastEthernet1/0", "FastEthernet1/1"),
    description="2-port FastEthernet + 2 WIC slots",
)
NM_4A_S = ModuleSpec(
    name="NM-4A/S", module_type=1, category="router_nm",
    ports_added=("Serial1/0", "Serial1/1", "Serial1/2", "Serial1/3"),
    description="4-port Async/Sync Serial",
)
NM_ESW_161 = ModuleSpec(
    name="NM-ESW-161", module_type=1, category="router_nm",
    ports_added=tuple(f"FastEthernet1/{i}" for i in range(16)),
    description="16-port Ethernet Switch module",
)

# --- Router HWIC/WIC Modules (slots 0, 1) ---
HWIC_2T = ModuleSpec(
    name="HWIC-2T", module_type=2, category="router_hwic",
    ports_added=("Serial0/0/0", "Serial0/0/1"),
    description="2-port Serial WAN Interface Card",
    compatible_with=("1941", "2901", "2911"),
)
HWIC_4ESW = ModuleSpec(
    name="HWIC-4ESW", module_type=2, category="router_hwic",
    ports_added=("FastEthernet0/1/0", "FastEthernet0/1/1", "FastEthernet0/1/2", "FastEthernet0/1/3"),
    description="4-port Ethernet Switch HWIC",
    compatible_with=("1941", "2901", "2911"),
)
HWIC_1GE_SFP = ModuleSpec(
    name="HWIC-1GE-SFP", module_type=2, category="router_hwic",
    ports_added=("GigabitEthernet0/0/0",),
    description="1-port GigabitEthernet SFP",
    compatible_with=("1941", "2901", "2911"),
)
HWIC_AP_AG_B = ModuleSpec(
    name="HWIC-AP-AG-B", module_type=2, category="router_hwic",
    ports_added=(),
    description="Integrated Wireless AP",
    compatible_with=("1941", "2901", "2911"),
)
HWIC_8A = ModuleSpec(
    name="HWIC-8A", module_type=2, category="router_hwic",
    ports_added=tuple(f"Async0/0/{i}" for i in range(8)),
    description="8-port Async Serial",
    compatible_with=("1941", "2901", "2911"),
)
WIC_1T = ModuleSpec(
    name="WIC-1T", module_type=2, category="router_wic",
    ports_added=("Serial0/0/0",),
    description="1-port Serial WAN Interface Card",
)
WIC_2T = ModuleSpec(
    name="WIC-2T", module_type=2, category="router_wic",
    ports_added=("Serial0/0/0", "Serial0/0/1"),
    description="2-port Serial WAN Interface Card",
)

# --- ISR NIM Modules ---
NIM_2T = ModuleSpec(
    name="NIM-2T", module_type=2, category="router_nim",
    ports_added=("Serial0/1/0", "Serial0/1/1"),
    description="2-port Serial NIM for ISR 4000",
    compatible_with=("ISR4321", "ISR4331"),
)
NIM_ES2_4 = ModuleSpec(
    name="NIM-ES2-4", module_type=2, category="router_nim",
    ports_added=("GigabitEthernet0/1/0", "GigabitEthernet0/1/1",
                 "GigabitEthernet0/1/2", "GigabitEthernet0/1/3"),
    description="4-port GE Layer 2 NIM for ISR 4000",
    compatible_with=("ISR4321", "ISR4331"),
)


# --- Catálogo indexado ---
ALL_MODULES: dict[str, ModuleSpec] = {
    m.name: m for m in [
        NM_1FE_TX, NM_2FE2W, NM_4A_S, NM_ESW_161,
        HWIC_2T, HWIC_4ESW, HWIC_1GE_SFP, HWIC_AP_AG_B, HWIC_8A,
        WIC_1T, WIC_2T,
        NIM_2T, NIM_ES2_4,
    ]
}

# Módulos más comunes por caso de uso
SERIAL_MODULES: dict[str, str] = {
    # router pt_type → módulo que agrega serial
    "1941":    "HWIC-2T",
    "2901":    "HWIC-2T",
    "2911":    "HWIC-2T",
    "ISR4321": "NIM-2T",
    "ISR4331": "NIM-2T",
}


def get_serial_module(router_model: str) -> ModuleSpec | None:
    """Retorna el módulo serial apropiado para un modelo de router."""
    module_name = SERIAL_MODULES.get(router_model)
    if module_name:
        return ALL_MODULES.get(module_name)
    return None


def resolve_module(name: str) -> ModuleSpec | None:
    """Resuelve un nombre de módulo."""
    return ALL_MODULES.get(name) or ALL_MODULES.get(name.upper())
