# 🏀 Fantasy Basketball Analyzer - 快速開始

## 系統已經為你建立好了！

你現在有一個完整的 Yahoo Fantasy Basketball API 分析系統，包含：

### ✅ 已完成的功能：

1. **Yahoo API 連接模組** (`src/api/`)
   - 自動化 OAuth 認證
   - 獲取聯盟、球員、陣容數據
   - 獲取對戰和計分板資訊

2. **9-Cat 評分系統** (`src/analysis/category_scorer.py`)
   - Z-Score 球員價值計算
   - 類別權重自定義
   - 球員排名系統

3. **陣容分析器** (`src/analysis/roster_analyzer.py`)
   - 識別優勢/劣勢類別
   - Punt 策略建議
   - 改善方向推薦

4. **交易分析器** (`src/analysis/trade_analyzer.py`)
   - 評估交易對各類別的影響
   - 計算總價值變化
   - 智能交易建議

5. **完整的資料模型** (`src/models/`)
   - Player, Roster, PlayerStats
   - CategoryStats 計算引擎

---

## 📋 立即開始使用

### 第一步：安裝依賴

```bash
cd /Users/murs/Documents/fantasy-basketball-analyzer
pip install -r requirements.txt
```

### 第二步：設定 Yahoo API

1. **建立 Yahoo Developer App**
   - 訪問: https://developer.yahoo.com/apps/
   - 點擊 "Create an App"
   - API Permissions: 勾選 "Fantasy Sports (Read)"
   - Redirect URI: 填入 `oob`

2. **填寫認證資訊**

```bash
cp config/credentials.example.json config/credentials.json
```

編輯 `config/credentials.json`，填入你的:
- `client_id`: Yahoo App 的 Client ID
- `client_secret`: Yahoo App 的 Client Secret
- `league_id`: 你的聯盟 ID (從 Yahoo 網址取得)

### 第三步：執行程式

```bash
cd /Users/murs/Documents/fantasy-basketball-analyzer
python src/main.py
```

第一次執行會要求 OAuth 認證：
1. 瀏覽器會開啟 Yahoo 授權頁面
2. 登入並授權
3. 複製授權碼貼回終端機
4. 完成！

---

## 🎯 主要功能使用

### 1️⃣ 分析你的陣容

```bash
python src/main.py
# 選擇選項 2
```

這會顯示：
- ✅ 你在哪些類別有優勢 (Strong)
- ❌ 你在哪些類別太弱 (Punt)
- 📊 各類別的 Z-Score 分數
- 💡 改善建議

### 2️⃣ 評估交易

```bash
python src/main.py
# 選擇選項 3
```

輸入交易方案後會顯示：
- 📈 哪些類別會變強
- 📉 哪些類別會變弱
- ✅ 建議 Accept / Reject
- 🎯 總價值變化

### 3️⃣ 查看球員排名

```bash
python src/main.py
# 選擇選項 4
```

這會顯示基於 Z-Score 的球員價值排名。

---

## 🔧 進階使用

### 自定義分析 (Jupyter Notebook)

```bash
jupyter notebook notebooks/example_analysis.py
```

這個 Notebook 包含：
- 完整的數據獲取流程
- 視覺化圖表
- 交易模擬
- 報告匯出

### 程式化使用

```python
from src.api.yahoo_client import YahooFantasyClient
from src.analysis.roster_analyzer import RosterAnalyzer

# 連接 API
client = YahooFantasyClient()

# 獲取你的陣容
my_roster = client.get_team_roster()

# 分析陣容
analyzer = RosterAnalyzer(my_roster)
report = analyzer.get_roster_report()

print(report['strategic_summary'])
```

---

## 📊 你的實際陣容分析

基於你之前分享的陣容，讓我用這個系統分析：

### 你的陣容 (12人):
- Giannis Antetokounmpo ($69)
- Chet Holmgren ($38)
- Donovan Mitchell ($42)
- Bradley Beal ($5)
- Jalen Suggs ($9)
- Jaden McDaniels ($2)
- Kyrie Irving ($4, 傷兵)
- Yves Missi ($2)
- Lonzo Ball ($1)
- Cameron Johnson ($7, Keep)
- Andrew Nembhard ($7, Keep)
- Jayson Tatum ($14, 傷兵)

### 系統會自動分析：

**優勢類別 (預期):**
- ✅ 3PM (Mitchell 230, Beal 140, Suggs 136)
- ✅ FT% (Beal .850, Suggs .832)
- ✅ ST (Mitchell 76, Giannis 70, Suggs 46)
- ✅ A/T (Nembhard, Lonzo 3.0)
- ✅ PTS (Giannis, Mitchell, Beal)

**劣勢類別 (Punt):**
- ❌ FG% (Lonzo .385, Suggs .442 拖累)
- ❌ REB (只有 Giannis + Chet)
- ❌ DD (只有 Giannis)

**系統建議:**
1. 用 Tatum (傷兵) 換取火鍋專家 (Walker Kessler, Jaren Jackson Jr.)
2. 交易 Lonzo (.385 FG%) 換高效率中鋒
3. 等 Kyrie 下半季復出補強陣容深度

---

## 🚀 接下來做什麼？

### 立即行動：

1. **安裝套件** (2分鐘)
   ```bash
   pip install -r requirements.txt
   ```

2. **設定 Yahoo API** (5分鐘)
   - 建立 Yahoo App
   - 填寫 credentials.json

3. **執行第一次分析** (1分鐘)
   ```bash
   python src/main.py
   ```

4. **查看你的陣容報告**
   - 看看系統分析是否準確
   - 獲得交易建議

### 長期使用：

- **每週更新**: 執行程式獲取最新數據
- **交易評估**: 有人提出交易時立即分析
- **自由球員**: 看看哪些 FA 值得撿
- **對戰預測**: 分析下週對手的弱點

---

## 📚 完整文檔

- **設定指南**: `SETUP_GUIDE.md`
- **README**: `README.md`
- **程式碼**: `src/` 目錄

---

## ❓ 需要幫助？

如果遇到問題：

1. 檢查 `SETUP_GUIDE.md` 的常見問題
2. 確認 Yahoo API 認證設定正確
3. 查看 Yahoo Fantasy API 官方文檔

---

## 🎉 開始分析你的陣容吧！

```bash
cd /Users/murs/Documents/fantasy-basketball-analyzer
pip install -r requirements.txt
python src/main.py
```

Good luck with your Fantasy Basketball season! 🏀🔥
