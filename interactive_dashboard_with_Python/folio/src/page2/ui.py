"""Página 2 – Detalle: indicadores + gráfico de 5 años."""
from datetime import date, timedelta

from shiny import module, ui
from shinywidgets import output_widget

from ..config import CHOICES, HISTORY_YEARS


@module.ui
def page2_ui():
    return ui.TagList(
        ui.layout_columns(
            ui.input_select("ticker", "Activo", CHOICES, selected="AAPL"),
            ui.input_date_range(
                "date_range",
                "Rango de fechas",
                start=date.today() - timedelta(days=365 * HISTORY_YEARS + 10),
                end=date.today(),
                language="es",
                format="dd/mm/yyyy",
                separator=" a ",
                width="100%",
            ),
            col_widths=[4, 8],
            class_="mt-3",
        ),
        ui.output_ui("subtitle"),
        ui.output_ui("indicators"),
        ui.card(
            ui.card_header("Precio de cierre ajustado"),
            output_widget("price_chart"),
            full_screen=True,
        ),
    )
