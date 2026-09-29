"""Servidor de la página 1."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from shiny import module, reactive, render, ui
from shinywidgets import render_plotly

from ..config import ASSETS, COLOR_DOWN, COLOR_UP, PERIODS
from ..data import get_history
from ..metrics import fmt_pct, fmt_price, variation
from ..theme import variation_cell_styles, variation_theme


def build_summary(history: dict[str, pd.Series]) -> pd.DataFrame:
    """Una fila por activo: último precio y variación en cada periodo (fracción)."""
    rows = []
    for tk, close in history.items():
        row = {"ticker": tk, "name": ASSETS[tk]["name"]}
        row["price"] = float(close.iloc[-1]) if len(close) else None
        row["asof"] = close.index[-1] if len(close) else None
        for key, _, offset in PERIODS:
            row[key] = variation(close, offset) if len(close) else None
        rows.append(row)
    return pd.DataFrame(rows)


def bar_figure(summary: pd.DataFrame, key: str) -> go.Figure:
    df = summary.dropna(subset=[key]).sort_values(key)
    colors = [COLOR_UP if v >= 0 else COLOR_DOWN for v in df[key]]
    fig = go.Figure(
        go.Bar(
            x=df[key] * 100,
            y=df["name"],
            orientation="h",
            marker_color=colors,
            text=[f"{v * 100:+.1f}%" for v in df[key]],
            textposition="outside",
            cliponaxis=False,
            hovertemplate="%{y}<br>%{x:+.2f}%<extra></extra>",
        )
    )
    lo, hi = min(0, df[key].min() * 100), max(0, df[key].max() * 100)
    pad = max((hi - lo) * 0.18, 0.5)  # aire para las etiquetas fuera de la barra
    fig.update_layout(
        margin=dict(l=10, r=40, t=10, b=30),
        height=340,
        xaxis=dict(title="Variación (%)", range=[lo - (pad if lo < 0 else 0), hi + (pad if hi > 0 else 0)], zeroline=True, zerolinecolor="#999", gridcolor="#eee"),
        yaxis=dict(title=None),
        plot_bgcolor="white",
        showlegend=False,
    )
    return fig


@module.server
def page1_server(input, output, session):
    @reactive.calc
    def summary() -> pd.DataFrame:
        with ui.Progress(min=0, max=len(ASSETS)) as p:
            p.set(message="Descargando precios…")
            hist = {}
            for i, tk in enumerate(ASSETS, 1):
                hist[tk] = get_history(tk)
                p.set(i)
        return build_summary(hist)

    @render.ui
    def cards():
        df = summary()
        boxes = []
        for _, r in df.iterrows():
            d = r["d"]
            arrow = "" if d is None or pd.isna(d) else ("▲ " if d >= 0 else "▼ ")
            is_up = None if d is None or pd.isna(d) else d >= 0
            boxes.append(
                ui.value_box(
                    r["ticker"],
                    fmt_price(r["price"]),
                    ui.tags.small(f"{arrow}{fmt_pct(d, 2, signed=True)} hoy · {r['name']}"),
                    theme=variation_theme(is_up),
                )
            )
        return ui.layout_columns(*boxes, col_widths=[2, 2, 2, 3, 3] if len(boxes) == 5 else None)

    def _make_outputs(key: str, label: str):
        @output(id=f"bar_{key}")
        @render_plotly
        def _bar():
            return bar_figure(summary(), key)

        @output(id=f"table_{key}")
        @render.data_frame
        def _table():
            df = summary()[["ticker", "name", "price", key]].copy()
            df = df.sort_values(key, ascending=False, na_position="last")
            return render.DataGrid(
                pd.DataFrame(
                    {
                        "Ticker": df["ticker"],
                        "Activo": df["name"],
                        "Precio": [fmt_price(v) for v in df["price"]],
                        label: [fmt_pct(v, 2, signed=True) for v in df[key]],
                    }
                ),
                width="100%",
                styles=variation_cell_styles(df[key].tolist(), col_index=3),
            )

    for key, label, _ in PERIODS:
        _make_outputs(key, label)
