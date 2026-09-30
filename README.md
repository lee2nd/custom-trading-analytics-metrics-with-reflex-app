# Reflex Trading Analytics Dashboard

以 Reflex 建置的股票技術分析儀表板。輸入美股代碼與日期區間後，可查看 SMA、EMA、RSI、MACD、布林通道、ATR、黃金交叉、死亡交叉等指標及互動圖表。

## 本機執行 (Docker，正式版單一映像檔)

```powershell
docker build -t reflex-trading-dashboard .
docker run --rm -p 7860:7860 reflex-trading-dashboard
```

適合驗證最終部署用的映像檔，但每次改程式碼都要重新 `docker build`，不適合日常開發。

## 開發模式 (Docker，熱重載，不用每次重建 image)

```powershell
docker compose -f docker-compose.dev.yml up --build   # 第一次要 build 相依套件層
docker compose -f docker-compose.dev.yml up            # 之後開回來，改 .py 檔會自動熱重載
docker compose -f docker-compose.dev.yml down          # 停止
```

前端：http://localhost:3000　後端：http://localhost:8000。只有 `Dockerfile` 或 `requirements.txt` 改變時才需要加 `--build`。

## 部署到 Reflex Cloud

### 自動部署（推薦）：push 到 `main` 自動佈署

[.github/workflows/deploy.yml](.github/workflows/deploy.yml) 會在每次 push 到 `main` 時自動執行測試並部署到 Reflex Cloud，部署目標是同一個 `--project`，所以**網址不會變**。

一次性設定（在 GitHub repo 的 **Settings → Secrets and variables → Actions** 新增）：

1. `REFLEX_PROJECT_ID`：Reflex Cloud 專案 ID（到 Reflex Cloud 專案頁面的 **Deployments → How to deploy** 可以找到，就是目前手動指令裡的 `<PROJECT_ID>`）。
2. `REFLEX_ACCESS_TOKEN`：CI 專用的存取權杖，**不要用個人登入 session**。產生方式二選一：
   - Reflex Cloud 網頁：Organization → **Tokens** → **Create Token**，範本選 **Deploy**，專案範圍選這個專案，設定到期日。
   - 或用 CLI：`reflex login` 後執行 `reflex cloud create-token "github-actions" --duration 90`（最長 90 天，到期前要重新產生並更新 secret）。

設好這兩個 secrets 後，之後只要 `git push` 到 `main`，GitHub Actions 就會自動測試＋部署，不用再手動貼指令。可以到 repo 的 **Actions** 分頁看部署進度與 log。

### 手動部署

Reflex Cloud 入口：[https://build.reflex.dev/](https://build.reflex.dev/)。先登入並建立專案，再到專案的 **Deployments** 頁面選擇 **How to deploy**，取得該專案專屬的 CLI 指令。

在本專案根目錄登入並執行部署：

```powershell
cd D:\pythonworkspace\custom-trading-analytics-metrics-with-reflex-app
.\.venv\Scripts\Activate.ps1
reflex login
reflex deploy --project <PROJECT_ID>
```

請以 Reflex Cloud 顯示的專案 ID 取代 `<PROJECT_ID>`；若頁面提供完整部署指令，直接使用該指令即可。部署完成後，公開應用程式網址會顯示在 Reflex Cloud 專案的 **Deployments** 頁面。

官方指南：[Reflex Cloud 部署快速入門](https://reflex.dev/docs/hosting/deploy-quick-start/)、[Tokens](https://reflex.dev/docs/hosting/tokens/)。
