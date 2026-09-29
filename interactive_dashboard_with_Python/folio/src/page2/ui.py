"""Página 2 – Detalle: indicadores + gráfico de 5 años."""
from shiny import module, ui
from shinywidgets import output_widget

from ..config import CHOICES, HISTORY_YEARS


@module.ui
def page2_ui():
    return ui.TagList(
        ui.layout_columns(
            ui.input_select("ticker", "Activo", CHOICES, selected="AAPL"),
            ui.output_ui("subtitle"),
            col_widths=[4, 8],
            class_="mt-3",
        ),
        ui.output_ui("indicators"),
        ui.card(
            ui.card_header(f"Precio de cierre ajustado – últimos {HISTORY_YEARS} años"),
            output_widget("price_chart"),
            full_screen=True,
        ),
    )
