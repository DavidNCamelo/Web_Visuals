"""Configuración central: activos, periodos y colores."""

# ticker -> (nombre a mostrar, tipo). Tipo: "stock" | "etf"
ASSETS: dict[str, dict] = {
    "ICOLCAP.CL": {"name": "icolcap", "type": "etf"},
    "CIB": {"name": "Cibest", "type": "stock"},
    "NU": {"name": "Nu Holdings", "type": "stock"},
    "IUIT.L": {"name": "iShares S&P 500 Tech", "type": "etf"},
    "GOAU": {"name": "US Global GO GOLD", "type": "etf"},
    "NVDA": {"name": "Nvidia", "type": "stock"},
    "INTC": {"name": "IBM", "type": "stock"},
}

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
COLOR_UP = "#2a78d6"
COLOR_DOWN = "#eb6834"
COLOR_LINE = "#2a78d6"
COLOR_MUTED = "#52514e"
