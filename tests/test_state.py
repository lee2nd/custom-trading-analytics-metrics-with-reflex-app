from unittest.mock import patch

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pytest

from custom_trading_analytics_metrics_with_reflex_app import state


def _sample_raw_df(n: int = 220) -> pd.DataFrame:
    idx = pd.date_range("2020-01-01", periods=n, freq="D")
    close = 100 + np.arange(n) * 0.1 + 2 * np.sin(np.arange(n) / 5)
    return pd.DataFrame(
        {
            "Open": close - 0.5,
            "High": close + 1.0,
            "Low": close - 1.0,
            "Close": close,
            "Volume": 1000 + np.arange(n),
        },
        index=idx,
    )


EXPECTED_KEYS = {"price_volume", "trend", "rsi_macd", "bollinger", "atr", "dashboard"}


def test_analyze_ticker_returns_all_six_figures():
    df = _sample_raw_df()

    result = state.analyze_ticker(df, "TEST")

    assert set(result.keys()) == EXPECTED_KEYS
    for figure in result.values():
        assert isinstance(figure, go.Figure)
        assert len(figure.data) > 0


def test_download_and_analyze_raises_on_empty_result():
    with patch.object(state.yf, "download", return_value=pd.DataFrame()):
        with pytest.raises(state.EmptyDataError):
            state._download_and_analyze("BADTICKER", "5y")


def test_download_and_analyze_success():
    df = _sample_raw_df()
    with patch.object(state.yf, "download", return_value=df):
        result = state._download_and_analyze("TEST", "5y")

    assert set(result.keys()) == EXPECTED_KEYS


def test_analyze_ticker_raises_on_insufficient_rows_for_sma_200():
    short_df = _sample_raw_df(n=60)

    with pytest.raises(state.EmptyDataError):
        state.analyze_ticker(short_df, "TEST")
