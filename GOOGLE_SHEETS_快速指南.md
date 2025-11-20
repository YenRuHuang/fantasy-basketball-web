# Google Sheets 同步 - 快速指南 ⚡

## 🎯 目標
5 分鐘內完成設置，讓你的 Fantasy Basketball 數據像朋友一樣實時同步到 Google Sheets！

---

## ⚡ 快速開始（3 步驟）

### 第 1 步：建立 Google Service Account（2 分鐘）

1. **開啟 Google Cloud Console**
   https://console.cloud.google.com/

2. **建立專案**
   - 點擊頂部專案選單
   - 點擊「新增專案」
   - 名稱：`fantasy-basketball-sync`
   - 點擊「建立」

3. **啟用 API（兩個）**

   **Google Sheets API:**
   - https://console.cloud.google.com/apis/library/sheets.googleapis.com
   - 點擊「啟用」

   **Google Drive API:**
   - https://console.cloud.google.com/apis/library/drive.googleapis.com
   - 點擊「啟用」

4. **建立 Service Account**
   - https://console.cloud.google.com/iam-admin/serviceaccounts
   - 點擊「+ 建立服務帳戶」
   - 名稱：`fantasy-basketball-bot`
   - 點擊「建立並繼續」→「完成」

5. **下載 JSON 金鑰**
   - 點擊剛建立的 Service Account
   - 切換到「金鑰」分頁
   - 點擊「新增金鑰」→「建立新金鑰」
   - 選擇「JSON」→「建立」
   - 檔案會自動下載

6. **複製 Service Account Email**
   ```
   格式：fantasy-basketball-bot@fantasy-basketball-sync.iam.gserviceaccount.com
   ```
   **📋 請複製這個 Email，等等會用到！**

---

### 第 2 步：設定檔案（1 分鐘）

1. **移動 JSON 檔案**
   ```bash
   # 在終端機執行
   cd ~/Downloads
   cp fantasy-basketball-sync-*.json /Users/murs/Documents/fantasy-basketball-analyzer/config/google_service_account.json
   ```

2. **建立 Google Sheets**
   - 前往 https://sheets.google.com
   - 點擊「空白試算表」
   - 重新命名：`Fantasy Basketball - 默絲佛陀攝影掃地伯`

3. **分享給 Service Account**
   - 點擊右上角「共用」
   - 貼上 Service Account Email（步驟 1.6 複製的）
   - 權限：**編輯者**
   - **取消勾選**「通知使用者」
   - 點擊「共用」

4. **複製 Spreadsheet ID**
   從網址列複製 ID：
   ```
   https://docs.google.com/spreadsheets/d/【這一段】/edit
   ```

5. **更新配置檔案**
   ```bash
   # 編輯配置
   nano config/google_sheets_config.json

   # 將 "請替換成你的 Spreadsheet ID" 改成剛複製的 ID
   # 按 Ctrl+X，然後 Y，然後 Enter 儲存
   ```

---

### 第 3 步：測試同步（30 秒）

```bash
cd /Users/murs/Documents/fantasy-basketball-analyzer

# 測試連接
python3 test_google_sheets.py

# 如果成功，執行完整同步
python3 sync_to_sheets.py
```

**✅ 完成！** 打開你的 Google Sheets，應該會看到：
- 📋 **陣容** 工作表 - 14 位球員清單
- 📊 **統計** 工作表 - 陣容統計摘要
- 💡 **分析** 工作表 - 策略建議

---

## 🚀 日常使用

### 方法 1：一鍵同步（最簡單）
```bash
cd /Users/murs/Documents/fantasy-basketball-analyzer
./quick_sync.sh
```

### 方法 2：手動同步
```bash
# 1. 更新陣容數據
echo "5zaskuw" | python3 get_full_roster_data.py

# 2. 同步到 Google Sheets
python3 sync_to_sheets.py
```

### 方法 3：自動同步（每小時）
```bash
# 編輯 crontab
crontab -e

# 加入這一行（每小時自動同步）
0 * * * * cd /Users/murs/Documents/fantasy-basketball-analyzer && ./quick_sync.sh >> logs/sync.log 2>&1
```

---

## 📱 分享給朋友

1. 打開 Google Sheets
2. 點擊右上角「共用」
3. 輸入朋友的 Email
4. 權限選擇：**檢視者**（他們只能看，不能編輯）
5. 點擊「傳送」

他們就能實時看到你的陣容和分析了！

---

## ❌ 故障排除

### 錯誤：找不到 Service Account 檔案
**檢查：**
```bash
ls -la config/google_service_account.json
```
如果找不到，重新執行第 2 步驟 1。

### 錯誤：Permission denied
**原因：** Service Account 沒有權限

**解決：**
1. 打開 Google Sheets
2. 點擊「共用」
3. 確認 Service Account Email 在名單中
4. 確認權限是「編輯者」

### 錯誤：Spreadsheet not found
**原因：** Spreadsheet ID 不正確

**解決：**
1. 檢查 `config/google_sheets_config.json`
2. 確認 `spreadsheet_id` 正確
3. 重新從網址列複製 ID

---

## 🎉 完成後你會擁有

✅ **實時數據同步** - 像朋友一樣的 Google Sheets 系統
✅ **陣容追蹤** - 14 位球員狀態一目了然
✅ **傷病監控** - 自動標記 GTD 和 INJ
✅ **策略建議** - 交易和陣容優化建議
✅ **移動查看** - 手機隨時查看數據
✅ **聯盟分享** - 炫耀你的數據系統

---

## 🔗 相關文件

- **完整教學**: [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md)
- **系統文件**: [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)
- **使用手冊**: [USER_GUIDE.md](USER_GUIDE.md)

---

**祝你 Fantasy Basketball 季順利！🏀🍀**
