# 重大訊息公布(ForexFactory 財經日曆)設計文件

- 日期:2026-11-27
- 範圍:在「可靠指標」頁面新增「重大訊息公布」區塊
- 狀態:已核准,待寫實作計畫

## 背景

「可靠指標」頁面(`custom_trading_analytics_metrics_with_reflex_app/components/reliable_indicators.py`)
目前只有「恐慌貪婪指數」區塊:四個來源連結卡片 + 數值區間速查色階表。使用者希望再加入
「重大訊息公布」區塊,引導他們使用 ForexFactory 財經日曆(`https://www.forexfactory.com/calendar`)
的篩選設定,並提供一份「經濟數據公布結果 vs. 市場偏強/偏弱解讀」的對照表。

## 目標

1. 在同一頁面新增一個視覺上獨立、但風格一致的區塊,說明如何設定 ForexFactory 日曆篩選。
2. 提供一份靜態對照表,列出 9 項常見總經數據(CPI/Core CPI、PCE、NFP、Unemployment、
   Retail Sales、GDP、ISM PMI、JOLTS、FOMC)在「偏強 / 高於預期」與「偏弱 / 低於預期」
   時,對風險資產/降息預期等的常見解讀。
3. 維持現有專案的靜態資料 + Radix 元件風格(不做任何即時爬蟲或 API 串接)。

## 非目標

- 不即時抓取 ForexFactory 的日曆資料(不做爬蟲、不做後端排程更新)。
- 不新增側邊欄分頁(已確認放在既有「可靠指標」頁面內)。
- 不處理使用者帳號、通知提醒等功能。

## 放置位置與視覺結構

新增區塊接在 `reliable_indicators()` 現有的「數值區間速查」色階區塊之後,作為第二個
卡片式區塊,沿用相同的外框樣式(`border_radius="12px"`、`border="1px solid var(--gray-a5)"`、
`background="var(--gray-a2)"`、`padding="1.25em 1.5em"`、`margin_top`)。

由上到下的內容:

1. **標題列**:`rx.icon("calendar-clock")` + 粗體標題文字「重大訊息公布」,風格比照
   `layout.py` 的 `_dashboard_explanation()` 標題列(icon + 粗體文字橫向排列)。
2. **說明文字**(`size="2"`, `color="gray"`):
   「追蹤會牽動美元與風險資產走勢的高評級(紅色)經濟數據,建議透過 ForexFactory
   財經日曆篩選後每日追蹤。」
3. **ForexFactory 連結卡片**:沿用 `reliable_indicators.py` 內 `_source_card()` 的卡片樣式
   (外部連結 icon、標籤 badge、說明文字),單張卡片,`href` 指向
   `https://www.forexfactory.com/calendar`,`is_external=True`。
   - 標題:「ForexFactory Calendar」
   - 標籤:「即時財經日曆」
   - 說明:「篩選高評級(紅色)美元事件,掌握 CPI、NFP、FOMC 等牽動市場的公布時間點。」
4. **Filter 設定步驟**:子標題「Filter 設定」(`size="3"`, `weight="bold"`)+ 5 步驟編號列表,
   每步前面帶一個對應 icon(仿照 `_dashboard_explanation()` 中 icon + 文字橫向排列的寫法):
   1. `sliders-horizontal` — 點選日曆上方的 Filter。
   2. `flame` — Impact:只勾選 High(紅色)。
   3. `dollar-sign` — Currency:優先勾選 USD。
   4. `clock` — 時區設定為你的當地時間,台灣是 GMT+8。
   5. `list-checks` — 每天先看 Today,再看 Tomorrow 以及本週剩餘事件。
5. **數據公布對照表**:子標題「數據公布:偏強 / 偏弱影響對照」+ `rx.table.root`
   (樣式比照 `llm_rankings.py` 的 `rx.table.root(..., variant="surface", width="100%")`,
   外層包一層 `overflow_x="auto"` 的 `rx.box` 以支援窄螢幕橫向捲動)。
   - 欄位:「數據」(`rx.table.column_header_cell`,row header)、「偏強 / 高於預期」、
     「偏弱 / 低於預期」。
   - 9 列資料,見下方「資料內容」。
   - 每一格文字依語意拆成多個 `rx.text.span` 片段上色:
     - 含「利多」「利好」→ `color="var(--green-11)"`。
     - 含「利空」「不利」→ `color="var(--red-11)"`。
     - 其餘中性描述(如「視通膨與利率環境」「可能偏鷹/偏鴿」)→ `color="gray"`。
     - 若同一格同時有利多與利空語意(例如 GDP、Retail Sales 的偏弱欄),拆成兩個
       `rx.text.span` 片段分別上色,而不是整格只選一種顏色。
6. **免責說明**:`rx.callout(..., icon="info", size="1", color_scheme="gray")`,風格比照
   `llm_rankings.py` 底部的 callout:
   「以上對照僅為市場慣例參考,實際影響力需視當下總經環境、市場預期與資金部位而定,
   並非保證走勢,請搭配其他指標綜合判斷。」

## 資料內容(對照表 9 列,逐格標註上色片段)

| 數據 | 偏強 / 高於預期(片段/顏色) | 偏弱 / 低於預期(片段/顏色) |
| --- | --- | --- |
| CPI / Core CPI | 可能利空風險資產(red) | 可能利多風險資產(green) |
| PCE | 可能利空(red) | 可能利多(green) |
| NFP | 視通膨與利率環境(gray) | 視衰退風險(gray) |
| Unemployment | 可能利空降息預期(red) | 可能利多降息,(green) / 但也可能引發衰退擔憂(gray) |
| Retail Sales | 經濟強,但利率可能較高(gray) | 可能利多降息,(green) / 或利空經濟(red) |
| GDP | 可能利好盈利,(green) / 利空降息預期(red) | 可能利多降息,(green) / 或利空成長(red) |
| ISM PMI | 視景氣及通膨分項(gray) | 視衰退與利率預期(gray) |
| JOLTS | 勞動需求強,可能偏鷹(gray) | 勞動需求弱,可能偏鴿(gray) |
| FOMC | 偏鷹通常不利風險資產(red) | 偏鴿通常利多風險資產(green) |

> 註:JOLTS、NFP、ISM PMI 的描述沒有出現「利多/利空/利好/不利」等明確字眼(只有
> 「偏鷹/偏鴿」「視...而定」等條件式描述),依使用者確認的規則維持灰色中性處理,
> 不額外推論成偏多/偏空。

## 資料結構(實作參考,非最終程式碼)

- `FOREX_CALENDAR_SOURCE`:dict,含 `name`/`url`/`tag`/`strength`,供 `_source_card()` 重用。
- `FILTER_STEPS`:`list[tuple[icon: str, text: str]]`,5 筆。
- `ECONOMIC_INDICATORS`:`list[dict]`,每筆含:
  - `metric: str`(數據名稱)
  - `strong: list[tuple[text: str, tone: Literal["up", "down", "neutral"]]]`
  - `weak: list[tuple[text: str, tone: Literal["up", "down", "neutral"]]]`
  - `tone` 對應顏色:`up -> var(--green-11)`、`down -> var(--red-11)`、
    `neutral -> gray`(沿用專案現有「純文字 color="gray"」慣例,而非 `var(--gray-11)`)。

## 錯誤處理 / 邊界情況

- 全部為靜態資料,無外部請求、無載入狀態、無例外處理需求。
- 窄螢幕:對照表外層加 `overflow_x="auto"`,避免表格擠壓版面(與 `llm_rankings.py` 作法一致)。

## 測試

- 純 UI 靜態內容變更,無既有自動化測試涵蓋此類頁面(`news.py`/`llm_rankings.py`/
  `reliable_indicators.py` 目前皆無對應測試)。比照既有慣例,不另外新增測試案例,
  以手動瀏覽頁面(`reflex run` 或既有流程)確認版面與連結正確即可。
