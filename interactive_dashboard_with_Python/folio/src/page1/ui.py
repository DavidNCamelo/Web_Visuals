"""Página 1 – Valores globales + variación por periodo."""
from shiny import module, ui
from shinywidgets import output_widget

from ..config import PERIODS


@module.ui
def page1_ui():
    tabs = [
        ui.nav_panel(
            label,
            ui.layout_columns(
                ui.card(
                    ui.card_header(f"Variación {label.lower()}"),
                    output_widget(f"bar_{key}"),
                    full_screen=True,
                ),
                ui.card(
                    ui.card_header("Detalle"),
                    ui.output_data_frame(f"table_{key}"),
                ),
                col_widths=[7, 5],
            ),
            value=key,
        )
        for key, label, _ in PERIODS
    ]
    return ui.TagList(
        ui.h4("Valores globales", class_="mt-3"),
        ui.output_ui("cards"),
        ui.navset_card_tab(*tabs, id="period"),
    )
