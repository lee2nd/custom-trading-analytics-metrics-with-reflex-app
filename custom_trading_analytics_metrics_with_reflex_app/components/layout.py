import reflex as rx

from ..state import AppState
from .controls import controls


def _tab(value: str, label: str, figure) -> rx.Component:
    return rx.tabs.content(rx.plotly(data=figure, width="100%"), value=value)


def layout() -> rx.Component:
    return rx.vstack(
        rx.heading("交易分析儀表板", size="6"),
        controls(),
        rx.cond(
            AppState.error != "",
            rx.callout(AppState.error, color_scheme="red"),
        ),
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Price & Volume", value="price_volume"),
                rx.tabs.trigger("SMA / EMA", value="trend"),
                rx.tabs.trigger("RSI / MACD", value="rsi_macd"),
                rx.tabs.trigger("Bollinger Bands", value="bollinger"),
                rx.tabs.trigger("ATR", value="atr"),
                rx.tabs.trigger("Dashboard", value="dashboard"),
            ),
            _tab("price_volume", "Price & Volume", AppState.price_volume_figure),
            _tab("trend", "SMA / EMA", AppState.trend_figure),
            _tab("rsi_macd", "RSI / MACD", AppState.rsi_macd_figure),
            _tab("bollinger", "Bollinger Bands", AppState.bollinger_figure),
            _tab("atr", "ATR", AppState.atr_figure),
            _tab("dashboard", "Dashboard", AppState.dashboard_figure),
            default_value="price_volume",
        ),
        width="100%",
        padding="2em",
        spacing="4",
    )
