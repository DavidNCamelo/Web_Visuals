"""Servidor de la página 2."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from shiny import module, reactive, render, ui
from shinywidgets import render_plotly

from ..config import ASSETS, COLOR_LINE, HISTORY_YEARS
from ..data import get_history, get_info
from ..metrics import (dividend_yield, expense_ratio, fmt_big, fmt_pct, fmt_x,
                       is_etf)


def stock_indicators(info: dict) -> list[tuple[str, str, str]]:
    """(título, valor, nota) para una acción / ADR."""
    return [
        ("P/E", fmt_x(info.get("trailingPE")), "Últimos 12 meses"),
        ("P/E forward", fmt_x(info.get("forwardPE")), "Estimado próximo año"),
        ("P/B", fmt_x(info.get("priceToBook")), "Precio / valor en libros"),
        ("PEG", fmt_x(info.get("trailingPegRatio") or info.get("pegRatio"), 2), "P/E ajustado por crecimiento"),
        ("Div. yield", fmt_pct(dividend_yield(info), 2), "Dividendo anual / precio"),
        ("Payout", fmt_pct(info.get("payoutRatio")), "Dividendos / utilidad"),
        ("ROE", fmt_pct(info.get("returnOnEquity")), "Utilidad / patrimonio"),
        ("ROA", fmt_pct(info.get("returnOnAssets")), "Utilidad / activos"),
        ("Margen bruto", fmt_pct(info.get("grossMargins")), "Utilidad bruta / ventas"),
        ("Margen operativo", fmt_pct(info.get("operatingMargins")), "Utilidad operativa / ventas"),
        ("Margen EBITDA", fmt_pct(info.get("ebitdaMargins")), "EBITDA / ventas"),
        ("Margen neto", fmt_pct(info.get("profitMargins")), "Utilidad neta / ventas"),
    ]


def etf_indicators(info: dict) -> list[tuple[str, str, str]]:
    """Equivalentes para ETF/fondo (sin ROE/ROIC/márgenes: no aplican a nivel fondo)."""
    return [
        ("P/E ponderado", fmt_x(info.get("trailingPE")), "Portafolio subyacente"),
        ("P/B ponderado", fmt_x(info.get("priceToBook")), "Portafolio subyacente"),
        ("Div. yield", fmt_pct(dividend_yield(info), 2), "Distribución anual / precio"),
        ("Expense ratio", fmt_pct(expense_ratio(info), 2), "Costo anual del fondo"),
        ("Activos (AUM)", fmt_big(info.get("totalAssets")), "Patrimonio del fondo"),
        ("Beta (3 años)", f"{info['beta3Year']:.2f}" if info.get("beta3Year") else "—", "Sensibilidad al mercado"),
    ]


def price_figure(close: pd.Series, name: str) -> go.Figure:
    fig = go.Figure(
        go.Scatter(
            x=close.index,
            y=close.values,
            mode="lines",
            line=dict(color=COLOR_LINE, width=2),
            name=name,
            hovertemplate="%{x|%d %b %Y}<br>%{y:,.2f}<extra></extra>",
        )
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=30),
        height=420,
        hovermode="x unified",
        showlegend=False,
        plot_bgcolor="white",
        xaxis=dict(showgrid=False, showspikes=True, spikemode="across", spikethickness=1),
        yaxis=dict(title="Precio", gridcolor="#eee"),
    )
    return fig


@module.server
def page2_server(input, output, session):
    @reactive.calc
    def history() -> pd.Series:
        return get_history(input.ticker())

    @reactive.calc
    def info() -> dict:
        return get_info(input.ticker())

    @reactive.calc
    def five_years() -> pd.Series:
        s = history()
        if s.empty:
            return s
        return s.loc[s.index >= s.index[-1] - pd.DateOffset(years=HISTORY_YEARS)]

    @reactive.calc
    def selected_history() -> pd.Series:
        s = five_years()
        start, end = input.date_range()
        if s.empty or start is None or end is None:
            return s
        return s.loc[(s.index >= pd.Timestamp(start)) & (s.index <= pd.Timestamp(end))]

    @render.ui
    def subtitle():
        i, tk = info(), input.ticker()
        parts = [ASSETS[tk]["name"]]
        for k in ("sector", "category", "currency"):
            if i.get(k):
                parts.append(str(i[k]))
        return ui.p(" · ".join(parts), class_="text-muted pt-4")

    @render.ui
    def indicators():
        i, tk = info(), input.ticker()
        if not i:
            return ui.div(
                "No se pudieron obtener indicadores (Yahoo no respondió y no hay caché).",
                class_="alert alert-warning",
            )
        etf = is_etf(i, ASSETS[tk]["type"])
        items = etf_indicators(i) if etf else stock_indicators(i)
        boxes = [ui.value_box(t, v, ui.tags.small(n)) for t, v, n in items]
        note = (
            ui.p("Fondo/ETF: se muestran los equivalentes del fondo; ROE, ROIC y márgenes no aplican.",
                 class_="text-muted small")
            if etf else None
        )
        return ui.TagList(ui.layout_column_wrap(*boxes, width="200px", fill=False), note)

    @render_plotly
    def price_chart():
        s = selected_history()
        if s.empty:
            return go.Figure()
        return price_figure(s, input.ticker())
