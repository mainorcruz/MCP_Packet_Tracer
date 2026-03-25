# domain/services/

6 servicios de negocio que implementan toda la lógica de planificación, validación y transformación de topologías. No dependen de infraestructura — solo de modelos del dominio.

## Archivos

### `orchestrator.py` — Pipeline principal

Transforma un `TopologyRequest` en un `TopologyPlan` completo y validado.

**Función principal:**
```python
plan_from_request(request: TopologyRequest) → tuple[TopologyPlan, ValidationResult]
```

**Pipeline interno:**
1. Normaliza `pcs_per_lan` y `laptops_per_lan` (expande int → lista por router)
2. `_create_devices()` — Crea routers, switches, PCs, laptops, APs, servers, cloud
3. `_create_links()` — Conecta dispositivos según template (router↔router, router↔switch, switch↔PC, etc.)
4. `ip_planner.plan_addressing()` — Asigna IPs, DHCP pools, rutas
5. `_create_validations()` — Genera tests de ping post-despliegue
6. `validate_plan()` — Validación final del plan

**Layout automático:** Calcula posiciones X/Y basándose en constantes de `shared/constants.py` para distribución visual en el canvas de PT.

**Funciones helper:**
- `_normalize_pcs(value, count)` — Convierte int a lista replicada
- `_normalize_laptops(value, count)` — Igual para laptops

---

### `ip_planner.py` — Motor de direccionamiento IP

Asigna direcciones IP a todas las interfaces, configura DHCP y genera rutas.

**Clase:** `IPPlanner`

| Método | Descripción |
|--------|-------------|
| `__init__(lan_base, link_base)` | Inicializa generadores de subredes |
| `next_lan_subnet()` | Siguiente subred /24 para LAN |
| `next_link_subnet()` | Siguiente subred /30 para enlace inter-router |
| `plan_addressing(plan, routing, dhcp, ...)` | Pipeline completo de asignación |

**Esquema de direccionamiento:**
- **LANs:** `192.168.x.0/24` — Gateway = `.1`, PCs desde `.2`
- **Inter-router:** `10.0.x.0/30` — 2 hosts por enlace

**Generación de rutas:**
| Método | Protocolo | Descripción |
|--------|-----------|-------------|
| `_plan_static_routes()` | static | Descubrimiento BFS + generación de `ip route` |
| `_plan_ospf()` | OSPF | router-id, networks con wildcard mask, area 0 |
| `_plan_rip()` | RIP v2 | networks classful, no auto-summary |
| `_plan_eigrp()` | EIGRP | AS number, networks con wildcard, no auto-summary |
| `_plan_floating_static_routes()` | static (backup) | Rutas alternativas con AD=254 |

---

### `validator.py` — Orquestador de validación

Ejecuta todas las reglas de validación sobre un plan.

**Función principal:**
```python
validate_plan(plan: TopologyPlan) → ValidationResult
```

**Flujo:** Llama secuencialmente a:
1. `validate_devices(plan)` — desde `rules/device_rules.py`
2. `validate_links(plan)` — desde `rules/cable_rules.py`
3. `validate_ips(plan)` — desde `rules/ip_rules.py`
4. `validate_dhcp(plan)` — desde `rules/ip_rules.py`

Sincroniza errores/warnings de vuelta a `plan.errors` y `plan.warnings` para compatibilidad.

---

### `auto_fixer.py` — Auto-corrección de errores

Corrige automáticamente errores comunes en planes mal formados.

**Función principal:**
```python
fix_plan(plan: TopologyPlan) → tuple[TopologyPlan, list[str]]
```

Retorna el plan corregido + lista de fixes aplicados (human-readable).

**Correcciones disponibles:**
| Fix interno | Qué corrige |
|-------------|-------------|
| `_fix_cables()` | Tipo de cable incorrecto → infiere el correcto según categorías |
| `_fix_insufficient_ports()` | Router sin suficientes puertos GigE → upgrade a modelo 2911 |
| `_fix_invalid_ports()` | Puerto inexistente → reasigna al primer puerto válido disponible |

---

### `explainer.py` — Generador de explicaciones

Produce explicaciones en lenguaje natural de las decisiones del plan.

**Función principal:**
```python
explain_plan(plan: TopologyPlan) → list[str]
```

**Genera explicaciones sobre:**
- Conteo de dispositivos por categoría
- Estrategia de subredes (LANs y enlaces)
- Tipos de cable usados y razón
- Configuración DHCP (pools, exclusiones)
- Protocolo de routing y configuración
- Tests de validación incluidos

---

### `estimator.py` — Estimación sin build completo

Dry-run que estima complejidad y recursos sin generar el plan completo.

**Funciones:**
| Función | Entrada | Salida |
|---------|---------|--------|
| `estimate_from_request(request)` | `TopologyRequest` | `dict` con conteos estimados |
| `estimate_from_plan(plan)` | `TopologyPlan` | `dict` con conteos reales + estado |
| `_estimate_complexity(req)` | `TopologyRequest` | `str`: "simple", "moderada", "compleja", "muy compleja" |

**Criterios de complejidad:**
- **Simple:** ≤2 routers, sin WAN, routing estático
- **Moderada:** 3–4 routers, o OSPF/EIGRP
- **Compleja:** 5–8 routers, o WAN + routing dinámico
- **Muy compleja:** 9+ routers
