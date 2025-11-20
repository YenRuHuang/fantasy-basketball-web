# Fantasy Basketball 終極智庫系統 🏀

## 系統簡介

這是一個完整的 Fantasy Basketball 分析和管理系統，為你的聯盟「大亂鬥」(ID# 71325) 和隊伍「默絲佛陀攝影掃地伯」量身打造。

**核心功能：**
✅ Yahoo Fantasy API 實時數據獲取
✅ Google Sheets 自動同步（像你朋友一樣！）
✅ 每週策略分析報告
✅ 智能交易建議
✅ 傷病追蹤和陣容優化

---

## 🚀 快速開始

### 立即使用（已完成設定）

```bash
cd /Users/murs/Documents/fantasy-basketball-analyzer

# 1. 查看陣容狀態
python3 get_full_roster_data.py

# 2. 生成週報告
python3 my_weekly_report.py

# 3. 同步到 Google Sheets（需先完成 Google 設定）
python3 sync_to_sheets.py
```

### 首次設定 Google Sheets（5 分鐘）

📖 閱讀快速指南：[GOOGLE_SHEETS_快速指南.md](GOOGLE_SHEETS_快速指南.md)

簡要步驟：
1. 建立 Google Service Account
2. 下載 JSON 金鑰 → 移動到 `config/google_service_account.json`
3. 建立 Google Sheets 並分享給 Service Account
4. 執行 `python3 test_google_sheets.py` 測試
5. 執行 `python3 sync_to_sheets.py` 完整同步

---

## 📁 系統架構

```
fantasy-basketball-analyzer/
├── config/                          # 配置文件
│   ├── credentials.json            # Yahoo API 認證（已設定✅）
│   ├── yahoo_token.json            # OAuth Token（已獲取✅）
│   ├── google_service_account.json # Google Service Account（需設定）
│   └── google_sheets_config.json   # Google Sheets 配置
│
├── data/                           # 數據文件
│   ├── my_roster_full.json        # 你的陣容數據（已獲取✅）
│   └── cache/                     # 緩存目錄
│
├── src/                           # 核心程式碼
│   ├── api/                       # API 連接
│   │   └── yahoo_client.py       # Yahoo API 客戶端
│   ├── models/                    # 數據模型
│   │   ├── player.py             # 球員模型
│   │   ├── roster.py             # 陣容模型
│   │   └── stats.py              # 統計模型
│   ├── analysis/                  # 分析引擎
│   │   ├── roster_analyzer.py    # 陣容分析
│   │   ├── trade_analyzer.py     # 交易分析
│   │   ├── matchup_predictor.py  # 對戰預測
│   │   └── trade_targets.py      # 交易目標推薦
│   ├── integrations/              # 第三方整合
│   │   └── google_sheets_sync.py # Google Sheets 同步
│   └── automation/                # 自動化
│       └── weekly_report.py      # 週報告生成器
│
├── 主要腳本
│   ├── get_full_roster_data.py   # 獲取陣容數據（✅ 可用）
│   ├── my_weekly_report.py       # 生成週報告（✅ 可用）
│   ├── test_google_sheets.py     # 測試 Google Sheets
│   ├── sync_to_sheets.py         # 同步到 Google Sheets
│   └── quick_sync.sh             # 一鍵同步腳本
│
└── 文件
    ├── README_完整系統總覽.md          # 本文件
    ├── GOOGLE_SHEETS_快速指南.md      # Google Sheets 快速設定
    ├── GOOGLE_SHEETS_SETUP.md        # Google Sheets 完整教學
    ├── ADVANCED_FEATURES.md          # 進階功能說明
    └── USER_GUIDE.md                 # 使用手冊
```

---

## ✅ 已完成功能

### 1. Yahoo Fantasy API 連接 ✅
- **狀態**: 已完成並測試成功
- **聯盟**: 大亂鬥 (ID# 71325)
- **隊伍**: 默絲佛陀攝影掃地伯 (Team ID: 1)
- **數據**: 已獲取 14 位球員完整資料

**你的陣容：**
- ✅ 11 名健康球員
- ⚠️ 1 名 GTD (Jalen Suggs)
- ❌ 2 名 INJ (Jayson Tatum, Kyrie Irving)

### 2. 週報告系統 ✅
- **檔案**: `my_weekly_report.py`
- **功能**:
  - 陣容狀態分析
  - 核心球員評估
  - 優劣勢診斷
  - 行動計畫（高/中/低優先級）
  - 4 個交易建議方案
  - 每日/每週檢查清單

**執行**:
```bash
python3 my_weekly_report.py
```

### 3. Google Sheets 同步系統 ✅
- **狀態**: 程式碼已完成，等待你設定 Service Account
- **功能**:
  - 自動同步陣容數據
  - 統計摘要
  - 分析建議
  - 自動格式化（顏色、粗體）

**設定指南**: [GOOGLE_SHEETS_快速指南.md](GOOGLE_SHEETS_快速指南.md)

---

## 🎯 當前陣容診斷

### 核心球員（Top 6）
1. ✅ **Giannis Antetokounmpo** (MIL, PF) - MVP 級別
2. ❌ **Jayson Tatum** (BOS, SF) - INJ ⚠️ 需處理
3. ❌ **Kyrie Irving** (DAL, PG) - INJ ⚠️ 需處理
4. ✅ **Donovan Mitchell** (CLE, PG) - 得分手
5. ✅ **Chet Holmgren** (OKC, PF) - 年輕潛力
6. ✅ **Bradley Beal** (LAC, SG) - 穩定得分

### 陣容問題
🔴 **緊急**: 2 名核心球員受傷 (Tatum, Kyrie)
🔴 **位置失衡**: 6 名 PG，僅 1 名 C
🟡 **深度不足**: 中鋒位置薄弱

### 推薦交易
1. **送出**: Tatum + Westbrook → **換來**: Anthony Davis
2. **送出**: Kyrie + Lonzo → **換來**: Vucevic + Lopez
3. **送出**: Lonzo + Filipowski → **換來**: Sabonis

---

## 📊 使用場景

### 每日例行（1 分鐘）
```bash
# 檢查陣容更新
echo "5zaskuw" | python3 get_full_roster_data.py
```

### 每週分析（2 分鐘）
```bash
# 生成完整週報告
python3 my_weekly_report.py
```

### 分享給聯盟（3 分鐘）
```bash
# 同步到 Google Sheets
python3 sync_to_sheets.py

# 或使用一鍵腳本
./quick_sync.sh
```

### 自動化（一次設定）
```bash
# 編輯 crontab
crontab -e

# 每小時自動同步
0 * * * * cd /Users/murs/Documents/fantasy-basketball-analyzer && ./quick_sync.sh >> logs/sync.log 2>&1
```

---

## 🔑 重要檔案說明

### 配置文件

**`config/credentials.json`** - Yahoo API 認證
```json
{
  "yahoo": {
    "client_id": "dj0yJmk9...",
    "client_secret": "d8f64ef...",
    "redirect_uri": "https://localhost:8787"
  },
  "league": {
    "league_id": "71325",
    "season": "2025",
    "game_code": "nba"
  }
}
```
✅ 已設定，不需更改

**`config/google_sheets_config.json`** - Google Sheets 配置
```json
{
  "service_account_file": "config/google_service_account.json",
  "spreadsheet_id": "請替換成你的 Spreadsheet ID",
  ...
}
```
⚠️ 需要設定 `spreadsheet_id`

### 數據文件

**`data/my_roster_full.json`** - 你的陣容數據
```json
{
  "team_name": "默絲佛陀攝影掃地伯",
  "team_id": 1,
  "week": 1,
  "players": [...]
}
```
✅ 已獲取，每次執行 `get_full_roster_data.py` 會更新

---

## 🛠️ 故障排除

### Yahoo API 連接問題
```bash
# 重新獲取 token
python3 complete_auth_with_code.py
```

### Google Sheets 連接問題
```bash
# 測試連接
python3 test_google_sheets.py

# 檢查配置
cat config/google_sheets_config.json
ls -la config/google_service_account.json
```

### 陣容數據過時
```bash
# 手動更新
echo "5zaskuw" | python3 get_full_roster_data.py
```

---

## 📚 進階功能

### 1. 對戰預測
`src/analysis/matchup_predictor.py` - 預測每週對戰結果

### 2. 交易分析器
`src/analysis/trade_analyzer.py` - 評估交易前後陣容變化

### 3. 交易目標推薦
`src/analysis/trade_targets.py` - 根據弱點推薦交易目標

### 4. 自動化週報告
`src/automation/weekly_report.py` - 整合所有分析的完整報告

**詳細說明**: [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)

---

## 🎓 學習資源

### 新手入門
1. [USER_GUIDE.md](USER_GUIDE.md) - 基本使用教學
2. [GOOGLE_SHEETS_快速指南.md](GOOGLE_SHEETS_快速指南.md) - Google Sheets 設定

### 進階使用
1. [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md) - 所有進階功能
2. [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) - 詳細設定步驟

---

## 🆚 與朋友系統比較

| 功能 | 你的系統 | 朋友的系統 |
|------|---------|-----------|
| Yahoo API 連接 | ✅ | ✅ |
| Google Sheets 同步 | ✅ | ✅ |
| 陣容追蹤 | ✅ | ✅ |
| 傷病監控 | ✅ | ✅ |
| **策略分析** | ✅ | ❌ |
| **交易建議** | ✅ | ❌ |
| **對戰預測** | ✅ | ❌ |
| **自動化報告** | ✅ | ❌ |
| **本地運行** | ✅ | ❌ |

**你的系統更強大！** 🚀

---

## 💡 下一步建議

### 立即可做
1. ✅ 執行 `python3 my_weekly_report.py` 查看本週分析
2. ⏳ 完成 Google Sheets 設定（5 分鐘）
3. ⏳ 執行第一次同步 `python3 sync_to_sheets.py`

### 本週內
1. 處理 Jayson Tatum 傷病問題
2. 評估 Kyrie Irving 交易價值
3. 監控 Jalen Suggs 復出狀態
4. 在 Waiver Wire 尋找高 FG% 球員

### 長期優化
1. 設定自動同步（crontab）
2. 建立交易評估流程
3. 追蹤每週數據趨勢
4. 優化 Punt 策略

---

## 🎉 系統已就緒！

你現在擁有一個比朋友更強大的 Fantasy Basketball 管理系統！

**已完成：**
✅ Yahoo API 連接
✅ 陣容數據獲取
✅ 週報告生成
✅ Google Sheets 同步程式（等待設定）

**立即使用：**
```bash
cd /Users/murs/Documents/fantasy-basketball-analyzer
python3 my_weekly_report.py
```

**祝你本季稱霸聯盟！** 🏆🏀

---

**需要幫助？**
- 查看文件：[docs/](docs/)
- 檢查配置：`config/`
- 查看數據：`data/`

**系統版本**: 1.0
**最後更新**: 2025-10-22
**建立者**: Claude Code + 你
