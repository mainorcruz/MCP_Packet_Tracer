# application/use_cases/

8 casos de uso que orquestan la interacción entre la capa MCP y el dominio. Son wrappers delgados — convierten DTOs en llamadas a servicios del dominio y formatean la respuesta.

## Principio de diseño

Cada use case:
1. Recibe un DTO o modelo de dominio
2. Llama a uno o más servicios del dominio
3. Retorna un DTO de respuesta

No contienen lógica de negocio — esa vive en `domain/services/`.

## Archivos

### `plan_topology.py`
```python
plan_topology(dto: PlanTopologyDTO) → tuple[TopologyPlan, ValidationResult]
```
Convierte `PlanTopologyDTO` → `TopologyRequest` → `orchestrator.plan_from_request()`.

---

### `full_build.py`
```python
full_build(dto: PlanTopologyDTO) → BuildResponse
```
Pipeline completo: plan → validate → generate script + configs → explain → estimate.
Es el use case más usado por `pt_full_build`.

---

### `validate_plan.py`
```python
validate_plan_uc(plan: TopologyPlan) → ValidationResponse
```
Wrapper sobre `validator.validate_plan()`.

---

### `fix_plan.py`
```python
fix_plan_uc(plan: TopologyPlan) → FixResponse
```
Llama `auto_fixer.fix_plan()`, re-valida, retorna fixes aplicados y estado.

---

### `explain_plan.py`
```python
explain_plan_uc(plan: TopologyPlan) → list[str]
```
Wrapper sobre `explainer.explain_plan()`.

---

### `generate_script.py`
```python
generate_script_uc(plan: TopologyPlan, include_configs: bool = True) → str
```
Genera script PTBuilder JS. Con `include_configs=True` incluye configuraciones CLI embebidas.

---

### `generate_configs.py`
```python
generate_configs_uc(plan: TopologyPlan) → dict[str, str]
```
Wrapper sobre `cli_config_generator.generate_all_configs()`. Retorna `{device_name: config_text}`.

---

### `export_artifacts.py`
```python
export_artifacts_uc(plan: TopologyPlan, output_dir: str) → ExportResponse
```
Wrapper sobre `ManualExecutor.execute()`. Exporta todos los artefactos a disco.
