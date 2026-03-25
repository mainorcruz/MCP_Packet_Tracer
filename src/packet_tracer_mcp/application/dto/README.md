# application/dto/

Data Transfer Objects que definen el contrato de entrada/salida entre la capa MCP (adapters) y la capa de aplicación (use cases).

## Archivos

### `requests.py` — DTOs de entrada

| DTO | Campos principales | Origen |
|-----|-------------------|--------|
| `PlanTopologyDTO` | `routers`, `pcs_per_lan`, `routing`, `template`, `dhcp`, `has_wan`, `router_model`, `switch_model`, `servers`, `access_points`, `laptops_per_lan`, `floating_routes`, `ospf_process_id`, `eigrp_as`, `base_network`, `inter_router_network` | `pt_plan_topology`, `pt_full_build` |
| `FixPlanDTO` | `plan_json` (str serializado) | `pt_fix_plan` |
| `ExportDTO` | `plan_json`, `project_name`, `output_dir` | `pt_export` |

Todos son `@dataclass` simples sin lógica — solo transportan datos.

---

### `responses.py` — DTOs de salida

| DTO | Campos principales | Retornado por |
|-----|-------------------|---------------|
| `BuildResponse` | `plan_json`, `script`, `configs`, `validation`, `explanation`, `estimation`, `is_valid`, `errors`, `warnings` | `full_build` |
| `ValidationResponse` | `is_valid`, `errors`, `warnings` | `validate_plan_uc` |
| `FixResponse` | `plan_json`, `fixes_applied`, `is_valid`, `remaining_errors` | `fix_plan_uc` |
| `ExportResponse` | `status`, `project_dir`, `files` | `export_artifacts_uc` |

Todos son `@dataclass` que encapsulan la respuesta para serialización JSON en la capa MCP.
