import reflex as rx

from ..state import PERIOD_OPTIONS, AppState


def controls() -> rx.Component:
    return rx.hstack(
        rx.input(
            placeholder="輸入股票代號，例如 GOOGL",
            value=AppState.ticker_input,
            on_change=AppState.set_ticker_input,
            width="200px",
        ),
        rx.select(
            PERIOD_OPTIONS,
            value=AppState.period,
            on_change=AppState.set_period,
            width="120px",
        ),
        rx.button(
            "查詢",
            on_click=AppState.submit,
            loading=AppState.is_loading,
        ),
        spacing="3",
        align="center",
    )
