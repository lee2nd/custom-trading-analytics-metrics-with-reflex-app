import reflex as rx

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
        "name": "Bloomberg（彭博） / Reuters（路透社）",
        "strength": "全球機構法人的一手消息來源。涉及美國利率政策、大型科技股財報、國際貿易關稅或重大監管時，這兩家幾乎是所有媒體轉載的源頭（Bloomberg 有免費閱讀額度，重度需求建議訂閱）。",
    },
    {
        "category": "跨市場與總經",
        "name": "財經M平方 (MacroMicro)",
        "strength": "偏重「數據解讀」而非即時新聞，將台美總經指標、聯準會動向與產業循環圖表化，適合用來過濾日常雜訊、確認中長線趨勢。",
    },
    {
        "category": "台股",
        "name": "經濟日報 / 工商時報",
        "strength": "台灣兩大財經專業報，對半導體供應鏈（台積電、AI 伺服器）、法說會重點與本土政策法規的報導最完整。",
    },
    {
        "category": "台股",
        "name": "Yahoo奇摩股市",
        "strength": "聚合台灣各大財經媒體的即時新聞，搭配個股報價與法人買賣超資訊，適合盤中快速掃描個股異動原因。",
    },
    {
        "category": "美股",
        "name": "CNBC",
        "strength": "美股盤中即時動態、華爾街分析師評級調整與企業 CEO 專訪的第一線平台，電視直播與網頁快訊同步。",
    },
    {
        "category": "美股",
        "name": "Benzinga",
        "strength": "專精於短線交易者最需要的「異動原因（Why Is It Moving）」，盤前盤後某檔股票突然暴漲暴跌時，這裡通常最快給出理由。",
    },
    {
        "category": "美股",
        "name": "Seeking Alpha",
        "strength": "匯集全球分析師的個股深度研究報告，並提供最完整的美股財報電話會議逐字稿（Earnings Call Transcripts）。",
    },
    {
        "category": "美股",
        "name": "Finviz",
        "strength": "雖以選股器聞名，但首頁與每檔個股頁面下方會直接彙整各大外媒（WSJ、MarketWatch、Yahoo Finance 等）的最新新聞連結，掃描效率極高。",
    },
    {
        "category": "加密貨幣",
        "name": "The Block",
        "strength": "機構級研究與深度新聞，對 ETF 資金流向、監管政策與一級市場融資消息最精準。",
    },
    {
        "category": "加密貨幣",
        "name": "CoinDesk / Cointelegraph",
        "strength": "幣圈最具影響力的兩大綜合媒體，重大協議升級、駭客事件或市場突發消息都會第一時間發布。",
    },
    {
        "category": "加密貨幣",
        "name": "動區動趨 (BlockTempo) / 鏈新聞 (ABMedia)",
        "strength": "台灣最活躍的兩大區塊鏈媒體，編譯海外一手快訊的速度極快，並會補充台灣在地法規與交易所動態。",
    },
    {
        "category": "加密貨幣",
        "name": "PANews / Foresight News",
        "strength": "提供類似彭博終端機的「24 小時滾動快訊流」，適合盯盤時快速瀏覽鏈上大額轉帳與項目公告。",
    },
    {
        "category": "實戰建議",
        "name": "看盤整合",
        "strength": "將台股、美股與幣圈的自選標的全部加入 TradingView，直接開啟右側的「新聞（News）」面板，即可在單一視窗接收所有相關外電。",
    },
    {
        "category": "實戰建議",
        "name": "數據預警",
        "strength": "每天開盤前先看 Investing.com 的財經日曆，確認當晚是否有美國總經數據公布或聯準會官員演說。",
    },
]


def _source_name_cell(source: dict) -> rx.Component:
    if source.get("url"):
        return rx.link(
            rx.hstack(
                rx.text(source["name"], size="2", weight="bold"),
                rx.icon("external-link", size=14, color="var(--accent-11)"),
                spacing="2",
                align="center",
            ),
            href=source["url"],
            is_external=True,
            underline="none",
        )
    return rx.text(source["name"], size="2", weight="bold")


def _source_row(source: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(source["category"], white_space="nowrap", color="gray"),
        rx.table.row_header_cell(_source_name_cell(source)),
        rx.table.cell(source["strength"]),
        _hover={"background": "var(--gray-a2)"},
        style={"verticalAlign": "middle"},
    )


def news() -> rx.Component:
    return rx.vstack(
        rx.heading("新聞", size="5"),
        rx.text("綜合看盤平台，以及依市場分類的一手新聞來源與實戰建議。", size="2", color="gray"),
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("分類"),
                        rx.table.column_header_cell("平台名稱"),
                        rx.table.column_header_cell("核心優勢與定位"),
                    )
                ),
                rx.table.body(*[_source_row(source) for source in NEWS_SOURCES]),
                variant="surface",
                width="100%",
            ),
            width="100%",
            overflow_x="auto",
        ),
        align_items="start",
        spacing="3",
        width="100%",
    )
