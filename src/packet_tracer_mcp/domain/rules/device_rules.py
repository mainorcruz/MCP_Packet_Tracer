"""Reglas de validación de dispositivos."""

from __future__ import annotations
from ..models.plans import TopologyPlan
from ..models.errors import PlanError, ErrorCode, ValidationResult
from ...infrastructure.catalog.devices import resolve_model


def validate_devices(plan: TopologyPlan) -> list[PlanError]:
    """Valida que todos los dispositivos sean válidos."""
    errors: list[PlanError] = []
    names_seen: set[str] = set()

    for dev in plan.devices:
        if dev.name in names_seen:
            errors.append(PlanError(
                code=ErrorCode.DUPLICATE_DEVICE_NAME,
                device=dev.name,
                message=f"Nombre de dispositivo duplicado: '{dev.name}'",
                suggestion="Renombrar uno de los dispositivos duplicados.",
            ))
        names_seen.add(dev.name)

        model = resolve_model(dev.model)
        if model is None:
            errors.append(PlanError(
                code=ErrorCode.UNKNOWN_DEVICE_MODEL,
                device=dev.name,
                message=f"Modelo desconocido '{dev.model}'.",
                suggestion=(
                    "Usar un modelo válido. Routers: 1841, 1941, 2811, 2901, 2911, ISR4321, ISR4331, Router-PT. "
                    "Switches: 2950-24, 2950T-24, 2960-24TT, 3560-24PS, 3650-24PS, Switch-PT. "
                    "End devices: PC-PT, Server-PT, Laptop-PT, TabletPC-PT, SMARTPHONE-PT, Printer-PT. "
                    "Otros: Cloud-PT, AccessPoint-PT, Hub-PT, 5505, 5506-X, WLC-PT, DSL-Modem-PT, Cable-Modem-PT."
                ),
            ))

    return errors
