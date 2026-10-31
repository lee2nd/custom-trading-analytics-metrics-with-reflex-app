import reflex as rx

# Ratings: 0 = 不適用, 1 = 參考, 2 = 適合, 3 = 最佳
LLM_RANKING_SITES = [
    {
        "name": "Artificial Analysis",
        "url": "https://artificialanalysis.ai/",
        "tag": "綜合能力・速度・成本",
        "stars": 5,
        "ratings": (3, 3, 3, 2),
    },
    {
        "name": "LMArena",
        "url": "https://arena.ai/leaderboard?tab=arena-elo",
        "tag": "真實使用者盲測",
        "stars": 5,
        "ratings": (3, 2, 3, 2),
    },
    {
        "name": "LiveBench",
        "url": "https://livebench.ai/",
        "tag": "新題目・研究/資料分析/Agent",
        "stars": 5,
        "ratings": (3, 3, 3, 2),
    },
    {
        "name": "SWE-bench",
        "url": "https://www.swebench.com/",
        "tag": "真實 GitHub 問題修復",
        "stars": 5,
        "ratings": (0, 3, 2, 0),
    },
    {
        "name": "Aider Polyglot",
        "url": "https://aider.chat/docs/leaderboards/",
        "tag": "程式正確率與成本",
        "stars": 4,
        "ratings": (0, 3, 1, 0),
    },
    {
        "name": "FinanceBenchmark",
        "url": "https://financebenchmark.ai/benchmarks",
        "tag": "財報・財務推理",
        "stars": 4,
        "ratings": (1, 0, 0, 3),
    },
    {
        "name": "LLMBenchmark.ai",
        "url": "https://llmbenchmark.ai/rankings",
        "tag": "多榜單彙整入口",
        "stars": 4,
        "ratings": (2, 2, 2, 1),
    },
]

LLM_RANKING_COLUMNS = [
    ("book-open", "知識整理"),
    ("code-xml", "寫程式"),
    ("database", "Data Eng"),
    ("chart-candlestick", "資產投資"),
]

LLM_RANKING_LEGEND = [
    (3, "最佳"),
    (2, "適合"),
    (1, "參考"),
]


def _dots(level: int) -> rx.Component:
    if level == 0:
        return rx.text("—", color="var(--gray-8)", size="2")
    return rx.hstack(
        *[
            rx.box(
                width="8px",
                height="8px",
                border_radius="50%",
                background="var(--accent-9)" if i < level else "var(--gray-a5)",
            )
            for i in range(3)
        ],
        spacing="1",
        align="center",
        justify="center",
    )


def _site_row(site: dict) -> rx.Component:
    return rx.table.row(
        rx.table.row_header_cell(
            rx.link(
                rx.hstack(
                    rx.vstack(
                        rx.text(site["name"], size="2", weight="bold"),
                        rx.text(site["tag"], size="1", color="gray"),
                        spacing="0",
                        align_items="start",
                    ),
                    rx.icon("external-link", size=14, color="var(--accent-11)"),
                    spacing="2",
                    align="center",
                ),
                href=site["url"],
                is_external=True,
                underline="none",
            ),
        ),
        *[rx.table.cell(_dots(level), text_align="center") for level in site["ratings"]],
        rx.table.cell(
            rx.text("★" * site["stars"] + "☆" * (5 - site["stars"]), size="2", color="var(--amber-9)"),
            text_align="center",
            white_space="nowrap",
        ),
        _hover={"background": "var(--gray-a2)"},
        style={"verticalAlign": "middle"},
    )


def _legend() -> rx.Component:
    return rx.hstack(
        *[
            rx.hstack(_dots(level), rx.text(label, size="1", color="gray"), spacing="1", align="center")
            for level, label in LLM_RANKING_LEGEND
        ],
        rx.text("— 不適用", size="1", color="gray"),
        spacing="4",
        align="center",
        wrap="wrap",
    )


def llm_rankings() -> rx.Component:
    return rx.vstack(
        rx.heading("LLM 模型排名", size="5"),
        rx.text("點網站名稱開啟排行榜；圓點為依你的使用情境評估的適合度。", size="2", color="gray"),
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("評測網站"),
                        *[
                            rx.table.column_header_cell(
                                rx.vstack(
                                    rx.icon(icon, size=16, color="var(--accent-11)"),
                                    rx.text(label, size="1"),
                                    spacing="1",
                                    align="center",
                                ),
                                text_align="center",
                                white_space="nowrap",
                            )
                            for icon, label in LLM_RANKING_COLUMNS
                        ],
                        rx.table.column_header_cell("推薦", text_align="center"),
                    )
                ),
                rx.table.body(*[_site_row(site) for site in LLM_RANKING_SITES]),
                variant="surface",
                width="100%",
            ),
            width="100%",
            overflow_x="auto",
        ),
        _legend(),
        rx.callout(
            "排名僅反映特定測試；重大選型請回原始榜單確認測試日期與設定。財務分析能力不等於投資報酬。",
            icon="info",
            size="1",
            color_scheme="gray",
        ),
        align_items="start",
        spacing="3",
        width="100%",
    )
