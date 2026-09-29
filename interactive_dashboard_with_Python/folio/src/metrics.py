"""Cálculos puros (sin red): variaciones y formato de indicadores."""
from __future__ import annotations

import math

import pandas as pd


def variation(close: pd.Series, offset: dict) -> float | None:
    """Variación porcentual del último cierre frente al cierre a `offset` atrás.

    offset = {"days": 1}   -> cierre anterior (sesión previa)
    offset = {"months": n} -> último cierre en o antes de (última fecha - n meses)
    Devuelve una fracción (0.05 = +5 %) o None si no hay historia suficiente.
    """
    close = close.dropna()
    if len(close) < 2:
        return None
    last = close.iloc[-1]
    if "days" in offset:
        base = close.iloc[-1 - offset["days"]] if len(close) > offset["days"] else None
    else:
        target = close.index[-1] - pd.DateOffset(**offset)
        if close.index[0] > target:
            return None  # la serie no llega tan atrás
        base = close.loc[:target].iloc[-1]
    if base is None or base == 0:
        return None
    return float(last / base - 1)


def _ok(x) -> bool:
    return x is not None and not (isinstance(x, float) and math.isnan(x))


def fmt_pct(x, digits: int = 1, signed: bool = False) -> str:
    if not _ok(x):
        return "—"
    return f"{x * 100:+.{digits}f}%" if signed else f"{x * 100:.{digits}f}%"


def fmt_x(x, digits: int = 1) -> str:
    return f"{x:.{digits}f}x" if _ok(x) else "—"


def fmt_price(x, currency: str | None = None) -> str:
    if not _ok(x):
        return "—"
    return f"{x:,.2f} {currency}" if currency else f"{x:,.2f}"


def fmt_big(x) -> str:
    if not _ok(x):
        return "—"
    for unit, div in (("B", 1e9), ("M", 1e6)):
        if abs(x) >= div:
            return f"{x / div:,.1f}{unit}"
    return f"{x:,.0f}"


def dividend_yield(info: dict) -> float | None:
    """Rendimiento por dividendo como fracción, robusto a cambios de escala en yfinance."""
    rate = info.get("dividendRate")
    px = info.get("currentPrice") or info.get("regularMarketPrice")
    if _ok(rate) and _ok(px) and px:
        return rate / px
    y = info.get("yield")  # ETFs: ya es fracción
    if _ok(y):
        return y
    y = info.get("dividendYield")  # yfinance >= 0.2.54: viene en porcentaje
    return y / 100 if _ok(y) else None


def expense_ratio(info: dict) -> float | None:
    v = info.get("netExpenseRatio")  # en porcentaje (0.03 = 0.03 %)
    if _ok(v):
        return v / 100
    v = info.get("annualReportExpenseRatio")  # fracción
    return v if _ok(v) else None


def is_etf(info: dict, fallback: str = "stock") -> bool:
    qt = (info.get("quoteType") or "").upper()
    if qt:
        return qt in {"ETF", "MUTUALFUND"}
    return fallback == "etf"
