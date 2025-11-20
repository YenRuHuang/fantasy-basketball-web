# 🚀 Fantasy Basketball Data Center - Zeabur 部署指南

完整的自動化部署方案，讓你的盟友可以即時查看聯盟數據

## 📋 已完成的準備工作

✅ 網頁界面（支援下拉選單）
✅ Express API 服務器
✅ Zeabur 配置檔案
✅ Git 倉庫初始化
✅ 自動部署腳本

## 🌐 部署步驟

### 步驟 1: 在 GitHub 建立倉庫

1. 前往 [GitHub](https://github.com/new)
2. 倉庫名稱：`fantasy-basketball-web`
3. 描述：`Fantasy Basketball Data Center - 大亂鬥聯盟數據中心`
4. 選擇：**Public**（或 Private，看你的需求）
5. **不要**勾選 "Initialize this repository with a README"
6. 點擊 "Create repository"

### 步驟 2: 連接到 GitHub

在終端機執行（替換 YOUR_USERNAME 為你的 GitHub 用戶名）：

```bash
cd web/
git remote add origin https://github.com/YOUR_USERNAME/fantasy-basketball-web.git
git branch -M main
git push -u origin main
```

### 步驟 3: 在 Zeabur 部署

1. **前往 Zeabur Dashboard**
   - 網址：https://dash.zeabur.com
   - 登入你的帳號

2. **建立新專案**
   - 點擊 "Create Project"
   - 專案名稱：`fantasy-basketball-web`
   - 區域：選擇最近的（例如：Tokyo）

3. **連接 GitHub 倉庫**
   - 點擊 "Deploy from GitHub"
   - 如果是第一次，需要授權 Zeabur 存取你的 GitHub
   - 選擇倉庫：`fantasy-basketball-web`
   - 分支：`main`

4. **Zeabur 會自動偵測配置**
   - 讀取 `zeabur.json` 配置
   - 執行 `npm install`
   - 執行 `npm start`

5. **等待部署完成**
   - 通常 2-5 分鐘
   - 可以在 Zeabur Dashboard 查看部署日誌

6. **取得網址**
   - 部署完成後會顯示網址
   - 格式：`https://fantasy-basketball-xxxxx.zeabur.app`
   - 或設定自訂域名

## 🔄 自動更新流程

每次聯盟數據更新後，執行一鍵部署：

```bash
cd /Users/murs/Documents/fantasy-basketball-analyzer
./deploy_to_zeabur.sh
```

這個腳本會自動：
1. ✅ 匯出最新聯盟數據
2. ✅ 提交到 Git
3. ✅ 推送到 GitHub
4. ✅ 觸發 Zeabur 自動重新部署

## 📅 整合到自動同步

更新 `auto_sync_league.sh`，讓它自動部署到 Zeabur：

```bash
#!/bin/bash

cd /Users/murs/Documents/fantasy-basketball-analyzer

# 1. 獲取聯盟數據
echo "$(date): 開始獲取聯盟數據..."
python3 get_full_league_data.py >> logs/league_fetch.log 2>&1

# 2. 同步到 Google Sheets
if [ $? -eq 0 ]; then
    echo "$(date): 數據獲取成功，同步到 Google Sheets..."
    python3 sync_league_shared.py >> logs/league_sync.log 2>&1

    # 3. 部署到 Zeabur
    if [ $? -eq 0 ]; then
        echo "$(date): 開始部署到 Zeabur..."
        ./deploy_to_zeabur.sh >> logs/zeabur_deploy.log 2>&1
        echo "$(date): Zeabur 部署完成！"
    fi
fi
```

## 📱 分享給盟友

部署完成後，分享給你的盟友：

```
🏀 Fantasy 大亂鬥聯盟數據中心

📊 即時網頁版：
https://fantasy-basketball-xxxxx.zeabur.app

📋 Google Sheets 版：
https://docs.google.com/spreadsheets/d/1KHS9wNfJ0dItWzj3uvCc63F1e06Hdol-flwxHYxLyjo

特色：
✅ 下拉選單切換隊伍
✅ 即時查看球員陣容
✅ 自動計算球隊統計
✅ Week 1-19 完整賽程
✅ 響應式設計（手機友善）
✅ 每小時自動更新

不需要登入，直接點開就能用！
```

## 🛠 測試部署

在本地測試：

```bash
cd web/
npm install
npm start
```

訪問 http://localhost:8080

## 📊 API 端點

你的網站會提供以下 API：

- `GET /` - 主頁面
- `GET /health` - 健康檢查
- `GET /api/league-data` - 獲取完整聯盟數據 (JSON)
- `GET /api/roster/:teamId` - 獲取特定隊伍陣容

## 🔧 環境變數（可選）

在 Zeabur Dashboard 可以設定：

```env
PORT=8080
NODE_ENV=production
```

## 🎯 優勢

### 對比 Google Sheets：
✅ **可以使用下拉選單**（不需要編輯權限）
✅ **更好的手機體驗**
✅ **自訂樣式和功能**
✅ **完全掌控數據展示**

### Zeabur 優勢：
✅ **免費額度足夠使用**
✅ **自動 HTTPS**
✅ **全球 CDN**
✅ **GitHub 自動部署**
✅ **零設定**

## 🚨 故障排除

### 1. 部署失敗

檢查 Zeabur Dashboard 的部署日誌：
```
Error: Cannot find module 'express'
```

解決：確認 `package.json` 中有 express 依賴

### 2. 數據沒有更新

確認 `data/full_league_data.json` 已更新並推送到 GitHub

### 3. 網頁顯示錯誤

查看瀏覽器 Console：
- F12 → Console
- 檢查是否有 API 請求錯誤

## 📈 下一步

1. ✅ 完成 GitHub 倉庫建立
2. ✅ 部署到 Zeabur
3. ✅ 測試所有功能
4. ✅ 分享給盟友
5. ⚙️ 整合到自動同步腳本
6. 🌐 （可選）設定自訂域名

---

🎉 **恭喜！你的聯盟數據中心即將上線！**

需要協助請參考 Zeabur 文檔：https://zeabur.com/docs
