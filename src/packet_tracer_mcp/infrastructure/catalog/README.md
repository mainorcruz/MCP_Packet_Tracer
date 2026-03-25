# infrastructure/catalog/

Catálogo estático de dispositivos, cables, aliases y templates verificados contra Packet Tracer 8.x. Todos los datos son inmutables (`frozen=True` en modelos Pydantic).

Esta carpeta es la **fuente de verdad** para qué dispositivos, puertos y cables existen en PT.

## Archivos

### `devices.py` — Catálogo de dispositivos (11 modelos)

**Modelos Pydantic:**
- `PortSpec` — Especificación de puerto: `speed` (PortSpeed), `slot` (int), `full_name` (str completo como "GigabitEthernet0/0")
- `DeviceModel` — Dispositivo: `name`, `pt_type` (nombre en PT), `category` (DeviceCategory), `ports` (list[PortSpec]), `display_name`

**Modelos verificados:**

| Modelo | Categoría | Puertos | Notas |
|--------|-----------|---------|-------|
| `1941` | Router | 2× GigabitEthernet | Básico |
| `2901` | Router | 2× GigabitEthernet | |
| `2911` | Router | 3× GigabitEthernet | **Default** — más puertos |
| `ISR4321` | Router | 2× GigabitEthernet | Moderno |
| `2960-24TT` | Switch | 24× FastEthernet + 2× GigabitEthernet | **Default** |
| `3560-24PS` | Switch | 24× FastEthernet + 2× GigabitEthernet | Layer 3 capable |
| `PC-PT` | PC | 1× FastEthernet0 | End device |
| `Server-PT` | Server | 1× FastEthernet0 | End device |
| `Laptop-PT` | Laptop | 1× FastEthernet0 | End device |
| `Cloud-PT` | Cloud | 1× Ethernet6 | WAN simulation |
| `AccessPoint-PT` | AP | 1× Port 0 | Wireless |

> **Nota:** Ningún router tiene puertos Serial por defecto. Serial requiere módulos HWIC físicos.

**Funciones:**
| Función | Firma | Descripción |
|---------|-------|-------------|
| `resolve_model(name)` | `str → DeviceModel` | Resuelve nombre o alias a modelo (usa `aliases.py`) |
| `get_ports_by_speed(model, speed)` | `DeviceModel, PortSpeed → list[PortSpec]` | Filtra puertos por velocidad |
| `get_valid_ports(model_name)` | `str → set[str]` | Set de nombres completos de puertos válidos |

**Constante:** `DEVICE_CATALOG: dict[str, DeviceModel]` — Diccionario nombre → modelo.

---

### `cables.py` — Tipos de cable y reglas de inferencia

**Constantes:**
- `CABLE_TYPES` — 5 tipos: `straight`, `cross`, `serial`, `fiber`, `console`
- `CABLE_RULES` — 20+ reglas como tuplas `(category_a, category_b) → cable_type`

**Reglas principales:**
| Combinación | Cable |
|-------------|-------|
| Router ↔ Router | cross |
| Router ↔ PC/Server | cross |
| Switch ↔ cualquier cosa | straight |
| Router ↔ Cloud | straight |
| Switch ↔ AccessPoint | straight |

**Función:**
```python
infer_cable(cat_a: str, cat_b: str) → str
```
Infiere el cable correcto dadas dos categorías de dispositivo.

---

### `aliases.py` — Aliases comunes para modelos

**Constante:** `MODEL_ALIASES: dict[str, str]`

Mapea nombres informales a modelos del catálogo:
```
"router" → "2911"     "switch" → "2960-24TT"    "pc" → "PC-PT"
"server" → "Server-PT"  "laptop" → "Laptop-PT"    "cloud" → "Cloud-PT"
"ap" → "AccessPoint-PT"  "cisco 2911" → "2911"     ...
```

Usado por `resolve_model()` en `devices.py` para que el LLM pueda usar nombres naturales.

---

### `templates.py` — Templates de topología (9 templates)

**Modelo:** `TemplateSpec`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | `str` | Nombre human-readable |
| `key` | `TopologyTemplate` | Enum key |
| `description` | `str` | Descripción del template |
| `min_routers` / `max_routers` | `int` | Límites de routers permitidos |
| `defaults` | `dict` | Valores por defecto del template |
| `requires_wan` | `bool` | Si necesita nube WAN |
| `default_routing` | `RoutingProtocol` | Routing recomendado |
| `tags` | `list[str]` | Tags para búsqueda |

**Templates disponibles:**
| Key | Nombre | Routers | Routing | WAN | Descripción |
|-----|--------|---------|---------|-----|-------------|
| `single_lan` | Single LAN | 1 | static | No | Red simple: 1 router, 1 switch, N PCs |
| `multi_lan` | Multi-LAN | 2–20 | static | No | Cadena de routers, cada uno con su LAN |
| `multi_lan_wan` | Multi-LAN + WAN | 2–20 | static | Sí | Multi-LAN con nube WAN |
| `star` | Star | 1 | static | No | 1 router con N switches (hub & spoke plano) |
| `hub_spoke` | Hub & Spoke | 2–20 | static | No | 1 hub router + N spoke routers |
| `branch_office` | Branch Office | 2–10 | static | Sí | Oficina central + sucursales con WAN |
| `three_router_triangle` | Triangle | 3 | ospf | No | 3 routers con redundancia |
| `router_on_a_stick` | Router on a Stick | 1 | none | No | Inter-VLAN routing |
| `custom` | Custom | 1–20 | static | No | Sin restricciones |

**Funciones:**
- `get_template(key)` → `TemplateSpec`
- `list_templates()` → `list[TemplateSpec]`
