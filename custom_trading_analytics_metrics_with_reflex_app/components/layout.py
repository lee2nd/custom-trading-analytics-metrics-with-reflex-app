import reflex as rx

from ..state import AppState
from .controls import controls

SUMMARY_ITEMS = [
    ("news", "新聞", "newspaper"),
    ("reliable_indicators", "可靠指標", "shield-check"),
    ("news_sites", "消息網站", "globe"),
]

ANALYSIS_ITEMS = [
    ("dashboard", "Technical Analysis", "layout-dashboard"),
]


def _nav_item(section: str, page: str, label: str, icon: str) -> rx.Component:
    is_active = AppState.active_page == page
    return rx.hstack(
        rx.icon(icon, size=16),
        rx.text(label, size="2", weight=rx.cond(is_active, "medium", "regular")),
        on_click=AppState.set_active_page(section, page),
        spacing="2",
        align="center",
        width="100%",
        padding="0.5em 0.75em",
        border_radius="8px",
        cursor="pointer",
        color=rx.cond(is_active, "var(--accent-11)", "var(--gray-11)"),
        background=rx.cond(is_active, "var(--accent-a3)", "transparent"),
        transition="background 0.15s ease, color 0.15s ease",
        _hover={"background": rx.cond(is_active, "var(--accent-a4)", "var(--gray-a3)")},
    )


def _nav_section(title: str, section: str, items: list[tuple[str, str, str]]) -> rx.Component:
    return rx.vstack(
        rx.text(
            title,
            size="1",
            weight="bold",
            color="gray",
            padding_x="0.75em",
            style={"textTransform": "uppercase", "letterSpacing": "0.06em"},
        ),
        *[_nav_item(section, page, label, icon) for page, label, icon in items],
        spacing="1",
        width="100%",
        align_items="stretch",
    )


def _sidebar() -> rx.Component:
    return rx.vstack(
        _nav_section("摘要", "summary", SUMMARY_ITEMS),
        _nav_section("My 分析", "analysis", ANALYSIS_ITEMS),
        width="230px",
        flex_shrink="0",
        spacing="5",
        padding="1.5em 0.75em",
        align_items="stretch",
        border_right="1px solid var(--gray-a5)",
        background="var(--gray-a2)",
    )


def _summary_placeholder(label: str) -> rx.Component:
    return rx.vstack(
        rx.heading(label, size="5"),
        rx.text("內容尚未提供，敬請期待。", color="gray"),
        align_items="start",
        spacing="2",
    )


DASHBOARD_EXPLANATION_POINTS = [
    ("trending-up", "均線 SMA / EMA", "判斷趨勢方向的參考線，短天期均線由下往上穿越長天期稱為黃金交叉（偏多訊號），反之為死亡交叉（偏空訊號）。"),
    ("waves", "布林通道 Bollinger Bands", "以價格的標準差畫出上下軌，價格貼近上軌代表相對強勢（可能超買），貼近下軌代表相對弱勢（可能超賣）。"),
    ("bar-chart-3", "成交量 Volume", "黑色虛線為 20 日均量：柱狀圖高於虛線代表「量增」（參與變熱），低於虛線代表「量縮」（關注度降低）；滑鼠掂過柱子可看到現量為均量的百分比。"),
    ("gauge", "RSI 相對強弱指標", "衡量近期漲跌力道，數值介於 0～100。一般 70 以上視為超買、30 以下視為超賣。"),
    ("activity", "MACD", "由快慢均線差值構成，柱狀圖由負轉正（翻紅）常被視為動能轉強訊號，由正轉負則相反。"),
    ("ruler", "ATR 平均真實波幅", "衡量價格波動幅度的大小，數值愈高代表波動愈劇烈，可用來評估風險與設定停損距離。"),
]


def _dashboard_explanation() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("info", size=16, color="var(--accent-11)"),
            rx.text("圖表指標說明", size="3", weight="bold"),
            spacing="2",
            align="center",
        ),
        rx.grid(
            *[
                rx.hstack(
                    rx.icon(icon, size=16, color="var(--accent-9)", flex_shrink="0"),
                    rx.vstack(
                        rx.text(title, size="2", weight="medium"),
                        rx.text(desc, size="2", color="gray"),
                        spacing="0",
                        align_items="start",
                    ),
                    spacing="2",
                    align="start",
                )
                for icon, title, desc in DASHBOARD_EXPLANATION_POINTS
            ],
            columns="2",
            spacing="4",
            padding_top="0.75em",
            width="100%",
        ),
        width="100%",
        padding="1.25em 1.5em",
        border_radius="12px",
        border="1px solid var(--gray-a5)",
        background="var(--gray-a2)",
        margin_top="1.5em",
    )


def _analysis_content() -> rx.Component:
    return rx.vstack(
        controls(),
        rx.cond(
            AppState.error != "",
            rx.callout(AppState.error, color_scheme="red"),
        ),
        rx.match(
            AppState.active_page,
            (
                "dashboard",
                rx.vstack(
                    rx.plotly(
                        data=AppState.dashboard_figure, width="100%",
                        config={"displaylogo": False},
                    ),
                    _dashboard_explanation(),
                    width="100%",
                    spacing="0",
                ),
            ),
        ),
        width="100%",
        spacing="4",
    )


def _main_content() -> rx.Component:
    return rx.box(
        rx.match(
            AppState.active_page,
            ("news", _summary_placeholder("新聞")),
            ("reliable_indicators", _summary_placeholder("可靠指標")),
            ("news_sites", _summary_placeholder("消息網站")),
            _analysis_content(),
        ),
        width="100%",
        padding="2em",
    )


def layout() -> rx.Component:
    return rx.vstack(
        rx.heading("Lee2nd 投資分析儀表板", size="6", padding="1.25em 1.5em 0"),
        rx.hstack(
            _sidebar(),
            _main_content(),
            width="100%",
            align_items="stretch",
            spacing="0",
        ),
        width="100%",
        spacing="4",
    )
