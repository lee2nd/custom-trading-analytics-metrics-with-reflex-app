"""Technical indicator calculations ported from us_stock_analysis.ipynb.

Pure functions only: no plotting, no I/O, no printing.
"""

import pandas as pd


def flatten_yfinance_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten yfinance's (field, ticker) MultiIndex columns down to just the field name."""
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = [col[0] for col in df.columns]
    return df


def add_sma_ema(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df with SMA_50, SMA_200, EMA_50, EMA_200 columns added."""
    df = df.copy()
    df["SMA_50"] = df["Close"].rolling(window=50).mean()
    df["SMA_200"] = df["Close"].rolling(window=200).mean()
    df["EMA_50"] = df["Close"].ewm(span=50, adjust=False).mean()
    df["EMA_200"] = df["Close"].ewm(span=200, adjust=False).mean()
    return df


def detect_crosses(df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """Return (golden_cross_mask, death_cross_mask) from SMA_50 crossing SMA_200."""
    sma_diff = df["SMA_50"] - df["SMA_200"]
    golden = (sma_diff > 0) & (sma_diff.shift(1) <= 0)
    death = (sma_diff < 0) & (sma_diff.shift(1) >= 0)
    return golden, death


def trend_alignment_masks(df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """Return (bullish_mask, bearish_mask) for Close vs SMA_50 vs SMA_200 ordering."""
    bullish = (df["Close"] > df["SMA_50"]) & (df["SMA_50"] > df["SMA_200"])
    bearish = (df["Close"] < df["SMA_50"]) & (df["SMA_50"] < df["SMA_200"])
    return bullish, bearish


def rsi(df: pd.DataFrame, n: int = 14) -> pd.Series:
    """Relative Strength Index over n periods."""
    change = df["Close"].diff()
    gain = change.where(change > 0, 0.0)
    loss = -change.where(change < 0, 0.0)
    avg_gain = gain.ewm(alpha=1 / n, min_periods=n).mean()
    avg_loss = loss.ewm(alpha=1 / n, min_periods=n).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def macd(df: pd.DataFrame, a: int = 12, b: int = 26, c: int = 9) -> pd.DataFrame:
    """Return a DataFrame with 'macd' and 'signal' columns."""
    ma_fast = df["Close"].ewm(span=a, min_periods=a).mean()
    ma_slow = df["Close"].ewm(span=b, min_periods=b).mean()
    macd_line = ma_fast - ma_slow
    signal_line = macd_line.ewm(span=c, min_periods=c).mean()
    return pd.DataFrame({"macd": macd_line, "signal": signal_line})


def bollinger_bands(df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """Return a copy of df with middle_band, upper_band, lower_band, BB_width columns added."""
    df = df.copy()
    df["middle_band"] = df["Close"].rolling(n).mean()
    rolling_std = df["Close"].rolling(n).std()
    df["upper_band"] = df["middle_band"] + (2 * rolling_std)
    df["lower_band"] = df["middle_band"] - (2 * rolling_std)
    df["BB_width"] = df["upper_band"] - df["lower_band"]
    return df


def atr(df: pd.DataFrame, n: int = 14) -> pd.DataFrame:
    """Return a copy of df with TR, ATR, ATR_pct columns added."""
    df = df.copy()
    df["H-L"] = df["High"] - df["Low"]
    df["H-PC"] = (df["High"] - df["Close"].shift(1)).abs()
    df["L-PC"] = (df["Low"] - df["Close"].shift(1)).abs()
    df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1)
    df["ATR"] = df["TR"].ewm(span=n, min_periods=n, adjust=False).mean()
    df["ATR_pct"] = df["ATR"] / df["Close"] * 100
    return df


def volume_sma(df: pd.DataFrame, n: int = 20) -> pd.Series:
    """n-period simple moving average of Volume, used as a baseline to judge 量增/量縮."""
    return df["Volume"].rolling(window=n).mean()


def buy_sell_probability(df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """Return (buy_prob, sell_prob) percentage Series from a 6-vote composite score."""
    s1 = (df["Close"] > df["SMA_50"]).astype(int) * 2 - 1
    s2 = (df["SMA_50"] > df["SMA_200"]).astype(int) * 2 - 1
    s3 = (df["EMA_50"] > df["EMA_200"]).astype(int) * 2 - 1
    s4 = (df["macd"] > df["signal"]).astype(int) * 2 - 1
    s5 = (df["rsi"] > 50).astype(int) * 2 - 1

    s6 = pd.Series(0, index=df.index)
    s6[df["Close"] < df["lower_band"]] = 1
    s6[df["Close"] > df["upper_band"]] = -1

    score = s1 + s2 + s3 + s4 + s5 + s6
    buy_prob = (score + 6) / 12 * 100
    sell_prob = 100 - buy_prob
    return buy_prob, sell_prob
