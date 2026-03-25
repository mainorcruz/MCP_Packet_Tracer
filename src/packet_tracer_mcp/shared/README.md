# shared/

Utilidades, constantes y enumeraciones compartidas por todas las capas del proyecto.

## Archivos

### `constants.py`
Constantes del sistema usadas globalmente:

| Constante | Valor | Descripción |
|-----------|-------|-------------|
| `DEFAULT_ROUTER` | `"2911"` | Modelo de router por defecto |
| `DEFAULT_SWITCH` | `"2960-24TT"` | Modelo de switch por defecto |
| `LAYOUT_X_START`, `LAYOUT_Y_ROUTER`, etc. | px | Posiciones del canvas de Packet Tracer para layout automático |
| `DEFAULT_LAN_BASE` | `"192.168.0.0/16"` | Base para subredes LAN (/24 por defecto) |
| `DEFAULT_LINK_BASE` | `"10.0.0.0/16"` | Base para enlaces inter-router (/30) |
| `DEFAULT_DNS` | `"8.8.8.8"` | Servidor DNS por defecto |
| `PREFIX_TO_MASK` | dict | Lookup CIDR → máscara decimal (ej: 24 → 255.255.255.0) |
| `CAPABILITIES` | dict | Features soportadas, límites, y versión — expuesto como MCP resource |

### `enums.py`
6 enumeraciones `str, Enum` para tipado fuerte:

| Enum | Valores | Uso |
|------|---------|-----|
| `RoutingProtocol` | static, ospf, eigrp, rip, none | Protocolo de enrutamiento del plan |
| `TopologyTemplate` | single_lan, multi_lan, star, hub_spoke, etc. (9 total) | Template de topología |
| `DeviceCategory` | router, switch, pc, server, laptop, cloud, accesspoint | Categoría de dispositivo |
| `DeviceRole` | core_router, branch_router, edge_router, access_switch, etc. | Rol semántico en la topología |
| `CableType` | straight, cross, serial, fiber, console | Tipo de cable |
| `PortSpeed` | FastEthernet, GigabitEthernet, Serial, Console | Velocidad de puerto |

### `utils.py`
3 funciones de utilidad:

| Función | Firma | Descripción |
|---------|-------|-------------|
| `prefix_to_mask(prefix)` | `int → str` | CIDR a máscara decimal (ej: 24 → "255.255.255.0") |
| `wildcard_mask(network)` | `IPv4Network → str` | Calcula wildcard mask (para OSPF) |
| `first_ip(interfaces)` | `dict → str` | Extrae la primera IP de un dict de interfaces |
