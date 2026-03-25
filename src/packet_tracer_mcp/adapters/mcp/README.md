# adapters/mcp/

Capa de protocolo MCP — registra las herramientas (tools) y recursos (resources) que el LLM puede invocar.

## Archivos

### `tool_registry.py`
**~1050 líneas** — Registro monolítico de los 22 MCP tools.

Función principal: `register_tools(mcp: FastMCP) → None`

Cada tool se define como una función decorada con `@mcp.tool()` dentro de `register_tools()`.

#### Tools registradas (22)

| Grupo | Tool | Descripción |
|-------|------|-------------|
| **Consulta** | `pt_list_devices` | Catálogo de dispositivos con puertos |
| | `pt_list_templates` | Templates de topología disponibles |
| | `pt_get_device_details` | Detalle de un modelo específico |
| **Estimación** | `pt_estimate_plan` | Dry-run sin generar plan completo |
| **Planificación** | `pt_plan_topology` | Genera plan completo → JSON |
| **Validación** | `pt_validate_plan` | Errores/warnings tipados |
| | `pt_fix_plan` | Auto-corrección + re-validación |
| | `pt_explain_plan` | Explicación en lenguaje natural |
| **Generación** | `pt_generate_script` | Script PTBuilder JS (± configs) |
| | `pt_generate_configs` | CLI IOS por dispositivo |
| **Pipeline** | `pt_full_build` | Plan + validar + generar + explicar + estimar |
| **Despliegue** | `pt_deploy` | Clipboard + archivos + instrucciones |
| | `pt_export` | Solo archivos a disco |
| | `pt_live_deploy` | Despliegue directo vía HTTP bridge |
| **Bridge** | `pt_bridge_status` | Verificar conexión con PT |
| **Proyectos** | `pt_list_projects` | Listar topologías guardadas |
| | `pt_load_project` | Cargar proyecto por nombre |
| **Interacción** | `pt_query_topology` | Consultar dispositivos/links actuales en PT |
| | `pt_delete_device` | Eliminar dispositivo |
| | `pt_rename_device` | Renombrar dispositivo |
| | `pt_move_device` | Mover dispositivo en canvas |
| | `pt_delete_link` | Eliminar enlace |
| | `pt_send_raw` | Enviar JS arbitrario al Script Engine |

#### Helpers internos
- `_http_get(url)` / `_http_post(url, data)` — Comunicación HTTP con el bridge
- `_js_escape(s)` — Escape de strings para JS
- `_bridge_is_up()` / `_bridge_pt_connected()` — Verificación de conectividad

### `resource_registry.py`
**~64 líneas** — Registro de 5 MCP resources estáticos.

Función principal: `register_resources(mcp: FastMCP) → None`

| Resource URI | Contenido |
|-------------|-----------|
| `pt://catalog/devices` | Catálogo completo de dispositivos con puertos |
| `pt://catalog/cables` | Tipos de cable disponibles |
| `pt://catalog/aliases` | Alias comunes → modelo real |
| `pt://catalog/templates` | Templates con descripción, rangos, routing default |
| `pt://capabilities` | Versión, features, límites del servidor |
