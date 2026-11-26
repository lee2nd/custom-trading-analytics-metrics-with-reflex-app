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
