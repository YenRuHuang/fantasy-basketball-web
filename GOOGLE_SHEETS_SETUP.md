# Google Sheets 同步設置指南

## 目標
建立像你朋友一樣的 Google Sheets 實時同步系統，自動更新 Yahoo Fantasy Basketball 數據。

---

## 第一步：建立 Google Cloud Project

### 1. 前往 Google Cloud Console
訪問：https://console.cloud.google.com/

### 2. 建立新專案
1. 點擊頂部的專案選單
2. 點擊「新增專案」
3. 專案名稱：`fantasy-basketball-sync`
4. 點擊「建立」

### 3. 啟用 API
在新專案中，啟用以下兩個 API：

**Google Sheets API:**
1. 前往 https://console.cloud.google.com/apis/library/sheets.googleapis.com
2. 確認專案是 `fantasy-basketball-sync`
3. 點擊「啟用」

**Google Drive API:**
1. 前往 https://console.cloud.google.com/apis/library/drive.googleapis.com
2. 點擊「啟用」

---

## 第二步：建立 Service Account

### 1. 建立 Service Account
1. 前往：https://console.cloud.google.com/iam-admin/serviceaccounts
2. 點擊「+ 建立服務帳戶」
3. 填寫資訊：
   - **服務帳戶名稱**: `fantasy-basketball-bot`
   - **服務帳戶 ID**: 自動生成
   - **說明**: `用於同步 Fantasy Basketball 數據到 Google Sheets`
4. 點擊「建立並繼續」
5. 角色選擇：**略過（不需要授予角色）**
6. 點擊「完成」

### 2. 建立 Service Account 金鑰
1. 在服務帳戶列表中，點擊剛建立的 `fantasy-basketball-bot`
2. 切換到「金鑰」分頁
3. 點擊「新增金鑰」→「建立新金鑰」
4. 選擇「JSON」格式
5. 點擊「建立」
6. JSON 檔案會自動下載到你的電腦

### 3. 複製 Service Account Email
在服務帳戶詳情頁面，複製 Email 地址，格式類似：
```
fantasy-basketball-bot@fantasy-basketball-sync.iam.gserviceaccount.com
```

**⚠️ 重要：請記住這個 Email，稍後需要用它來分享 Google Sheets！**

---

## 第三步：設置專案配置

### 1. 將 JSON 金鑰檔案移動到專案目錄
```bash
# 假設下載的檔案在 ~/Downloads/
cd ~/Downloads

# 找到 JSON 檔案（檔名類似 fantasy-basketball-sync-xxxxx.json）
ls -la fantasy-basketball*.json

# 複製到專案 config 目錄
cp fantasy-basketball-sync-*.json /Users/murs/Documents/fantasy-basketball-analyzer/config/google_service_account.json
```

### 2. 驗證檔案
```bash
cd /Users/murs/Documents/fantasy-basketball-analyzer
cat config/google_service_account.json | head -5
```

應該看到類似：
```json
{
  "type": "service_account",
  "project_id": "fantasy-basketball-sync",
  "private_key_id": "xxxxx",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...
```

---

## 第四步：建立 Google Sheets

### 1. 建立新的 Google Sheets
1. 前往 https://sheets.google.com
2. 點擊「空白試算表」
3. 重新命名為：`Fantasy Basketball - 默絲佛陀攝影掃地伯`

### 2. 分享給 Service Account
1. 點擊右上角「共用」按鈕
2. 在「新增使用者和群組」欄位中，貼上 Service Account Email：
   ```
   fantasy-basketball-bot@fantasy-basketball-sync.iam.gserviceaccount.com
   ```
3. 權限選擇：**編輯者**
4. **取消勾選**「通知使用者」（Service Account 不需要通知）
5. 點擊「共用」

### 3. 取得 Spreadsheet ID
從瀏覽器網址列複製 Spreadsheet ID：
```
https://docs.google.com/spreadsheets/d/【這一段就是 ID】/edit
```

例如：
```
https://docs.google.com/spreadsheets/d/1a2B3c4D5e6F7g8H9i0J1k2L3m4N5o6P7q8R9s0T1/edit
```

Spreadsheet ID 就是：`1a2B3c4D5e6F7g8H9i0J1k2L3m4N5o6P7q8R9s0T1`

### 4. 更新配置檔案
編輯 `config/google_sheets_config.json`：
```json
{
  "service_account_file": "config/google_service_account.json",
  "spreadsheet_id": "【貼上你的 Spreadsheet ID】",
  "sheets": {
    "roster": "陣容",
    "stats": "統計",
    "matchup": "對戰",
    "analysis": "分析"
  }
}
```

---

## 第五步：測試連接

### 1. 執行測試腳本
```bash
cd /Users/murs/Documents/fantasy-basketball-analyzer
python3 test_google_sheets.py
```

### 2. 預期結果
如果成功，會看到：
```
✅ Google Sheets API 連接成功
✅ 成功寫入測試數據到工作表「測試」
```

並在你的 Google Sheets 中看到一個新的工作表「測試」，裡面有測試數據。

---

## 第六步：執行完整同步

### 1. 同步陣容數據
```bash
python3 sync_to_sheets.py
```

### 2. 預期結果
Google Sheets 會自動建立以下工作表：
- **陣容**：球員名單、位置、狀態
- **統計**：各項數據統計
- **對戰**：本週對戰預測
- **分析**：策略分析和建議

---

## 自動化同步（可選）

### 每小時自動同步
```bash
# 編輯 crontab
crontab -e

# 加入以下行（每小時執行一次）
0 * * * * cd /Users/murs/Documents/fantasy-basketball-analyzer && /usr/local/bin/python3 sync_to_sheets.py >> logs/sync.log 2>&1
```

### 每天早上 8 點同步
```bash
0 8 * * * cd /Users/murs/Documents/fantasy-basketball-analyzer && /usr/local/bin/python3 sync_to_sheets.py >> logs/sync.log 2>&1
```

---

## 故障排除

### 錯誤 1: "Credentials not found"
**解決方法：**
- 確認 `google_service_account.json` 在 `config/` 目錄下
- 檢查檔案路徑是否正確

### 錯誤 2: "Permission denied"
**解決方法：**
- 確認 Service Account Email 已加入 Google Sheets 的共用名單
- 確認權限是「編輯者」

### 錯誤 3: "Spreadsheet not found"
**解決方法：**
- 檢查 `google_sheets_config.json` 中的 `spreadsheet_id` 是否正確
- 確認 Google Sheets 存在且可訪問

---

## 完成！

現在你的系統就像你朋友的一樣，能夠實時同步 Yahoo Fantasy Basketball 數據到 Google Sheets！

📊 你可以：
1. **隨時查看最新數據**：打開 Google Sheets 就能看到
2. **分享給聯盟成員**：點擊「共用」按鈕邀請其他人查看
3. **手機查看**：用 Google Sheets App 隨時監控
4. **自動更新**：設定 crontab 自動同步

🎉 享受你的 Fantasy Basketball 智庫系統！
