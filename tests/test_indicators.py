import pandas as pd
import pytest

from custom_trading_analytics_metrics_with_reflex_app import indicators


def test_flatten_yfinance_columns_collapses_multiindex():
    columns = pd.MultiIndex.from_tuples([("Close", "GOOGL"), ("Volume", "GOOGL")])
    df = pd.DataFrame([[100.0, 1000]], columns=columns)

    result = indicators.flatten_yfinance_columns(df)

    assert list(result.columns) == ["Close", "Volume"]


def test_flatten_yfinance_columns_passthrough_for_regular_index():
    df = pd.DataFrame({"Close": [100.0], "Volume": [1000]})

    result = indicators.flatten_yfinance_columns(df)

    assert list(result.columns) == ["Close", "Volume"]


def test_add_sma_ema_arithmetic_sequence():
    df = pd.DataFrame({"Close": pd.Series(range(1, 221), dtype=float)})

    result = indicators.add_sma_ema(df)

    assert result["SMA_50"].iloc[:49].isna().all()
    assert result["SMA_50"].iloc[49] == pytest.approx(25.5)  # mean(1..50)
    assert result["SMA_50"].iloc[-1] == pytest.approx(195.5)  # mean(171..220)
    assert result["SMA_200"].iloc[-1] == pytest.approx(120.5)  # mean(21..220)


def test_add_sma_ema_flat_series_gives_constant_ema():
    df = pd.DataFrame({"Close": pd.Series([100.0] * 60)})

    result = indicators.add_sma_ema(df)

    assert result["EMA_50"].round(6).eq(100.0).all()


def test_detect_crosses():
    df = pd.DataFrame({
        "Close": [1, 2, 3, 4, 5],
        "SMA_50": [1, 1, 3, 3, 5],
        "SMA_200": [2, 2, 2, 4, 4],
    })

    golden, death = indicators.detect_crosses(df)

    assert golden.tolist() == [False, False, True, False, True]
    assert death.tolist() == [False, False, False, True, False]


def test_trend_alignment_masks():
    df = pd.DataFrame({
        "Close": [10, 5, 3, 10],
        "SMA_50": [8, 8, 5, 10],
        "SMA_200": [6, 6, 8, 5],
    })

    bullish, bearish = indicators.trend_alignment_masks(df)

    assert bullish.tolist() == [True, False, False, False]
    assert bearish.tolist() == [False, False, True, False]


def test_rsi_is_100_for_strictly_increasing_prices():
    df = pd.DataFrame({"Close": pd.Series(range(1, 30), dtype=float)})

    result = indicators.rsi(df, n=14)

    assert result.iloc[-1] == pytest.approx(100.0)


def test_rsi_is_0_for_strictly_decreasing_prices():
    df = pd.DataFrame({"Close": pd.Series(range(30, 1, -1), dtype=float)})

    result = indicators.rsi(df, n=14)

    assert result.iloc[-1] == pytest.approx(0.0)


def test_macd_is_zero_for_flat_prices():
    df = pd.DataFrame({"Close": pd.Series([50.0] * 40)})

    result = indicators.macd(df)

    assert result["macd"].iloc[-1] == pytest.approx(0.0, abs=1e-9)
    assert result["signal"].iloc[-1] == pytest.approx(0.0, abs=1e-9)


def test_bollinger_bands_zero_width_for_flat_prices():
    df = pd.DataFrame({"Close": pd.Series([100.0] * 25)})

    result = indicators.bollinger_bands(df, n=20)

    assert result["middle_band"].iloc[-1] == pytest.approx(100.0)
    assert result["upper_band"].iloc[-1] == pytest.approx(100.0)
    assert result["lower_band"].iloc[-1] == pytest.approx(100.0)
    assert result["BB_width"].iloc[-1] == pytest.approx(0.0)


def test_atr_is_zero_when_no_range_and_no_price_change():
    df = pd.DataFrame({
        "High": [100.0] * 20,
        "Low": [100.0] * 20,
        "Close": [100.0] * 20,
    })

    result = indicators.atr(df, n=14)

    assert result["ATR"].iloc[-1] == pytest.approx(0.0)
    assert result["ATR_pct"].iloc[-1] == pytest.approx(0.0)


def test_buy_sell_probability_all_bullish_votes():
    df = pd.DataFrame({
        "Close": [110.0],
        "SMA_50": [100.0],
        "SMA_200": [90.0],
        "EMA_50": [105.0],
        "EMA_200": [95.0],
        "macd": [1.0],
        "signal": [0.0],
        "rsi": [60.0],
        "lower_band": [80.0],
        "upper_band": [120.0],
    })

    buy_prob, sell_prob = indicators.buy_sell_probability(df)

    assert buy_prob.iloc[0] == pytest.approx(91.666667)
    assert sell_prob.iloc[0] == pytest.approx(8.333333)
