import reflex as rx

from ..state import PERIOD_OPTIONS, AppState

INDEX_REFERENCE = [
    ("S&P 500", "^GSPC", "美國大型股整體市場，最常用"),
    ("NASDAQ Composite", "^IXIC", "那斯達克綜合指數"),
    ("Dow Jones", "^DJI", "道瓊工業指數"),
    ("Russell 2000", "^RUT", "美國小型股"),
    ("NASDAQ-100", "^NDX", "那斯達克 100 大型非金融股"),
]


def _index_reference_row(name: str, symbol: str, desc: str) -> rx.Component:
    return rx.table.row(
        rx.table.cell(name, size="1"),
        rx.table.cell(rx.code(symbol, size="1"), size="1"),
        rx.table.cell(desc, size="1", color="gray"),
        on_click=AppState.set_ticker_input(symbol),
        cursor="pointer",
        _hover={"background": "var(--gray-a3)"},
    )


def _index_reference_table() -> rx.Component:
    return rx.vstack(
        rx.text("常用美股指數代碼", size="1", weight="bold", color="gray"),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("指數"),
                    rx.table.column_header_cell("代碼"),
                    rx.table.column_header_cell("說明"),
                ),
            ),
            rx.table.body(
                *[_index_reference_row(name, symbol, desc) for name, symbol, desc in INDEX_REFERENCE],
            ),
            variant="surface",
            size="1",
        ),
        spacing="1",
        align_items="start",
    )


def controls() -> rx.Component:
    return rx.hstack(
        rx.hstack(
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
        ),
        _index_reference_table(),
        spacing="5",
        align="start",
        wrap="wrap",
    )
