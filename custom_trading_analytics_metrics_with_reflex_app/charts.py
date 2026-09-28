"""Plotly figure builders ported from us_stock_analysis.ipynb.

Each build_* function takes an indicator-enriched DataFrame and returns a
standalone go.Figure. No I/O, no fig.show().
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from . import indicators


def _mask_to_ranges(mask) -> list[tuple]:
    """Convert a boolean Series into a list of (start, end) index ranges for contiguous True runs."""
    ranges = []
    idx = mask.index
    start = None
    for i, val in enumerate(mask.to_numpy()):
        if val and start is None:
            start = idx[i]
        elif not val and start is not None:
            ranges.append((start, idx[i - 1]))
            start = None
    if start is not None:
        ranges.append((start, idx[-1]))
    return ranges


def build_price_volume_figure(df, ticker: str) -> go.Figure:
    """2-row subplot: Close price line (top) and Volume bars (bottom)."""
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        row_heights=[0.7, 0.3], vertical_spacing=0.05,
        subplot_titles=(f"{ticker} Price", "Volume"),
    )
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close"), row=1, col=1)
    fig.add_trace(go.Bar(x=df.index, y=df["Volume"], name="Volume"), row=2, col=1)
    fig.update_layout(template="plotly_white", height=700)
    return fig


def build_trend_figure(df, ticker: str) -> go.Figure:
    """Close/SMA/EMA lines with bullish/bearish shading and Golden/Death Cross markers."""
    golden_mask, death_mask = indicators.detect_crosses(df)
    bullish_mask, bearish_mask = indicators.trend_alignment_masks(df)

    fig = go.Figure()

    for x0, x1 in _mask_to_ranges(bullish_mask):
        fig.add_shape(
            type="rect", x0=x0, x1=x1, y0=0, y1=1, xref="x", yref="y domain",
            fillcolor="green", opacity=0.08, line_width=0, layer="below",
        )
    for x0, x1 in _mask_to_ranges(bearish_mask):
        fig.add_shape(
            type="rect", x0=x0, x1=x1, y0=0, y1=1, xref="x", yref="y domain",
            fillcolor="red", opacity=0.08, line_width=0, layer="below",
        )

    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close"))
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA_50"], name="SMA 50"))
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA_200"], name="SMA 200"))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA_50"], name="EMA 50", line={"dash": "dash"}))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA_200"], name="EMA 200", line={"dash": "dash"}))
    fig.add_trace(go.Scatter(
        x=df.index[golden_mask], y=df.loc[golden_mask, "SMA_50"], name="Golden Cross",
        mode="markers", marker={"symbol": "triangle-up", "size": 12, "color": "green"},
    ))
    fig.add_trace(go.Scatter(
        x=df.index[death_mask], y=df.loc[death_mask, "SMA_50"], name="Death Cross",
        mode="markers", marker={"symbol": "triangle-down", "size": 12, "color": "red"},
    ))

    fig.update_layout(
        title=f"{ticker} Price with SMA, EMA & Golden/Death Cross",
        template="plotly_white", height=600,
    )
    return fig


def build_rsi_macd_figure(df, ticker: str) -> go.Figure:
    """2-row subplot: RSI with overbought/oversold lines, MACD with signal and histogram."""
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        row_heights=[0.5, 0.5], vertical_spacing=0.08,
        subplot_titles=("RSI (14)", "MACD (12, 26, 9)"),
    )
    fig.add_trace(go.Scatter(x=df.index, y=df["rsi"], name="RSI", line={"color": "purple"}), row=1, col=1)
    for level, color in [(70, "red"), (30, "green")]:
        fig.add_hline(y=level, line_dash="dash", line_color=color, row=1, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df["macd"], name="MACD", line={"color": "blue"}), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["signal"], name="Signal", line={"color": "orange"}), row=2, col=1)
    fig.add_trace(go.Bar(x=df.index, y=df["macd"] - df["signal"], name="Histogram", opacity=0.4), row=2, col=1)
    fig.add_hline(y=0, line_dash="dash", row=2, col=1)

    fig.update_layout(template="plotly_white", height=700)
    return fig


def build_bollinger_figure(df, ticker: str) -> go.Figure:
    """Close price with upper/middle/lower Bollinger Bands and a shaded band area."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df["upper_band"], name="BB Upper",
        line={"width": 1, "color": "lightgrey"}, hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=df.index, y=df["lower_band"], name="BB Lower",
        line={"width": 1, "color": "lightgrey"}, fill="tonexty",
        fillcolor="rgba(200,200,200,0.2)", hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=df.index, y=df["middle_band"], name="BB Middle",
        line={"width": 1, "color": "grey", "dash": "dot"},
    ))
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close", line={"color": "black"}))

    fig.update_layout(title=f"{ticker} Bollinger Bands", template="plotly_white", height=600)
    return fig


def build_atr_figure(df, ticker: str) -> go.Figure:
    """ATR and ATR% lines."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["ATR"], name="ATR", line={"color": "brown"}))
    fig.add_trace(go.Scatter(x=df.index, y=df["ATR_pct"], name="ATR%", line={"color": "teal", "dash": "dash"}))

    fig.update_layout(title=f"{ticker} Average True Range (ATR)", template="plotly_white", height=500)
    return fig


def build_dashboard_figure(df, ticker: str) -> go.Figure:
    """Combined 5-row dashboard: Price+BB+crosses, Volume, RSI, MACD, ATR."""
    golden_mask, death_mask = indicators.detect_crosses(df)
    bullish_mask, bearish_mask = indicators.trend_alignment_masks(df)
    buy_prob, sell_prob = indicators.buy_sell_probability(df)

    latest_buy = buy_prob.iloc[-1]
    latest_sell = sell_prob.iloc[-1]

    fig = make_subplots(
        rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.03,
        row_heights=[0.4, 0.12, 0.16, 0.16, 0.16],
        subplot_titles=(
            f"{ticker} Price & Moving Averages (Latest: Buy {latest_buy:.0f}% / Sell {latest_sell:.0f}%)",
            "Volume", "RSI", "MACD", "ATR",
        ),
    )

    for x0, x1 in _mask_to_ranges(bullish_mask):
        fig.add_shape(type="rect", x0=x0, x1=x1, y0=0, y1=1, xref="x", yref="y domain",
                      fillcolor="green", opacity=0.12, line_width=0, layer="above", row=1, col=1)
    for x0, x1 in _mask_to_ranges(bearish_mask):
        fig.add_shape(type="rect", x0=x0, x1=x1, y0=0, y1=1, xref="x", yref="y domain",
                      fillcolor="red", opacity=0.12, line_width=0, layer="above", row=1, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df["upper_band"], name="BB Upper",
                              line={"width": 1, "color": "lightgrey"}, hoverinfo="skip"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["lower_band"], name="BB Lower",
                              line={"width": 1, "color": "lightgrey"}, fill="tonexty",
                              fillcolor="rgba(200,200,200,0.2)", hoverinfo="skip"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["middle_band"], name="BB Middle",
                              line={"width": 1, "color": "grey", "dash": "dot"}), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close", line={"color": "black"}), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA_50"], name="SMA 50", line={"width": 1}), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA_200"], name="SMA 200", line={"width": 1}), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA_50"], name="EMA 50",
                              line={"width": 1, "dash": "dash"}), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA_200"], name="EMA 200",
                              line={"width": 1, "dash": "dash"}), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index[golden_mask], y=df.loc[golden_mask, "SMA_50"], name="Golden Cross",
                              mode="markers", marker={"symbol": "triangle-up", "size": 12, "color": "green"}),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index[death_mask], y=df.loc[death_mask, "SMA_50"], name="Death Cross",
                              mode="markers", marker={"symbol": "triangle-down", "size": 12, "color": "red"}),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
                              marker={"size": 12, "symbol": "square", "color": "rgba(0,128,0,0.3)"},
                              name="多頭排列 (Close > SMA50 > SMA200)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
                              marker={"size": 12, "symbol": "square", "color": "rgba(220,0,0,0.3)"},
                              name="空頭排列 (Close < SMA50 < SMA200)"), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df["Close"], name="Buy/Sell Probability", mode="lines",
        line={"width": 0}, opacity=0, showlegend=False,
        customdata=list(zip(buy_prob, sell_prob)),
        hovertemplate="Buy Prob: %{customdata[0]:.0f}% / Sell Prob: %{customdata[1]:.0f}%<extra></extra>",
    ), row=1, col=1)

    fig.add_trace(go.Bar(x=df.index, y=df["Volume"], name="Volume", marker_color="steelblue"), row=2, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df["rsi"], name="RSI", line={"color": "purple"}), row=3, col=1)
    for level, color in [(70, "red"), (50, "gray"), (30, "green")]:
        fig.add_hline(y=level, line_dash="dash", line_color=color, row=3, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df["macd"], name="MACD", line={"color": "blue"}), row=4, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["signal"], name="Signal", line={"color": "orange"}), row=4, col=1)
    fig.add_trace(go.Bar(x=df.index, y=df["macd"] - df["signal"], name="Histogram",
                          marker_color="grey", opacity=0.4), row=4, col=1)
    fig.add_hline(y=0, line_dash="dash", line_color="black", row=4, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df["ATR"], name="ATR", line={"color": "brown"}), row=5, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["ATR_pct"], name="ATR%",
                              line={"color": "teal", "dash": "dash"}), row=5, col=1)

    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_yaxes(title_text="RSI", row=3, col=1)
    fig.update_yaxes(title_text="MACD", row=4, col=1)
    fig.update_yaxes(title_text="ATR", row=5, col=1)
    fig.update_xaxes(title_text="Date", row=5, col=1)

    fig.update_layout(
        height=1600,
        hovermode="x unified",
        template="plotly_white",
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.04, "xanchor": "center", "x": 0.5},
        margin={"t": 130, "l": 60, "r": 60, "b": 60},
    )
    return fig
