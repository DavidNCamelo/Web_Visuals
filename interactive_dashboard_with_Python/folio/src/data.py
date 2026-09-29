"""Capa de datos: yfinance + caché en disco (/data)."""
from __future__ import annotations

import json
import time
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

from .config import HISTORY_YEARS, INFO_TTL_SECONDS, PRICE_TTL_SECONDS

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def _safe(ticker: str) -> str:
    return ticker.replace("/", "_")


def _fresh(path: Path, ttl: int) -> bool:
    return path.exists() and (time.time() - path.stat().st_mtime) < ttl


def get_history(ticker: str) -> pd.Series:
    """Serie de cierres ajustados (últimos HISTORY_YEARS años). Vacía si falla y no hay caché."""
    path = DATA_DIR / f"{_safe(ticker)}_prices.csv"
    if not _fresh(path, PRICE_TTL_SECONDS):
        try:
            start = date.today() - timedelta(days=365 * HISTORY_YEARS + 10)
            df = yf.Ticker(ticker).history(start=start.isoformat(), auto_adjust=True)
            if not df.empty:
                close = df["Close"].copy()
                close.index = pd.to_datetime(close.index).tz_localize(None).normalize()
                close.name = "Close"
                close.to_csv(path, index_label="Date")
        except Exception:
            pass  # cae a caché vieja si existe
    if not path.exists():
        return pd.Series(dtype=float, name="Close")
    s = pd.read_csv(path, index_col="Date", parse_dates=True)["Close"]
    return s.dropna().sort_index()


def get_info(ticker: str) -> dict:
    """Ticker.info cacheado (es lento y golpea a Yahoo). {} si falla y no hay caché."""
    path = DATA_DIR / f"{_safe(ticker)}_info.json"
    if not _fresh(path, INFO_TTL_SECONDS):
        try:
            info = yf.Ticker(ticker).info
            if info:
                path.write_text(json.dumps(info, default=str))
        except Exception:
            pass
    if not path.exists():
        return {}
    return json.loads(path.read_text())
