import itertools

import reflex as rx

# Radix color token used for each category's accent bar, heading, and card
# hover border.
CATEGORY_COLORS = {
    "綜合看盤": "green",
    "跨市場與總經": "purple",
    "台股": "blue",
    "美股": "amber",
    "加密貨幣": "crimson",
}

# Ordered by category so itertools.groupby in news() produces one group per
# category without needing to sort first.
NEWS_SOURCES = [
    {
        "category": "綜合看盤",
        "name": "TradingView",
        "url": "https://www.tradingview.com/",
        "strength": "看盤同時整合 Reuters、Benzinga、Cointelegraph 等外電，可依自選股過濾快訊",
    },
    {
        "category": "綜合看盤",
        "name": "Investing.com",
        "url": "https://www.investing.com/",
        "strength": "全球最完整的即時財經日曆（CPI、非農、FOMC 數據秒級更新）與多市場新聞流",
    },
    {
        "category": "綜合看盤",
        "name": "鉅亨網 (Anue)",
        "url": "https://www.cnyes.com/",
        "strength": "台灣本土資訊最完整，涵蓋台股盤中快訊、美股外電編譯與加密貨幣專區",
    },
    {
        "category": "跨市場與總經",
        "name": "Bloomberg（彭博）",
        "url": "https://www.bloomberg.com/",
        "strength": "全球機構法人的一手消息來源，涉及美國利率政策、大型科技股財報、國際貿易關稅或重大監管時幾乎是所有媒體轉載的源頭（有免費閱讀額度，重度需求建議訂閱）",
    },
    {
        "category": "跨市場與總經",
        "name": "Reuters（路透社）",
        "url": "https://www.reuters.com/",
        "strength": "全球機構法人的一手消息來源，與 Bloomberg 並列重大政策、財報與監管新聞的轉載源頭",
    },
    {
        "category": "跨市場與總經",
        "name": "財經M平方 (MacroMicro)",
        "url": "https://www.macromicro.me/",
        "strength": "偏重「數據解讀」而非即時新聞，將台美總經指標、聯準會動向與產業循環圖表化，適合用來過濾日常雜訊、確認中長線趨勢",
    },
    {
        "category": "台股",
        "name": "經濟日報",
        "url": "https://money.udn.com/money/index",
        "strength": "台灣財經專業報，對半導體供應鏈（台積電、AI 伺服器）、法說會重點與本土政策法規的報導最完整",
    },
    {
        "category": "台股",
        "name": "工商時報",
        "url": "https://www.ctee.com.tw/",
        "strength": "台灣兩大財經專業報之一，聚焦工商界要聞與產業財經重要新聞",
    },
    {
        "category": "台股",
        "name": "Yahoo奇摩股市",
        "url": "https://tw.stock.yahoo.com/",
        "strength": "聚合台灣各大財經媒體的即時新聞，搭配個股報價與法人買賣超資訊，適合盤中快速掃描個股異動原因",
    },
    {
        "category": "美股",
        "name": "CNBC",
        "url": "https://www.cnbc.com/",
        "strength": "美股盤中即時動態、華爾街分析師評級調整與企業 CEO 專訪的第一線平台，電視直播與網頁快訊同步",
    },
    {
        "category": "美股",
        "name": "Benzinga",
        "url": "https://www.benzinga.com/",
        "strength": "專精於短線交易者最需要的「異動原因（Why Is It Moving）」，盤前盤後某檔股票突然暴漲暴跌時這裡通常最快給出理由",
    },
    {
        "category": "美股",
        "name": "Seeking Alpha",
        "url": "https://seekingalpha.com/",
        "strength": "匯集全球分析師的個股深度研究報告，並提供最完整的美股財報電話會議逐字稿（Earnings Call Transcripts）",
    },
    {
        "category": "美股",
        "name": "Finviz",
        "url": "https://finviz.com/",
        "strength": "雖以選股器聞名，但首頁與每檔個股頁面下方會直接彙整各大外媒（WSJ、MarketWatch、Yahoo Finance 等）的最新新聞連結，掃描效率極高",
    },
    {
        "category": "加密貨幣",
        "name": "The Block",
        "url": "https://www.theblock.co/",
        "strength": "機構級研究與深度新聞，對 ETF 資金流向、監管政策與一級市場融資消息最精準",
    },
    {
        "category": "加密貨幣",
        "name": "CoinDesk",
        "url": "https://www.coindesk.com/",
        "strength": "幣圈最具影響力的綜合媒體之一，重大協議升級、駭客事件或市場突發消息都會第一時間發布",
    },
    {
        "category": "加密貨幣",
        "name": "Cointelegraph",
        "url": "https://cointelegraph.com/",
        "strength": "幣圈最具影響力的綜合媒體之一，與 CoinDesk 並列重大新聞的第一手來源",
    },
    {
        "category": "加密貨幣",
        "name": "動區動趨 (BlockTempo)",
        "url": "https://www.blocktempo.com/",
        "strength": "台灣最活躍的區塊鏈媒體之一，編譯海外一手快訊的速度極快，並會補充台灣在地法規與交易所動態",
    },
    {
        "category": "加密貨幣",
        "name": "鏈新聞 (ABMedia)",
        "url": "https://abmedia.io/",
        "strength": "台灣最活躍的區塊鏈媒體之一，提供全球區塊鏈與加密貨幣的一手新聞與趨勢報告",
    },
    {
        "category": "加密貨幣",
        "name": "PANews",
        "url": "https://www.panewslab.com/zh-hant",
        "strength": "提供類似彭博終端機的「24 小時滾動快訊流」，適合盯盤時快速瀏覽鏈上大額轉帳與項目公告",
    },
    {
        "category": "加密貨幣",
        "name": "Foresight News",
        "url": "https://www.foresightnews.pro/",
        "strength": "聚焦 Web3 產業趨勢的快訊平台，提供即時新聞與深度解析",
    },
]


def _source_card(source: dict) -> rx.Component:
    color = CATEGORY_COLORS[source["category"]]
    return rx.link(
        rx.vstack(
            rx.hstack(
                rx.text(source["name"], size="2", weight="bold"),
                rx.icon("external-link", size=14, color="var(--gray-9)"),
                justify="between",
                align="center",
                width="100%",
            ),
            rx.text(source["strength"], size="2", color="gray"),
            spacing="1",
            align_items="start",
            width="100%",
        ),
        href=source["url"],
        is_external=True,
        underline="none",
        width="100%",
        padding="0.75em 1em",
        border_radius="10px",
        border="1px solid var(--gray-a5)",
        background="var(--gray-a2)",
        _hover={"border_color": f"var(--{color}-8)", "background": "var(--gray-a3)"},
    )


def _category_section(category: str, sources: list[dict]) -> rx.Component:
    color = CATEGORY_COLORS[category]
    return rx.vstack(
        rx.box(
            rx.text(category, size="3", weight="bold", color=f"var(--{color}-11)"),
            border_left=f"4px solid var(--{color}-9)",
            padding_left="0.6em",
        ),
        rx.box(
            *[_source_card(source) for source in sources],
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(260px, 1fr))",
                "gap": "0.75em",
            },
            width="100%",
        ),
        align_items="start",
        spacing="3",
        width="100%",
    )


def news() -> rx.Component:
    return rx.vstack(
        rx.heading("新聞", size="5"),
        rx.text("依市場分類的一手新聞來源，點擊卡片即可開啟官方網站。", size="2", color="gray"),
        *[
            _category_section(category, list(sources))
            for category, sources in itertools.groupby(NEWS_SOURCES, key=lambda s: s["category"])
        ],
        align_items="start",
        spacing="5",
        width="100%",
    )
