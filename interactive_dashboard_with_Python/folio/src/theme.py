"""Tema visual de la app (compilado a CSS vía Sass con shiny.ui.Theme).

Centraliza aquí lo que antes intentaba resolverse con un stylesheet externo
(como el de la versión en Dash) para que colores de marca, tabs, navbar y
tarjetas usen la misma paleta que los gráficos de Plotly.
"""
from __future__ import annotations

from shiny.ui import Theme, ValueBoxTheme

from .config import COLOR_DOWN, COLOR_LINE, COLOR_MUTED, COLOR_UP


def mix_with_white(hex_color: str, amount: float) -> str:
    """Aclara un color mezclándolo con blanco (amount=0 color puro, 1 blanco)."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    r, g, b = (round(c + (255 - c) * amount) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


TINT_UP = mix_with_white(COLOR_UP, 0.88)
TINT_DOWN = mix_with_white(COLOR_DOWN, 0.88)

# Fondo gris-azulado (plateado), con las tarjetas en blanco puro para que resalten.
BODY_BG = "#e9edf2"
CARD_BG = "#ffffff"

# Tema global: variables de Bootstrap (Sass) + reglas puntuales para navbar y tabs.
app_theme = (
    Theme(preset="shiny")
    .add_defaults(
        primary=COLOR_LINE,
        secondary=COLOR_MUTED,
        danger=COLOR_DOWN,
        body_color="#262b33",
        body_bg=BODY_BG,
        border_radius="0.65rem",
        font_size_base="0.95rem",
    )
    .add_rules(
        f"""
        body {{ background-color: {BODY_BG}; }}

        .navbar {{ background-color: {COLOR_LINE} !important; }}
        .navbar .navbar-brand,
        .navbar .nav-link {{ color: rgba(255, 255, 255, .8) !important; }}
        .navbar .nav-link.active {{ color: #ffffff !important; font-weight: 600; }}

        .nav-tabs .nav-link {{ color: {COLOR_MUTED}; }}
        .nav-tabs .nav-link.active {{
          color: {COLOR_LINE};
          border-bottom: 3px solid {COLOR_LINE};
          font-weight: 600;
        }}

        .card {{
          background-color: {CARD_BG};
          border: 1px solid #d7dde4;
          box-shadow: 0 1px 2px rgba(30, 41, 59, .06);
        }}

        /* Tabla de variaciones: refuerza el color que ya pinta styles= en DataGrid */
        .shiny-data-grid table td {{ vertical-align: middle; }}
        """
    )
)


def variation_theme(is_up: bool | None) -> ValueBoxTheme | None:
    """Tema de value_box según el signo de la variación (mismo azul/naranja que los gráficos)."""
    if is_up is None:
        return None
    fg = COLOR_UP if is_up else COLOR_DOWN
    bg = TINT_UP if is_up else TINT_DOWN
    return ValueBoxTheme(class_=None, fg=fg, bg=bg)


def variation_cell_styles(values, col_index: int) -> list[dict]:
    """Estilos por fila para una columna de % en un render.DataGrid, mismo azul/naranja.

    `values` son las variaciones sin formatear (fracciones, pueden traer NaN/None);
    `col_index` es la posición (0-based) de la columna a colorear.
    """
    styles = []
    for i, v in enumerate(values):
        if v is None or (isinstance(v, float) and v != v):  # NaN
            color = COLOR_MUTED
        else:
            color = COLOR_UP if v >= 0 else COLOR_DOWN
        styles.append({"rows": [i], "cols": [col_index], "style": {"color": color, "font-weight": "600"}})
    return styles
