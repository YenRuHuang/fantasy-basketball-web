# Fantasy Basketball Analyzer

Yahoo Fantasy Basketball API 整合分析系統 - 專為 9-Cat H2H 聯盟設計

## 功能特色

- **即時數據抓取**: 透過 Yahoo Fantasy Sports API 獲取最新球員數據和聯盟資訊
- **9-Cat 分析**: 專門針對 9 類別 (FG%, FT%, 3PM, PTS, REB, AST, ST, BLK, TO/A/T) 的評分系統
- **陣容優化**: 分析你的陣容在各類別的強弱勢
- **交易分析**: 計算交易前後對各類別的影響
- **每週對戰預測**: 預測下週對戰的勝率

## 專案結構

```
fantasy-basketball-analyzer/
├── src/                    # 核心程式碼
│   ├── api/               # Yahoo API 連接模組
│   ├── analysis/          # 數據分析引擎
│   ├── models/            # 資料模型
│   └── utils/             # 工具函數
├── data/                  # 資料存儲
│   ├── cache/            # API 快取
│   └── exports/          # 匯出報告
├── config/               # 設定檔
│   └── credentials.json  # OAuth 認證資訊 (不提交到 git)
├── notebooks/            # Jupyter 筆記本
└── tests/               # 單元測試
```

## 快速開始

### 1. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 2. 設定 Yahoo API 認證

1. 前往 [Yahoo Developer Network](https://developer.yahoo.com/apps/)
2. 建立新的應用程式
3. 獲取 Client ID 和 Client Secret
4. 將認證資訊填入 `config/credentials.json`

### 3. 執行分析

```bash
python src/main.py
```

## 使用範例

### 獲取聯盟數據

```python
from src.api.yahoo_client import YahooFantasyClient

client = YahooFantasyClient()
league_data = client.get_league_data()
```

### 分析陣容強弱

```python
from src.analysis.roster_analyzer import RosterAnalyzer

analyzer = RosterAnalyzer(your_roster)
strengths = analyzer.get_category_strengths()
```

### 評估交易

```python
from src.analysis.trade_analyzer import TradeAnalyzer

trade = TradeAnalyzer()
impact = trade.evaluate(give=['Player A'], receive=['Player B'])
```

## 技術棧

- **Python 3.9+**
- **yfpy** - Yahoo Fantasy Sports API Wrapper
- **pandas** - 資料分析
- **numpy** - 數值計算
- **matplotlib/seaborn** - 資料視覺化

## 授權

MIT License
