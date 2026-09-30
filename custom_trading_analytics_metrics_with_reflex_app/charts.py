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
    """ATR (price units) on the primary axis and ATR% (relative volatility) on a secondary axis."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=df.index, y=df["ATR"], name="ATR",
            line={"color": "#2563eb", "width": 2},
            fill="tozeroy", fillcolor="rgba(37, 99, 235, 0.08)",
            hovertemplate="ATR：%{y:.2f}<extra></extra>",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df["ATR_pct"], name="ATR%",
            line={"color": "#f59e0b", "width": 1.5, "dash": "dot"},
            hovertemplate="ATR%%：%{y:.2f}%%<extra></extra>",
        ),
        secondary_y=True,
    )

    fig.update_yaxes(
        title_text="ATR（價格單位）", secondary_y=False,
        showgrid=True, gridcolor="rgba(15, 23, 42, 0.06)", zeroline=False,
    )
    fig.update_yaxes(title_text="ATR%（%）", secondary_y=True, showgrid=False, zeroline=False)
    fig.update_xaxes(showgrid=False)

    fig.update_layout(
        title="平均真實波幅 Average True Range（ATR）",
        template="plotly_white",
        height=460,
        hovermode="x unified",
        font={"family": "Inter, -apple-system, sans-serif", "size": 13, "color": "#374151"},
        legend={"orientation": "h", "yanchor": "top", "y": -0.15, "xanchor": "center", "x": 0.5},
        margin={"t": 56, "l": 60, "r": 60, "b": 60},
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    return fig


def build_dashboard_figure(df, ticker: str) -> go.Figure:
    """Combined 5-row technical analysis view: Price+BB+crosses, Volume, RSI, MACD, ATR."""
    golden_mask, death_mask = indicators.detect_crosses(df)
    bullish_mask, bearish_mask = indicators.trend_alignment_masks(df)
    buy_prob, sell_prob = indicators.buy_sell_probability(df)

    latest_buy = buy_prob.iloc[-1]
    latest_sell = sell_prob.iloc[-1]

    vol_ratio = df["Volume"] / df["Volume_SMA_20"]
    latest_vol_ratio = vol_ratio.iloc[-1]
    vol_state = "量增" if latest_vol_ratio >= 1 else "量縮"
    vol_color = "#16a34a" if latest_vol_ratio >= 1 else "#dc2626"

    fig = make_subplots(
        rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.04,
        row_heights=[0.38, 0.1, 0.16, 0.16, 0.16],
        subplot_titles=(
            f"{ticker} 價格與均線走勢　"
            f"<span style='color:#16a34a'>看多 {latest_buy:.0f}%</span>／"
            f"<span style='color:#dc2626'>看空 {latest_sell:.0f}%</span>",
            f"成交量　<span style='color:{vol_color}'>{vol_state} （現量為 20 日均量的 {latest_vol_ratio * 100:.0f}%）</span>",
            "RSI（相對強弱指標）", "MACD", "ATR（波動幅度）",
        ),
    )

    for x0, x1 in _mask_to_ranges(bullish_mask):
        fig.add_shape(type="rect", x0=x0, x1=x1, y0=0, y1=1, xref="x", yref="y domain",
                      fillcolor="#16a34a", opacity=0.08, line_width=0, layer="below", row=1, col=1)
    for x0, x1 in _mask_to_ranges(bearish_mask):
        fig.add_shape(type="rect", x0=x0, x1=x1, y0=0, y1=1, xref="x", yref="y domain",
                      fillcolor="#dc2626", opacity=0.08, line_width=0, layer="below", row=1, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df["upper_band"], name="布林上軌", showlegend=False,
                              line={"width": 1, "color": "rgba(148,163,184,0.8)"}, hoverinfo="skip"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["lower_band"], name="布林下軌", showlegend=False,
                              line={"width": 1, "color": "rgba(148,163,184,0.8)"}, fill="tonexty",
                              fillcolor="rgba(148,163,184,0.12)", hoverinfo="skip"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["middle_band"], name="布林中軌", showlegend=False,
                              line={"width": 1, "color": "#94a3b8", "dash": "dot"}), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="收盤價", line={"color": "#111827", "width": 1.5}), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA_50"], name="SMA 50", line={"color": "#2563eb", "width": 1}), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA_200"], name="SMA 200", line={"color": "#7c3aed", "width": 1}), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA_50"], name="EMA 50", showlegend=False,
                              line={"color": "#2563eb", "width": 1, "dash": "dash"}), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA_200"], name="EMA 200", showlegend=False,
                              line={"color": "#7c3aed", "width": 1, "dash": "dash"}), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index[golden_mask], y=df.loc[golden_mask, "SMA_50"], name="黃金交叉",
                              mode="markers", marker={"symbol": "triangle-up", "size": 11, "color": "#16a34a"}),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index[death_mask], y=df.loc[death_mask, "SMA_50"], name="死亡交叉",
                              mode="markers", marker={"symbol": "triangle-down", "size": 11, "color": "#dc2626"}),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
                              marker={"size": 12, "symbol": "square", "color": "rgba(22,163,74,0.25)"},
                              name="多頭排列"), row=1, col=1)
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
                              marker={"size": 12, "symbol": "square", "color": "rgba(220,38,38,0.25)"},
                              name="空頭排列"), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df["Close"], name="買賣訊號機率", mode="lines",
        line={"width": 0}, opacity=0, showlegend=False,
        customdata=list(zip(buy_prob, sell_prob)),
        hovertemplate="看多機率：%{customdata[0]:.0f}% ／看空機率：%{customdata[1]:.0f}%<extra></extra>",
    ), row=1, col=1)

    volume_colors = ["#16a34a" if c >= o else "#dc2626" for o, c in zip(df["Open"], df["Close"])]
    fig.add_trace(go.Bar(
        x=df.index, y=df["Volume"], name="成交量",
        marker_color=volume_colors, opacity=0.55,
        customdata=vol_ratio, hovertemplate="成交量：%{y:,.0f}<br>為 20 日均量的 %{customdata:.0%}<extra></extra>",
    ), row=2, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df["Volume_SMA_20"], name="20日均量",
        line={"color": "#111827", "width": 1.2, "dash": "dot"},
        hovertemplate="20日均量：%{y:,.0f}<extra></extra>",
    ), row=2, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df["rsi"], name="RSI", line={"color": "#7c3aed", "width": 1.5}), row=3, col=1)
    for level, color in [(70, "#dc2626"), (50, "#9ca3af"), (30, "#16a34a")]:
        fig.add_hline(y=level, line_dash="dash", line_color=color, line_width=1, row=3, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df["macd"], name="MACD", line={"color": "#2563eb", "width": 1.5}), row=4, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["signal"], name="訊號線", line={"color": "#f59e0b", "width": 1.5}), row=4, col=1)
    macd_hist = df["macd"] - df["signal"]
    hist_colors = ["#16a34a" if v >= 0 else "#dc2626" for v in macd_hist]
    fig.add_trace(go.Bar(x=df.index, y=macd_hist, name="柱狀圖",
                          marker_color=hist_colors, opacity=0.5), row=4, col=1)
    fig.add_hline(y=0, line_dash="dash", line_color="#9ca3af", line_width=1, row=4, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df["ATR"], name="ATR", line={"color": "#2563eb", "width": 1.5},
                              fill="tozeroy", fillcolor="rgba(37,99,235,0.06)"), row=5, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["ATR_pct"], name="ATR%",
                              line={"color": "#f59e0b", "width": 1.2, "dash": "dot"}), row=5, col=1)

    fig.update_yaxes(title_text="價格", row=1, col=1, showgrid=True, gridcolor="rgba(15,23,42,0.05)", zeroline=False)
    fig.update_yaxes(title_text="成交量", row=2, col=1, showgrid=False, zeroline=False)
    fig.update_yaxes(title_text="RSI", row=3, col=1, showgrid=True, gridcolor="rgba(15,23,42,0.05)", zeroline=False)
    fig.update_yaxes(title_text="MACD", row=4, col=1, showgrid=True, gridcolor="rgba(15,23,42,0.05)", zeroline=False)
    fig.update_yaxes(title_text="ATR", row=5, col=1, showgrid=True, gridcolor="rgba(15,23,42,0.05)", zeroline=False)
    fig.update_xaxes(title_text="日期", row=5, col=1)
    fig.update_xaxes(showgrid=False)

    fig.update_layout(
        height=1500,
        hovermode="x unified",
        template="plotly_white",
        font={"family": "Inter, -apple-system, sans-serif", "size": 12, "color": "#374151"},
        legend={
            "orientation": "h", "yanchor": "bottom", "y": 1.03, "xanchor": "center", "x": 0.5,
            "font": {"size": 11},
        },
        margin={"t": 130, "l": 60, "r": 60, "b": 60},
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    return fig
