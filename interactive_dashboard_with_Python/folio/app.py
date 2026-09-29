"""Portafolio – Shiny para Python.

Ejecutar:  uv run shiny run --reload app.py
"""

from shiny import App, ui

from src.page1.server import page1_server
from src.page1.ui import page1_ui
from src.page2.server import page2_server
from src.page2.ui import page2_ui

app_ui = ui.page_navbar(
    ui.nav_panel("Global", page1_ui("p1")),
    ui.nav_panel("Detalle", page2_ui("p2")),
    title="Portafolio",
    id="nav",
    fillable=False,
)


def server(input, output, session):
    page1_server("p1")
    page2_server("p2")


app = App(app_ui, server)
