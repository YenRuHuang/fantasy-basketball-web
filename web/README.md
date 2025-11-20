# 蛇星刁手 Fantasy Basketball Data Center

Yahoo Fantasy Basketball 蛇星刁手聯盟的數據中心網頁版。

## 功能特色

- 📊 **聯盟排名** - 即時排名和戰績
- 🏀 **本週對戰** - 當前週次對戰組合
- 📅 **完整賽程** - Week 1-22 完整對戰表
- 👥 **球員陣容** - 各隊球員名單（下拉選單）
- 📈 **球隊統計** - 勝率和詳細數據
- ℹ️ **聯盟資訊** - 基本聯盟資料

## 手機優化

- ✅ 響應式設計，完美支援手機瀏覽
- ✅ 卡片式佈局（手機版排名頁面）
- ✅ 分頁滑動提示（手機版）
- ✅ 觸控優化滾動

## 部署方式

### 1. 建立 GitHub 倉庫

在 GitHub 建立新倉庫，例如：`snakestar-basketball-web`

### 2. 連接到遠端倉庫

```bash
cd /Users/murs/Documents/fantasy-basketball-snakestar/web
git remote add origin https://github.com/YourUsername/snakestar-basketball-web.git
git branch -M main
git add .
git commit -m "Initial commit: 蛇星刁手 Data Center"
git push -u origin main
```

### 3. Zeabur 部署

1. 登入 [Zeabur Dashboard](https://dash.zeabur.com)
2. 點擊 "New Project"
3. 選擇 "Deploy from GitHub"
4. 選擇你的倉庫：`snakestar-basketball-web`
5. Zeabur 會自動偵測 Node.js 環境並部署
6. 在 "Generate Domain" 設定公開網址（例如：snakestar-basketball）

### 4. 自動更新

每次執行 `auto_sync_league.sh` 時會：
1. 獲取最新 Yahoo Fantasy 數據
2. 同步到 Google Sheets
3. 推送到 GitHub → 觸發 Zeabur 自動部署

## API 端點

- `GET /` - 主頁面
- `GET /health` - 健康檢查
- `GET /api/league-data` - 完整聯盟數據
- `GET /api/roster/:teamId` - 特定隊伍陣容

## 技術架構

- **後端**: Express.js
- **前端**: Vanilla JavaScript (無框架)
- **樣式**: CSS (Noto Sans TC 字體)
- **部署**: Zeabur (Node.js)
- **資料來源**: Yahoo Fantasy Sports API

## 聯盟資訊

- **聯盟名稱**: 蛇星刁手
- **League ID**: 30947
- **賽季**: 2024-25 NBA Season

---

Last updated: 2025-10-22
