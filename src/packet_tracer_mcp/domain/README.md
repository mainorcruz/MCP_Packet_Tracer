# domain/

Lógica de negocio pura del proyecto. No depende de infraestructura ni de frameworks externos (solo Pydantic para modelos).

## Estructura

```
domain/
├── models/      → Modelos de datos inmutables (Plan, Request, Error)
├── services/    → Servicios de negocio (Orchestrator, IPPlanner, Validator...)
└── rules/       → Reglas de validación independientes
```

---

## models/

Modelos Pydantic que representan el contrato de datos del sistema.

### `requests.py` — TopologyRequest
Entrada del LLM — define qué topología construir:

| Campo | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `template` | TopologyTemplate | multi_lan | Plantilla de topología |
| `routers` | int (1-20) | 2 | Número de routers |
| `switches_per_router` | int (0-4) | 1 | Switches por router |
| `pcs_per_lan` | list[int] \| int | 3 | PCs por LAN |
| `servers` | int (0-10) | 0 | Servidores |
| `has_wan` | bool | False | Incluir nube WAN |
| `dhcp` | bool | True | DHCP habilitado |
| `routing` | RoutingProtocol | static | Protocolo de routing |
| `router_model` / `switch_model` | str | 2911 / 2960-24TT | Modelos de dispositivos |
| `base_network` / `inter_router_network` | str | 192.168.0.0/16 / 10.0.0.0/16 | Bases de direccionamiento |
| `floating_routes` | bool | False | Rutas estáticas de respaldo (AD=254) |
| `ospf_process_id` | int | 1 | ID de proceso OSPF |
| `eigrp_as` | int | 100 | AS de EIGRP |

### `plans.py` — Modelos del plan
Resultado validado y completo de la planificación:

| Modelo | Campos clave | Propósito |
|--------|-------------|-----------|
| `DevicePlan` | name, model, category, role, x, y, interfaces, gateway | Un dispositivo concreto |
| `LinkPlan` | from_device, from_port, to_device, to_port, cable_type | Un enlace entre dispositivos |
| `DHCPPool` | pool_name, network, mask, gateway, dns, excluded_start, excluded_end | Pool DHCP en router |
| `StaticRoute` | destination, mask, next_hop, admin_distance | Ruta estática |
| `OSPFConfig` | process_id, router_id, networks (list of network/wildcard/area) | Config OSPF |
| `RIPConfig` | version, networks | Config RIP |
| `EIGRPConfig` | as_number, networks | Config EIGRP |
| `ValidationCheck` | check_type, from_device, to_target, expected | Verificación post-deploy |
| `TopologyPlan` | devices, links, dhcp_pools, static_routes, ospf_configs, etc. | Plan completo |

`TopologyPlan` incluye helpers: `device_by_name(name)`, `devices_by_category(cat)`.

### `errors.py` — Taxonomía de errores
15 códigos de error tipados con mensajes, dispositivos afectados y sugerencias:

| Categoría | Códigos |
|-----------|---------|
| Dispositivos | DUPLICATE_DEVICE, UNKNOWN_MODEL, INSUFFICIENT_PORTS |
| Enlaces | INVALID_PORT, DUPLICATE_LINK, CABLE_MISMATCH, PORT_ALREADY_USED, LINK_DEVICE_NOT_FOUND |
| IP | IP_CONFLICT, INVALID_IP_FORMAT, SUBNET_OVERFLOW |
| DHCP | DHCP_POOL_OVERLAP, DHCP_GATEWAY_MISMATCH |
| Routing | MISSING_ROUTE |
| Template | TEMPLATE_CONSTRAINT_VIOLATION |

Clases: `ErrorCode` (enum), `PlanError` (error + sugerencia), `ValidationResult` (errors + warnings + is_valid).

---

## services/

6 servicios de negocio stateless:

### `orchestrator.py` — Pipeline principal
Función: `plan_from_request(request) → (TopologyPlan, ValidationResult)`

Flujo interno:
1. `_create_devices()` → genera DevicePlan para routers, switches, PCs, servers, cloud
2. `_create_links()` → conecta router↔switch, switch↔PC, router↔router, router↔cloud
3. `ip_planner.plan_addressing()` → asigna IPs, DHCP, rutas
4. `_create_validations()` → genera checks post-deploy (ping tests)
5. `validator.validate_plan()` → valida el plan completo

### `ip_planner.py` — Direccionamiento IP
Clase: `IPPlanner`

| Método | Descripción |
|--------|-------------|
| `plan_addressing(plan, request)` | Asigna subredes LAN (/24), inter-router (/30), DHCP pools, rutas |
| `_assign_lan_subnets()` | 192.168.x.0/24 secuencial por LAN |
| `_assign_inter_router_ips()` | 10.0.x.0/30 por enlace router-router |
| `_create_dhcp_pools()` | Pool por LAN con exclusión del gateway |
| `_create_routes()` | Estáticas, floating, OSPF, RIP o EIGRP según el request |

Esquema: Gateway = .1, PCs desde .2, enlaces /30 (solo 2 hosts).

### `validator.py` — Orquestador de validación
Función: `validate_plan(plan) → ValidationResult`

Ejecuta secuencialmente: `validate_devices()` → `validate_links()` → `validate_ips()` → `validate_dhcp()`.

### `auto_fixer.py` — Auto-corrección
Función: `fix_plan(plan) → (TopologyPlan, list[str])`

3 estrategias de corrección:
- `_fix_cables()` — infiere tipo de cable correcto según categorías
- `_fix_insufficient_ports()` — sube modelo de router si faltan puertos
- `_fix_invalid_ports()` — reasigna puertos inválidos

### `explainer.py` — Explicaciones
Función: `explain_plan(plan) → list[str]`

Genera texto legible: conteo de dispositivos, estrategia de subredes, DHCP, WAN, routing.

### `estimator.py` — Estimación dry-run
Funciones:
- `estimate_from_request(request) → dict` — estimación rápida sin generar plan
- `estimate_from_plan(plan) → dict` — estimación desde plan existente

Retorna: complejidad (simple/medium/complex), conteos, subnets estimadas.

---

## rules/

3 módulos de reglas de validación independientes:

| Archivo | Función | Valida |
|---------|---------|--------|
| `device_rules.py` | `validate_devices(plan)` | Nombres duplicados, modelos desconocidos |
| `cable_rules.py` | `validate_links(plan)` | Puertos válidos, duplicados, tipos de cable |
| `ip_rules.py` | `validate_ips(plan)` + `validate_dhcp(plan)` | Conflictos IP, formato, gateway DHCP |

Cada función retorna `list[PlanError]` (errores) o `tuple[list[PlanError], list[PlanError]]` (errores + warnings).
