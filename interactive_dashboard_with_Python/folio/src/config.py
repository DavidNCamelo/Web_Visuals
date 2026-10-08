"""Configuración central: activos, periodos y colores."""

import json
import os

# ticker -> (nombre a mostrar, tipo). Tipo: "stock" | "etf"
portfolio = os.environ.get("PORTFOLIO_ASSETS")
ASSETS: dict[str, dict] = json.loads(portfolio)

# Selector: {ticker: "Nombre (TICKER)"}
CHOICES = {t: f"{a['name']} ({t})" for t, a in ASSETS.items()}

# key, etiqueta de la pestaña, tipo de ventana
PERIODS = [
    ("d", "Diaria", {"days": 1}),
    ("m", "Mensual", {"months": 1}),
    ("s", "Semestral", {"months": 6}),
    ("a", "Anual", {"months": 12}),
]

HISTORY_YEARS = 5

# Cache en disco (carpeta /data)
PRICE_TTL_SECONDS = 6 * 3600
INFO_TTL_SECONDS = 24 * 3600

# Colores (paleta de referencia validada: azul / naranja como par divergente)
COLOR_UP = "#2ad633"
COLOR_DOWN = "#eb6834"
COLOR_LINE = "#d69f2a"
COLOR_MUTED = "#52514e"
