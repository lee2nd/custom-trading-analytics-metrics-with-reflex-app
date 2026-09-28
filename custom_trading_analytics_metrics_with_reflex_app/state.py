"""Reflex state for the trading analytics dashboard."""

import asyncio
import logging

import plotly.express as px
import plotly.graph_objects as go
import reflex as rx
import yfinance as yf

from . import charts, indicators

logger = logging.getLogger(__name__)

PERIOD_OPTIONS = ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"]


class EmptyDataError(Exception):
    """Raised when yfinance returns no data for the requested ticker."""


def analyze_ticker(df, ticker: str) -> dict[str, go.Figure]:
    """Compute all indicators and build all chart figures for a raw OHLCV DataFrame."""
    df = indicators.flatten_yfinance_columns(df)
    df = indicators.add_sma_ema(df)
    df["rsi"] = indicators.rsi(df)
    macd_df = indicators.macd(df)
    df["macd"] = macd_df["macd"]
    df["signal"] = macd_df["signal"]
    df = indicators.bollinger_bands(df)
    df = indicators.atr(df)
    df = df.dropna()
    if df.empty:
        raise EmptyDataError(
            f"「{ticker}」在所選期間的資料筆數不足以計算所有技術指標（需要至少 200 個交易日），請選擇更長的期間。"
        )

    return {
        "price_volume": charts.build_price_volume_figure(df, ticker),
        "trend": charts.build_trend_figure(df, ticker),
        "rsi_macd": charts.build_rsi_macd_figure(df, ticker),
        "bollinger": charts.build_bollinger_figure(df, ticker),
        "atr": charts.build_atr_figure(df, ticker),
        "dashboard": charts.build_dashboard_figure(df, ticker),
    }


def _download_and_analyze(ticker: str, period: str) -> dict[str, go.Figure]:
    """Blocking helper: download from yfinance and run the full analysis pipeline."""
    df = yf.download(ticker, period=period)
    if df is None or df.empty:
        raise EmptyDataError(f"找不到「{ticker}」的資料，請確認代號是否正確。")
    return analyze_ticker(df, ticker)


def _empty_figure() -> go.Figure:
    return px.line()


class AppState(rx.State):
    ticker_input: str = "GOOGL"
    period: str = "5y"
    is_loading: bool = False
    error: str = ""

    price_volume_figure: go.Figure = _empty_figure()
    trend_figure: go.Figure = _empty_figure()
    rsi_macd_figure: go.Figure = _empty_figure()
    bollinger_figure: go.Figure = _empty_figure()
    atr_figure: go.Figure = _empty_figure()
    dashboard_figure: go.Figure = _empty_figure()

    @rx.event
    def set_ticker_input(self, value: str):
        self.ticker_input = value

    @rx.event
    def set_period(self, value: str):
        self.period = value

    @rx.event
    def submit(self):
        ticker = self.ticker_input.strip().upper()
        if not ticker:
            self.error = "請輸入股票代號"
            return
        self.ticker_input = ticker
        self.error = ""
        self.is_loading = True
        return AppState.fetch_and_analyze

    @rx.event(background=True)
    async def fetch_and_analyze(self):
        async with self:
            ticker = self.ticker_input
            period = self.period

        try:
            figures = await asyncio.to_thread(_download_and_analyze, ticker, period)
        except EmptyDataError as exc:
            async with self:
                self.error = str(exc)
            return
        except Exception:  # network / yfinance failures
            logger.exception(
                "fetch_and_analyze failed for ticker=%s period=%s", ticker, period
            )
            async with self:
                self.error = "抓取資料時發生錯誤，請稍後再試。"
            return
        else:
            async with self:
                self.price_volume_figure = figures["price_volume"]
                self.trend_figure = figures["trend"]
                self.rsi_macd_figure = figures["rsi_macd"]
                self.bollinger_figure = figures["bollinger"]
                self.atr_figure = figures["atr"]
                self.dashboard_figure = figures["dashboard"]
        finally:
            async with self:
                self.is_loading = False
