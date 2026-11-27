# 重大訊息公布(ForexFactory 財經日曆)Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a「重大訊息公布」section to the existing 可靠指標 (`reliable_indicators()`) page that explains ForexFactory calendar filter setup and shows a static table mapping 9 common macro data releases to their typical "beat" / "miss" market interpretation.

**Architecture:** Single-file change to `custom_trading_analytics_metrics_with_reflex_app/components/reliable_indicators.py`. Follows the file's existing static-data + Radix-component pattern (module-level `list`/`dict` constants, small private `_` render helper functions, composed into the page-level `reliable_indicators()` function). No new files, no state, no backend calls.

**Tech Stack:** Reflex (Python → React), Radix UI theme tokens (`var(--{color}-11)` etc.), Lucide icons via `rx.icon`.

**Reference spec:** `docs/superpowers/specs/2026-11-27-economic-calendar-design.md`

**Testing note:** This codebase has no automated tests for its static-content page composers (`news.py`, `llm_rankings.py`, `reliable_indicators.py` all have zero test coverage — only `charts.py`/`indicators.py`/`state.py` are tested, per `tests/`). Consistent with that convention, this plan does not add pytest tests. Instead, each step verifies the change with a quick Python import/instantiation check (`python3 -c "..."`), which catches Python-level errors (typos, bad signatures, syntax errors) immediately. Final visual confirmation happens via `reflex run` in Task 5.

---

### Task 1: Add static data constants

**Files:**
- Modify: `custom_trading_analytics_metrics_with_reflex_app/components/reliable_indicators.py`

- [ ] **Step 1: Add `FOREX_CALENDAR_SOURCE`, `FILTER_STEPS`, `TONE_COLORS`, and `ECONOMIC_INDICATORS` constants**

Insert the following block right after the `RANGES = [...]` list closes (i.e. immediately before the `def _source_card(source: dict) -> rx.Component:` line):

```python
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
```

- [ ] **Step 2: Verify the module still imports cleanly**

Run:
```bash
python3 -c "
from custom_trading_analytics_metrics_with_reflex_app.components import reliable_indicators as ri
print('metrics:', [item['metric'] for item in ri.ECONOMIC_INDICATORS])
print('tones ok:', all(tone in ri.TONE_COLORS for item in ri.ECONOMIC_INDICATORS for _, tone in item['strong'] + item['weak']))
"
```
Expected output:
```
metrics: ['CPI / Core CPI', 'PCE', 'NFP', 'Unemployment', 'Retail Sales', 'GDP', 'ISM PMI', 'JOLTS', 'FOMC']
tones ok: True
```

- [ ] **Step 3: Commit**

```bash
git add custom_trading_analytics_metrics_with_reflex_app/components/reliable_indicators.py
git commit -m "Add ForexFactory calendar data constants to reliable_indicators"
```

---

### Task 2: Add render helpers for filter steps and table cells

**Files:**
- Modify: `custom_trading_analytics_metrics_with_reflex_app/components/reliable_indicators.py`

- [ ] **Step 1: Add `_filter_step`, `_tone_cell`, and `_indicator_row` helper functions**

Insert this block immediately after the existing `_range_row(band: dict) -> rx.Component:` function (i.e. right before `def reliable_indicators() -> rx.Component:`):

```python
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
```

- [ ] **Step 2: Verify the helpers build real components without error**

Run:
```bash
python3 -c "
from custom_trading_analytics_metrics_with_reflex_app.components import reliable_indicators as ri
step = ri._filter_step(1, 'sliders-horizontal', '點選日曆上方的 Filter。')
cell = ri._tone_cell(ri.ECONOMIC_INDICATORS[5]['strong'])
row = ri._indicator_row(ri.ECONOMIC_INDICATORS[5])
print('OK', type(step).__name__, type(cell).__name__, type(row).__name__)
"
```
Expected output (exact class names may vary slightly by Reflex version, but it must print `OK` with no traceback):
```
OK HStack Text Row
```

- [ ] **Step 3: Commit**

```bash
git add custom_trading_analytics_metrics_with_reflex_app/components/reliable_indicators.py
git commit -m "Add filter-step and table-row render helpers for economic calendar"
```

---

### Task 3: Add the `_economic_calendar_section()` composer

**Files:**
- Modify: `custom_trading_analytics_metrics_with_reflex_app/components/reliable_indicators.py`

- [ ] **Step 1: Add the section composer function**

Insert this block immediately after `_indicator_row` (still before `def reliable_indicators() -> rx.Component:`):

```python
def _economic_calendar_section() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("calendar-clock", size=16, color="var(--accent-11)"),
                rx.text("重大訊息公布", size="3", weight="bold"),
                spacing="2",
                align="center",
            ),
            rx.text(
                "追蹤會牽動美元與風險資產走勢的高評級（紅色）經濟數據，"
                "建議透過 ForexFactory 財經日曆篩選後每日追蹤。",
                size="2",
                color="gray",
            ),
            _source_card(FOREX_CALENDAR_SOURCE),
            rx.vstack(
                rx.text("Filter 設定", size="3", weight="bold"),
                *[
                    _filter_step(index, icon, text)
                    for index, (icon, text) in enumerate(FILTER_STEPS, start=1)
                ],
                spacing="2",
                align_items="start",
                width="100%",
            ),
            rx.vstack(
                rx.text("數據公布：偏強 / 偏弱影響對照", size="3", weight="bold"),
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("數據"),
                                rx.table.column_header_cell("偏強 / 高於預期"),
                                rx.table.column_header_cell("偏弱 / 低於預期"),
                            )
                        ),
                        rx.table.body(*[_indicator_row(item) for item in ECONOMIC_INDICATORS]),
                        variant="surface",
                        width="100%",
                    ),
                    width="100%",
                    overflow_x="auto",
                ),
                spacing="2",
                align_items="start",
                width="100%",
            ),
            rx.callout(
                "以上對照僅為市場慣例參考，實際影響力需視當下總經環境、市場預期與資金部位而定，"
                "並非保證走勢，請搭配其他指標綜合判斷。",
                icon="info",
                size="1",
                color_scheme="gray",
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        width="100%",
        padding="1.25em 1.5em",
        border_radius="12px",
        border="1px solid var(--gray-a5)",
        background="var(--gray-a2)",
        margin_top="1.5em",
    )
```

- [ ] **Step 2: Verify the section builds without error**

Run:
```bash
python3 -c "
from custom_trading_analytics_metrics_with_reflex_app.components import reliable_indicators as ri
section = ri._economic_calendar_section()
print('OK', type(section).__name__)
"
```
Expected output:
```
OK Box
```

- [ ] **Step 3: Commit**

```bash
git add custom_trading_analytics_metrics_with_reflex_app/components/reliable_indicators.py
git commit -m "Add economic calendar section composer"
```

---

### Task 4: Wire the section into the page

**Files:**
- Modify: `custom_trading_analytics_metrics_with_reflex_app/components/reliable_indicators.py:126-158` (the `reliable_indicators()` function; exact line numbers will shift after Tasks 1-3 add code above it — locate the function by name, not by line number)

- [ ] **Step 1: Append `_economic_calendar_section()` as the last child of `reliable_indicators()`**

Current end of the function looks like this:

```python
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
```

Replace it with:

```python
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
        _economic_calendar_section(),
        align_items="start",
        spacing="4",
        width="100%",
    )
```

- [ ] **Step 2: Verify the full page component builds without error**

Run:
```bash
python3 -c "
from custom_trading_analytics_metrics_with_reflex_app.components.reliable_indicators import reliable_indicators
page = reliable_indicators()
print('OK', type(page).__name__)
"
```
Expected output:
```
OK VStack
```

- [ ] **Step 3: Commit**

```bash
git add custom_trading_analytics_metrics_with_reflex_app/components/reliable_indicators.py
git commit -m "Wire economic calendar section into reliable_indicators page"
```

---

### Task 5: Visual verification in the running app

**Files:** none (manual check only)

- [ ] **Step 1: Run the project's existing test suite to confirm no regressions**

```bash
python3 -m pytest tests/ -v
```
Expected: all existing tests still PASS (this change touches no code they exercise, so this is a regression guard, not new coverage).

- [ ] **Step 2: Start the Reflex dev server**

```bash
reflex run
```
Wait for the terminal to show the local frontend URL (default `http://localhost:3000`).

- [ ] **Step 3: Open the app and navigate to 可靠指標**

In a browser, open the frontend URL, click **可靠指標** in the left sidebar, and scroll past the existing 恐慌貪婪指數 section. Confirm:
- 「重大訊息公布」區塊標題與說明文字正常顯示。
- ForexFactory 連結卡片可點擊，在新分頁開啟 `https://www.forexfactory.com/calendar`。
- 5 個 Filter 設定步驟依序顯示，各自帶有編號與 icon。
- 對照表顯示 9 列資料，欄位為「數據」「偏強 / 高於預期」「偏弱 / 低於預期」。
- 混合語意的欄位（Unemployment 偏弱、Retail Sales 偏弱、GDP 偏強、GDP 偏弱）在同一格內同時出現綠字與紅字片段。
- 中性欄位（NFP、ISM PMI、JOLTS）文字為灰色。
- 底部免責聲明 callout 正常顯示。

- [ ] **Step 4: Stop the dev server**

Stop the `reflex run` process (Ctrl+C in the terminal, or terminate the background shell if it was started with the `bash` tool in async mode).

- [ ] **Step 5: Final commit (if any manual fixes were needed during visual check)**

If Step 3 revealed any visual issues, fix them in `reliable_indicators.py`, re-run Steps 1-3, then commit:

```bash
git add custom_trading_analytics_metrics_with_reflex_app/components/reliable_indicators.py
git commit -m "Fix visual issues found in economic calendar section review"
```

If no issues were found, no commit is needed for this task.

---

## Self-Review Notes

- **Spec coverage:** Task 1 covers 資料內容/資料結構 section of the spec; Task 2 covers per-cell tone coloring behavior; Task 3 covers the full visual structure (標題列、說明文字、連結卡片、Filter 步驟、對照表、免責說明); Task 4 covers 放置位置 (appended after 數值區間速查 box, inside `reliable_indicators()`); Task 5 covers 測試 section (no new automated tests, manual verification).
- **Placeholder scan:** no TBD/TODO; every step has complete, runnable code or exact commands with expected output.
- **Type consistency:** `TONE_COLORS` keys (`up`/`down`/`neutral`) match the tones used throughout `ECONOMIC_INDICATORS` (Task 1) and are the only keys read by `_tone_cell` (Task 2). `FOREX_CALENDAR_SOURCE` (Task 1) matches the `dict` shape expected by the existing `_source_card(source: dict)` function (`name`/`url`/`tag`/`strength` keys, same as `SOURCES` entries). `FILTER_STEPS` tuple shape `(icon, text)` matches the `_filter_step(index, icon, text)` signature via `enumerate(FILTER_STEPS, start=1)` unpacking in Task 3.
