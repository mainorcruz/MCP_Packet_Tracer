# domain/models/

Modelos Pydantic que definen el contrato de datos del sistema. Son el lenguaje compartido entre todas las capas.

## Archivos

### `requests.py` — TopologyRequest

Modelo de entrada del LLM — define qué topología construir.

| Campo | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `template` | `TopologyTemplate` | `multi_lan` | Plantilla base de la topología |
| `routers` | `int (1–20)` | `2` | Número de routers |
| `switches_per_router` | `int (0–4)` | `1` | Switches conectados a cada router |
| `pcs_per_lan` | `list[int] \| int` | `3` | PCs por LAN (int se replica a cada router) |
| `laptops_per_lan` | `list[int] \| int` | `0` | Laptops por LAN |
| `servers` | `int (0–10)` | `0` | Servidores en la primera LAN |
| `access_points` | `int (0–10)` | `0` | Access Points |
| `has_wan` | `bool` | `False` | Incluir nube WAN conectada al primer router |
| `dhcp` | `bool` | `True` | Habilitar configuración DHCP en routers |
| `routing` | `RoutingProtocol` | `static` | Protocolo de enrutamiento |
| `router_model` | `str` | `"2911"` | Modelo de router a utilizar |
| `switch_model` | `str` | `"2960-24TT"` | Modelo de switch a utilizar |
| `base_network` | `str` | `"192.168.0.0/16"` | Red base para LANs (/24) |
| `inter_router_network` | `str` | `"10.0.0.0/16"` | Red base para enlaces inter-router (/30) |
| `floating_routes` | `bool` | `False` | Generar rutas estáticas de respaldo (AD=254) |
| `ospf_process_id` | `int` | `1` | ID de proceso OSPF |
| `eigrp_as` | `int` | `100` | AS number de EIGRP |

---

### `plans.py` — Modelos del plan

Resultado completo y validado de la planificación. `TopologyPlan` es el modelo central del sistema.

#### `DevicePlan`
Representa un dispositivo concreto en la topología.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | `str` | Nombre único (ej: `R1`, `SW1`, `PC1`) |
| `model` | `str` | Modelo del catálogo (ej: `2911`, `PC-PT`) |
| `category` | `DeviceCategory` | Categoría (router, switch, pc, etc.) |
| `role` | `DeviceRole \| None` | Rol semántico (core_router, access_switch, etc.) |
| `x`, `y` | `int` | Posición en el canvas de Packet Tracer |
| `interfaces` | `dict[str, str]` | Mapa interface → IP/CIDR (ej: `{"GigabitEthernet0/0": "192.168.1.1/24"}`) |
| `gateway` | `str \| None` | Gateway por defecto (solo PCs/servers) |

#### `LinkPlan`
Conexión física entre dos dispositivos.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `from_device` | `str` | Nombre del dispositivo A |
| `from_port` | `str` | Puerto en dispositivo A |
| `to_device` | `str` | Nombre del dispositivo B |
| `to_port` | `str` | Puerto en dispositivo B |
| `cable_type` | `CableType` | Tipo de cable (straight, cross, etc.) |

#### `DHCPPool`
Configuración de pool DHCP en un router.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `pool_name` | `str` | Nombre del pool (ej: `LAN1_POOL`) |
| `router` | `str` | Router que sirve el pool |
| `network` | `str` | Red del pool (ej: `192.168.1.0`) |
| `mask` | `str` | Máscara (ej: `255.255.255.0`) |
| `gateway` | `str` | Gateway del pool (ej: `192.168.1.1`) |
| `dns` | `str` | Servidor DNS (default `8.8.8.8`) |
| `excluded_start` | `str` | Inicio del rango excluido |
| `excluded_end` | `str` | Fin del rango excluido |

#### `StaticRoute`
Ruta estática para un router.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `destination` | `str` | Red destino |
| `mask` | `str` | Máscara de destino |
| `next_hop` | `str` | IP del siguiente salto |
| `admin_distance` | `int \| None` | Distancia administrativa (254 para floating) |

#### `OSPFConfig`, `RIPConfig`, `EIGRPConfig`
Configuración de protocolos de enrutamiento dinámico por router.

#### `ValidationCheck`
Test de verificación post-despliegue (ping tests).

#### `TopologyPlan`
Modelo central que agrupa todo el plan:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | `str` | Nombre de la topología |
| `devices` | `list[DevicePlan]` | Todos los dispositivos |
| `links` | `list[LinkPlan]` | Todos los enlaces |
| `dhcp_pools` | `list[DHCPPool]` | Pools DHCP |
| `static_routes` | `dict[str, list[StaticRoute]]` | Rutas por router |
| `ospf_configs` | `dict[str, OSPFConfig]` | Config OSPF por router |
| `rip_configs` | `dict[str, RIPConfig]` | Config RIP por router |
| `eigrp_configs` | `dict[str, EIGRPConfig]` | Config EIGRP por router |
| `validations` | `list[ValidationCheck]` | Tests de verificación |
| `errors` | `list[dict]` | Errores de validación |
| `warnings` | `list[dict]` | Advertencias |
| `is_valid` | `bool` | Estado de validación |

**Métodos:** `device_by_name(name)`, `devices_by_category(category)`

---

### `errors.py` — Taxonomía de errores

Sistema tipado de errores con 18 códigos agrupados por categoría.

#### `ErrorCode` (Enum)
| Código | Categoría | Descripción |
|--------|-----------|-------------|
| `UNKNOWN_DEVICE_MODEL` | Dispositivo | Modelo no existe en catálogo |
| `DUPLICATE_DEVICE_NAME` | Dispositivo | Nombre duplicado |
| `INSUFFICIENT_PORTS` | Dispositivo | No hay suficientes puertos |
| `DEVICE_NOT_FOUND` | Link | Dispositivo referenciado no existe |
| `INVALID_PORT` | Link | Puerto no existe en el modelo |
| `PORT_ALREADY_USED` | Link | Puerto ya ocupado por otro link |
| `INVALID_CABLE_TYPE` | Link | Tipo de cable desconocido |
| `INVALID_IP_ADDRESS` | IP | Dirección IP inválida |
| `SUBNET_OVERLAP` | IP | Subredes solapadas |
| `IP_CONFLICT` | IP | IP duplicada |
| `DHCP_ROUTER_NOT_FOUND` | DHCP | Router del pool no existe |
| `DHCP_GATEWAY_MISMATCH` | DHCP | Gateway no coincide con interface |
| `UNSUPPORTED_ROUTING_PROTOCOL` | Routing | Protocolo no soportado |
| `TEMPLATE_CONSTRAINT_VIOLATION` | Template | Parámetros violan restricciones |
| `INVALID_INTERFACE_ASSIGNMENT` | IP | Interface inválida |
| `VALIDATION_ERROR` | General | Error genérico de validación |

#### `PlanError`
Error individual: `code`, `message`, `device`, `suggestion`, `to_dict()`.

#### `ValidationResult`
Colección de errores y warnings con propiedad `is_valid` (True si no hay errores).
