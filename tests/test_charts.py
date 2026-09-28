import pandas as pd
import plotly.graph_objects as go
import pytest

from custom_trading_analytics_metrics_with_reflex_app import charts, indicators


def _sample_df(n: int = 220) -> pd.DataFrame:
    import numpy as np

    idx = pd.date_range("2020-01-01", periods=n, freq="D")
    close = 100 + np.arange(n) * 0.1 + 2 * np.sin(np.arange(n) / 5)
    df = pd.DataFrame(
        {
            "Open": close - 0.5,
            "High": close + 1.0,
            "Low": close - 1.0,
            "Close": close,
            "Volume": 1000 + np.arange(n),
        },
        index=idx,
    )
    df = indicators.add_sma_ema(df)
    df["rsi"] = indicators.rsi(df)
    macd_df = indicators.macd(df)
    df["macd"] = macd_df["macd"]
    df["signal"] = macd_df["signal"]
    df = indicators.bollinger_bands(df)
    df = indicators.atr(df)
    return df.dropna()


def test_build_price_volume_figure_has_two_traces():
    df = _sample_df()

    fig = charts.build_price_volume_figure(df, "TEST")

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 2
    names = [trace.name for trace in fig.data]
    assert "Close" in names
    assert "Volume" in names


def test_build_trend_figure_has_seven_traces():
    df = _sample_df()

    fig = charts.build_trend_figure(df, "TEST")

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 7
    names = {trace.name for trace in fig.data}
    assert names == {
        "Close", "SMA 50", "SMA 200", "EMA 50", "EMA 200",
        "Golden Cross", "Death Cross",
    }


def test_build_rsi_macd_figure_has_four_traces():
    df = _sample_df()

    fig = charts.build_rsi_macd_figure(df, "TEST")

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 4
    names = {trace.name for trace in fig.data}
    assert names == {"RSI", "MACD", "Signal", "Histogram"}


def test_build_bollinger_figure_has_four_traces():
    df = _sample_df()

    fig = charts.build_bollinger_figure(df, "TEST")

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 4
    names = {trace.name for trace in fig.data}
    assert names == {"Close", "BB Upper", "BB Middle", "BB Lower"}


def test_build_atr_figure_has_two_traces():
    df = _sample_df()

    fig = charts.build_atr_figure(df, "TEST")

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 2
    names = {trace.name for trace in fig.data}
    assert names == {"ATR", "ATR%"}


def test_build_dashboard_figure_has_twenty_traces_and_five_rows():
    df = _sample_df()

    fig = charts.build_dashboard_figure(df, "TEST")

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 20
    yaxes = [key for key in fig.layout if key.startswith("yaxis")]
    assert len(yaxes) == 5
