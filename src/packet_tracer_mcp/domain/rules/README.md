# domain/rules/

Reglas de validación independientes organizadas por dominio. Cada archivo contiene funciones puras que reciben un `TopologyPlan` y retornan listas de `PlanError`.

Son invocadas por el servicio `validator.py` — nunca directamente desde fuera del dominio.

## Archivos

### `device_rules.py` — Validación de dispositivos

```python
validate_devices(plan: TopologyPlan) → list[PlanError]
```

**Verificaciones:**
| Check | ErrorCode | Descripción |
|-------|-----------|-------------|
| Nombres duplicados | `DUPLICATE_DEVICE_NAME` | Dos dispositivos con el mismo nombre |
| Modelo inválido | `UNKNOWN_DEVICE_MODEL` | Modelo no existe en el catálogo de `devices.py` |

---

### `cable_rules.py` — Validación de enlaces y cables

```python
validate_links(plan: TopologyPlan) → tuple[list[PlanError], list[PlanError]]
```

Retorna `(errores, warnings)` — los warnings son para cables incorrectos pero no fatales.

**Verificaciones:**
| Check | ErrorCode | Descripción |
|-------|-----------|-------------|
| Dispositivo no existe | `DEVICE_NOT_FOUND` | Link referencia un dispositivo inexistente |
| Puerto no existe | `INVALID_PORT` | Puerto no existe en el modelo del dispositivo |
| Puerto reutilizado | `PORT_ALREADY_USED` | Mismo puerto usado en dos links diferentes |
| Cable desconocido | `INVALID_CABLE_TYPE` | Tipo de cable no reconocido |
| Cable incorrecto | (warning) | Cable no es el recomendado para esa combinación |

**Helper interno:**
- `_check_port(port, model_name)` — Valida que un puerto existe en el modelo del catálogo

---

### `ip_rules.py` — Validación de IPs y DHCP

```python
validate_ips(plan: TopologyPlan) → list[PlanError]
validate_dhcp(plan: TopologyPlan) → list[PlanError]
```

**Verificaciones de IP:**
| Check | ErrorCode | Descripción |
|-------|-----------|-------------|
| IP inválida | `INVALID_IP_ADDRESS` | Formato de IP incorrecto |
| IP duplicada | `IP_CONFLICT` | Misma IP asignada a dos interfaces |

**Verificaciones de DHCP:**
| Check | ErrorCode | Descripción |
|-------|-----------|-------------|
| Router no existe | `DHCP_ROUTER_NOT_FOUND` | Pool asignado a router inexistente |
| Gateway no coincide | `DHCP_GATEWAY_MISMATCH` | Gateway del pool no es IP de ninguna interface del router |
