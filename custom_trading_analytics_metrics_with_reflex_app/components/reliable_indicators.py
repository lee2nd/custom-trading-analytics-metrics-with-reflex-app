import reflex as rx

# Links verified directly against each site; Alternative.me and CoinGlass use
# the exact URLs provided (zh-TW CoinGlass path, canonical Alternative.me path).
SOURCES = [
    {
        "name": "Alternative.me",
        "url": "https://alternative.me/crypto/fear-and-greed-index/",
        "tag": "首選、每日看情緒",
        "strength": "經典 Crypto Fear & Greed Index，0–100 指數並附歷史走勢，適合判斷市場整體情緒與週期",
    },
    {
        "name": "CoinGecko",
        "url": "https://www.coingecko.com/zh-tw/charts/fear-and-greed-index",
        "tag": "綜合型情緒指標",
        "strength": "自有 Fear & Greed 指數，除價格外納入鏈上、資金流、期貨市場結構等因素，可查看歷史走勢",
    },
    {
        "name": "CoinMarketCap",
        "url": "https://coinmarketcap.com/charts/fear-and-greed-index/",
        "tag": "大盤觀察",
        "strength": "Fear & Greed 指數同時呈現市值、交易量與 BTC Dominance，適合一起觀察整體市場狀況",
    },
    {
        "name": "CoinGlass",
        "url": "https://www.coinglass.com/zh-TW/pro/i/FearGreedIndex",
        "tag": "交易情緒更實用",
        "strength": "除情緒指數外還有 Funding Rate、Open Interest、Long/Short Ratio、清算熱力圖等合約交易數據，適合做合約、短中線交易的人參考",
    },
]

# Radix color token per band, ordered low→high so the scale bar and legend
# render as one continuous red→teal gradient.
RANGES = [
    {
        "range": "0 – 24",
        "label": "極度恐懼 Extreme Fear",
        "color": "red",
        "span": 24,
        "description": "市場出現恐慌性拋售或連環清算，投資人過度悲觀，常被長線投資者視為分批觀察買點的區域。",
    },
    {
        "range": "25 – 49",
        "label": "恐懼 Fear",
        "color": "orange",
        "span": 25,
        "description": "市場情緒偏謹慎、觀望氣氛濃厚。",
    },
    {
        "range": "50 – 74",
        "label": "貪婪 Greed",
        "color": "green",
        "span": 25,
        "description": "樂觀情緒升溫，資金持續流入，山寨幣開始轉趨活躍。",
    },
    {
        "range": "75 – 100",
        "label": "極度貪婪 Extreme Greed",
        "color": "teal",
        "span": 26,
        "description": "市場出現 FOMO（錯失恐懼症）與高槓桿堆積，通常代表短期過熱、回調風險升高。",
    },
]

# ForexFactory calendar: single link card reusing the _source_card() layout.
FOREX_CALENDAR_SOURCE = {
    "name": "ForexFactory Calendar",
    "url": "https://www.forexfactory.com/calendar",
    "tag": "即時財經日曆",
    "strength": "篩選高評級（紅色）美元事件，掌握 CPI、NFP、FOMC 等牽動市場的公布時間點。",
}

# Filter 設定步驟，依序對應 ForexFactory 日曆上方 Filter 選單的操作順序。
FILTER_STEPS = [
    ("sliders-horizontal", "點選日曆上方的 Filter。"),
    ("flame", "Impact：只勾選 High（紅色）。"),
    ("dollar-sign", "Currency：優先勾選 USD。"),
    ("clock", "時區設定為你的當地時間，台灣是 GMT+8。"),
    ("list-checks", "每天先看 Today，再看 Tomorrow 以及本週剩餘事件。"),
]

# Radix color token per sentiment tone, used to color individual table-cell
# text segments (not the whole cell, since one cell can mix tones).
TONE_COLORS = {
    "up": "var(--green-11)",
    "down": "var(--red-11)",
    "neutral": "gray",
}

# 經濟數據公布結果對「偏強/高於預期」「偏弱/低於預期」的常見市場解讀。
# 每格文字拆成 (文字片段, tone) 列表；tone 對應 TONE_COLORS。同一格若同時
# 出現利多與利空語意（例如 GDP、Retail Sales 偏弱欄），拆成多個片段分別
# 上色，而非整格只選一種顏色。沒有明確「利多/利好/利空/不利」字眼的描述
# （例如「視通膨與利率環境」「可能偏鷹/偏鴿」）一律標記為 neutral。
ECONOMIC_INDICATORS = [
    {
        "metric": "CPI / Core CPI",
        "strong": [("可能利空風險資產", "down")],
        "weak": [("可能利多風險資產", "up")],
    },
    {
        "metric": "PCE",
        "strong": [("可能利空", "down")],
        "weak": [("可能利多", "up")],
    },
    {
        "metric": "NFP",
        "strong": [("視通膨與利率環境", "neutral")],
        "weak": [("視衰退風險", "neutral")],
    },
    {
        "metric": "Unemployment",
        "strong": [("可能利空降息預期", "down")],
        "weak": [("可能利多降息，", "up"), ("但也可能引發衰退擔憂", "neutral")],
    },
    {
        "metric": "Retail Sales",
        "strong": [("經濟強，但利率可能較高", "neutral")],
        "weak": [("可能利多降息，", "up"), ("或利空經濟", "down")],
    },
    {
        "metric": "GDP",
        "strong": [("可能利好盈利，", "up"), ("利空降息預期", "down")],
        "weak": [("可能利多降息，", "up"), ("或利空成長", "down")],
    },
    {
        "metric": "ISM PMI",
        "strong": [("視景氣及通膨分項", "neutral")],
        "weak": [("視衰退與利率預期", "neutral")],
    },
    {
        "metric": "JOLTS",
        "strong": [("勞動需求強，可能偏鷹", "neutral")],
        "weak": [("勞動需求弱，可能偏鴿", "neutral")],
    },
    {
        "metric": "FOMC",
        "strong": [("偏鷹通常不利風險資產", "down")],
        "weak": [("偏鴿通常利多風險資產", "up")],
    },
]


def _source_card(source: dict) -> rx.Component:
    return rx.link(
        rx.vstack(
            rx.hstack(
                rx.text(source["name"], size="2", weight="bold"),
                rx.icon("external-link", size=14, color="var(--gray-9)"),
                justify="between",
                align="center",
                width="100%",
            ),
            rx.badge(source["tag"], color_scheme="gray", size="1", variant="soft"),
            rx.text(source["strength"], size="2", color="gray"),
            spacing="2",
            align_items="start",
            width="100%",
        ),
        href=source["url"],
        is_external=True,
        underline="none",
        width="100%",
        padding="0.9em 1em",
        border_radius="10px",
        border="1px solid var(--gray-a5)",
        background="var(--gray-a2)",
        _hover={"border_color": "var(--accent-8)", "background": "var(--gray-a3)"},
    )


def _scale_bar() -> rx.Component:
    return rx.hstack(
        *[
            rx.box(
                width=f"{band['span']}%",
                height="10px",
                background=f"var(--{band['color']}-9)",
            )
            for band in RANGES
        ],
        spacing="0",
        width="100%",
        border_radius="999px",
        overflow="hidden",
    )


def _range_row(band: dict) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text(band["range"], size="2", weight="bold", color=f"var(--{band['color']}-11)", white_space="nowrap"),
            rx.text(band["label"], size="2", weight="bold", color=f"var(--{band['color']}-11)"),
            spacing="2",
            align="baseline",
        ),
        rx.text(band["description"], size="2", color="gray"),
        border_left=f"4px solid var(--{band['color']}-9)",
        padding_left="0.75em",
        padding_y="0.1em",
    )


def _filter_step(index: int, icon: str, text: str) -> rx.Component:
    return rx.hstack(
        rx.badge(str(index), color_scheme="gray", variant="soft", radius="full"),
        rx.icon(icon, size=16, color="var(--accent-9)", flex_shrink="0"),
        rx.text(text, size="2", color="gray"),
        spacing="2",
        align="center",
    )


def _tone_cell(segments: list[tuple[str, str]]) -> rx.Component:
    return rx.text(
        *[rx.text.span(text, color=TONE_COLORS[tone]) for text, tone in segments],
        size="2",
    )


def _indicator_row(indicator: dict) -> rx.Component:
    return rx.table.row(
        rx.table.row_header_cell(rx.text(indicator["metric"], size="2", weight="bold")),
        rx.table.cell(_tone_cell(indicator["strong"])),
        rx.table.cell(_tone_cell(indicator["weak"])),
        _hover={"background": "var(--gray-a2)"},
        style={"verticalAlign": "middle"},
    )


def reliable_indicators() -> rx.Component:
    return rx.vstack(
        rx.heading("可靠指標", size="5"),
        rx.text("加密貨幣恐慌貪婪指數：四個可參考的指數來源，點擊卡片即可開啟官方頁面。", size="2", color="gray"),
        rx.box(
            *[_source_card(source) for source in SOURCES],
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(260px, 1fr))",
                "gap": "0.75em",
            },
            width="100%",
        ),
        rx.box(
            rx.text("數值區間速查", size="3", weight="bold"),
            rx.vstack(
                _scale_bar(),
                *[_range_row(band) for band in RANGES],
                spacing="3",
                width="100%",
                padding_top="0.9em",
            ),
            width="100%",
            padding="1.25em 1.5em",
            border_radius="12px",
            border="1px solid var(--gray-a5)",
            background="var(--gray-a2)",
            margin_top="0.5em",
        ),
        align_items="start",
        spacing="4",
        width="100%",
    )
