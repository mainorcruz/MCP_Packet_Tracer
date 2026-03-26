"""Catálogo de cables y reglas de cableado."""

from __future__ import annotations

# Tipos de cable en Packet Tracer (key → display name)
# Keys son los strings que PTBuilder acepta en addLink()
CABLE_TYPES: dict[str, str] = {
    "straight":  "Copper Straight-Through",
    "cross":     "Copper Cross-Over",
    "serial":    "Serial DCE",
    "fiber":     "Fiber",
    "console":   "Console",
    "phone":     "Phone",
    "coaxial":   "Coaxial",
    "auto":      "Automatic",
}

# Tipos de cable completos de PT (para referencia/validación extendida)
# Estos son todos los que PT soporta internamente
ALL_LINK_TYPES: dict[str, int] = {
    "straight":  8100,
    "cross":     8101,
    "roll":      8102,
    "fiber":     8103,
    "phone":     8104,
    "cable":     8105,
    "serial":    8106,
    "auto":      8107,
    "console":   8108,
    "wireless":  8109,
    "coaxial":   8110,
    "octal":     8111,
    "cellular":  8112,
    "usb":       8113,
    "custom_io": 8114,
}

# Reglas: (categoría_a, categoría_b) → tipo de cable
CABLE_RULES: dict[tuple[str, str], str] = {
    ("router", "switch"):       "straight",
    ("switch", "router"):       "straight",
    ("switch", "pc"):           "straight",
    ("pc", "switch"):           "straight",
    ("switch", "server"):       "straight",
    ("server", "switch"):       "straight",
    ("switch", "laptop"):       "straight",
    ("laptop", "switch"):       "straight",
    ("switch", "accesspoint"):  "straight",
    ("accesspoint", "switch"):  "straight",
    ("router", "router"):       "cross",
    ("switch", "switch"):       "cross",
    ("router", "cloud"):        "straight",
    ("cloud", "router"):        "straight",
    ("router", "pc"):           "cross",
    ("pc", "router"):           "cross",
    ("router", "server"):       "cross",
    ("server", "router"):       "cross",
    # Hub connections
    ("hub", "pc"):              "straight",
    ("pc", "hub"):              "straight",
    ("hub", "switch"):          "straight",
    ("switch", "hub"):          "straight",
    ("hub", "router"):          "straight",
    ("router", "hub"):          "straight",
    ("hub", "server"):          "straight",
    ("server", "hub"):          "straight",
    ("hub", "laptop"):          "straight",
    ("laptop", "hub"):          "straight",
    # Firewall connections
    ("firewall", "switch"):     "straight",
    ("switch", "firewall"):     "straight",
    ("firewall", "router"):     "cross",
    ("router", "firewall"):     "cross",
    ("firewall", "pc"):         "straight",
    ("pc", "firewall"):         "straight",
    # WLC connections
    ("wlc", "switch"):          "straight",
    ("switch", "wlc"):          "straight",
    ("wlc", "accesspoint"):     "straight",
    ("accesspoint", "wlc"):     "straight",
    # Modem connections
    ("modem", "router"):        "straight",
    ("router", "modem"):        "straight",
    ("modem", "cloud"):         "straight",
    ("cloud", "modem"):         "straight",
}


def infer_cable(cat_a: str, cat_b: str) -> str:
    """Infiere el tipo de cable correcto entre dos categorías de dispositivo."""
    return CABLE_RULES.get((cat_a, cat_b), "straight")
