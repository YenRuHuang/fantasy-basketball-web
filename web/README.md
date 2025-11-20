# 🏀 Fantasy Basketball Data Center

大亂鬥聯盟數據中心 - 即時查看球隊陣容、統計和賽程

## 📊 功能特色

- ✅ 球員陣容查看（支援下拉選單切換隊伍）
- ✅ 球隊統計（即時計算位置分佈）
- ✅ 完整賽程（Week 1-19）
- ✅ 自動每小時更新
- ✅ 響應式設計（支援手機/平板）

## 🚀 部署到 Zeabur

### 方法 1: 通過 GitHub 部署（推薦）

1. **初始化 Git 倉庫**
   ```bash
   cd web/
   git init
   git add .
   git commit -m "Initial commit: Fantasy Basketball Data Center"
   ```

2. **推送到 GitHub**
   ```bash
   # 在 GitHub 建立新倉庫：fantasy-basketball-web
   git remote add origin https://github.com/YOUR_USERNAME/fantasy-basketball-web.git
   git branch -M main
   git push -u origin main
   ```

3. **在 Zeabur 部署**
   - 前往 [Zeabur Dashboard](https://dash.zeabur.com)
   - 點擊 "Create Project"
   - 選擇 "Deploy from GitHub"
   - 選擇 `fantasy-basketball-web` 倉庫
   - Zeabur 會自動偵測 `zeabur.json` 並部署

4. **設定環境變數** (可選)
   ```
   PORT=8080
   NODE_ENV=production
   ```

5. **取得網址**
   - 部署完成後會得到網址如：`https://fantasy-basketball-xxxxx.zeabur.app`

### 方法 2: 本地測試

```bash
cd web/
npm install
npm start
```

訪問 http://localhost:8080

## 📡 API 端點

- `GET /` - 主頁面
- `GET /health` - 健康檢查
- `GET /api/league-data` - 獲取完整聯盟數據
- `GET /api/roster/:teamId` - 獲取特定隊伍陣容

## 🔄 自動更新

每次執行數據同步後，需要更新部署：

```bash
# 1. 在主目錄執行數據同步
python3 export_for_web.py

# 2. 提交並推送更新
cd web/
git add data/full_league_data.json
git commit -m "Update league data: $(date)"
git push

# Zeabur 會自動重新部署
```

## 🛠 自動化部署腳本

使用 `deploy_to_zeabur.sh` 一鍵部署：

```bash
chmod +x deploy_to_zeabur.sh
./deploy_to_zeabur.sh
```

## 📱 分享給盟友

部署完成後，將網址分享給盟友：

```
🏀 Fantasy 大亂鬥聯盟數據中心

📊 即時查看：
https://fantasy-basketball-xxxxx.zeabur.app

包含：
✅ 聯盟排名 - 即時戰績
✅ 本週對戰 - 當週配對
✅ 完整賽程 - W1-W19 所有對戰
✅ 球員陣容 - 下拉選單查看各隊陣容
✅ 球隊統計 - 下拉選單查看各隊數據

每小時自動更新！
```

## 🔧 技術棧

- **前端**: HTML5, CSS3, JavaScript (Vanilla)
- **後端**: Node.js + Express
- **部署**: Zeabur
- **數據源**: Yahoo Fantasy Sports API

## 📄 授權

MIT License
