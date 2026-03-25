# packet_tracer_mcp

Módulo principal del servidor MCP para Cisco Packet Tracer.

## Arquitectura

Sigue **Clean Architecture / Domain-Driven Design** con separación clara de capas:

```
packet_tracer_mcp/
├── adapters/mcp/       → Capa de protocolo MCP (tools + resources)
├── application/        → Casos de uso + DTOs (entrada/salida)
├── domain/             → Lógica de negocio pura
│   ├── models/         → Modelos de datos (Plan, Request, Error)
│   ├── services/       → Servicios (Orchestrator, IPPlanner, Validator...)
│   └── rules/          → Reglas de validación (dispositivos, cables, IPs)
├── infrastructure/     → Preocupaciones externas
│   ├── catalog/        → Catálogo de dispositivos, cables, templates
│   ├── generator/      → Generadores de scripts PTBuilder + CLI configs
│   ├── execution/      → Estrategias de despliegue (manual, live bridge)
│   └── persistence/    → Persistencia de proyectos
├── shared/             → Enums, constantes, utilidades
├── server.py           → Punto de entrada MCP
├── settings.py         → Configuración global
└── __main__.py         → Entry point: python -m packet_tracer_mcp
```

## Flujo de datos

```
Request → TopologyRequest → Orchestrator → TopologyPlan → Validator
                                                ↓
                                    Generator (PTBuilder JS + CLI configs)
                                                ↓
                                    Executor (Manual / Deploy / Live Bridge)
```

## Archivos raíz

| Archivo | Propósito |
|---------|-----------|
| `server.py` | Crea la instancia `FastMCP`, registra tools/resources, arranca en HTTP (:39000) o stdio |
| `__main__.py` | Entry point para `python -m packet_tracer_mcp` — invoca `server.main()` |
| `settings.py` | Constantes globales: `VERSION` (0.4.0), `SERVER_NAME`, `SERVER_INSTRUCTIONS` |

## Ejecución

```bash
# Streamable HTTP (default, puerto 39000)
python -m packet_tracer_mcp

# Modo stdio (debug/legacy)
python -m packet_tracer_mcp --stdio
```

## Dependencias entre capas

```
adapters/mcp → application/use_cases → domain/services → domain/models
                                              ↓
                                    infrastructure/ (catalog, generator, execution)
                                              ↓
                                         shared/ (enums, constants, utils)
```

Sin dependencias circulares. La capa `domain` nunca importa de `infrastructure` directamente — la comunicación es a través de las interfaces.
