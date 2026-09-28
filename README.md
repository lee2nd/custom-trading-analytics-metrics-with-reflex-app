# Reflex Trading Analytics Dashboard

以 Reflex 建置的股票技術分析儀表板。輸入股票代碼與日期區間後，可查看 SMA、EMA、RSI、MACD、布林通道與 ATR 等指標及互動圖表。

## 本機執行 (Docker)

```powershell
docker build -t reflex-trading-dashboard .
docker run --rm -p 7860:7860 reflex-trading-dashboard
```

## 部署到 Reflex Cloud

Reflex Cloud 入口：[https://build.reflex.dev/](https://build.reflex.dev/)。先登入並建立專案，再到專案的 **Deployments** 頁面選擇 **How to deploy**，取得該專案專屬的 CLI 指令。

在本專案根目錄登入並執行部署：

```powershell
reflex login
reflex deploy --project <PROJECT_ID>
```

請以 Reflex Cloud 顯示的專案 ID 取代 `<PROJECT_ID>`；若頁面提供完整部署指令，直接使用該指令即可。部署完成後，公開應用程式網址會顯示在 Reflex Cloud 專案的 **Deployments** 頁面。目前尚未建立線上部署，因此尚無可用的應用程式網址。

官方指南：[Reflex Cloud 部署快速入門](https://reflex.dev/docs/hosting/deploy-quick-start/)。
