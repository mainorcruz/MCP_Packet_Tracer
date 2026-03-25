# application/

Capa de aplicación — casos de uso y DTOs que orquestan la interacción entre la capa MCP y el dominio.

## Estructura

```
application/
├── dto/           → Data Transfer Objects (entrada/salida)
│   ├── requests.py
│   └── responses.py
└── use_cases/     → 8 casos de uso (wrappers delgados sobre servicios del dominio)
```

## dto/

### `requests.py`
DTOs de entrada — lo que llega desde el tool registry:

| DTO | Campos clave | Propósito |
|-----|-------------|-----------|
| `PlanTopologyDTO` | routers, pcs_per_lan, routing, template, dhcp, has_wan | Parámetros para planificar topología |
| `FixPlanDTO` | plan_json | JSON serializado del plan a corregir |
| `ExportDTO` | plan_json, project_name, output_dir | Parámetros para exportar artefactos |

### `responses.py`
DTOs de salida — lo que retornan los use cases:

| DTO | Campos | Propósito |
|-----|--------|-----------|
| `BuildResponse` | plan_json, script, configs, validation, explanation, estimation, is_valid, errors, warnings | Resultado del full build completo |
| `ValidationResponse` | is_valid, errors, warnings | Resultado de validación |
| `FixResponse` | plan_json, fixes_applied, is_valid, remaining_errors | Resultado de auto-fix |
| `ExportResponse` | status, project_dir, files | Resultado de exportación a disco |

## use_cases/

8 wrappers delgados que convierten DTOs en llamadas a servicios del dominio:

| Archivo | Función | Flujo |
|---------|---------|-------|
| `plan_topology.py` | `plan_topology(dto)` | DTO → TopologyRequest → `orchestrator.plan_from_request()` |
| `full_build.py` | `full_build(dto)` | plan → validate → generate script + configs → explain → estimate → BuildResponse |
| `validate_plan.py` | `validate_plan_uc(plan)` | `validator.validate_plan()` → ValidationResponse |
| `fix_plan.py` | `fix_plan_uc(plan)` | `auto_fixer.fix_plan()` → re-validate → FixResponse |
| `generate_script.py` | `generate_script_uc(plan, include_configs)` | PTBuilder script con o sin configs embebidas |
| `generate_configs.py` | `generate_configs_uc(plan)` | `cli_config_generator.generate_all_configs()` |
| `explain_plan.py` | `explain_plan_uc(plan)` | `explainer.explain_plan()` → list[str] |
| `export_artifacts.py` | `export_artifacts_uc(plan, output_dir)` | `ManualExecutor.execute()` → ExportResponse |

Cada use case mantiene la responsabilidad única: transformar DTOs, invocar servicios, y devolver responses tipados.
