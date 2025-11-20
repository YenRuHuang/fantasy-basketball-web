# 🏀 Fantasy Basketball Analyzer - 快速參考

## ⚡ 常用命令

```bash
# 進入專案目錄
cd /Users/murs/Documents/fantasy-basketball-analyzer

# 執行主程式
python3 src/main.py

# 測試 API 連接
python3 test_api.py

# 重新授權 (Token 過期時)
python3 get_auth_url.py  # 取得授權網址
python3 complete_auth.py # 完成授權
```

---

## 📊 主程式選單

| 選項 | 功能 | 使用時機 |
|------|------|----------|
| **1** | 獲取聯盟數據 | 查看排名、當前週次 |
| **2** | **分析陣容** ⭐ | 每週必用！查看優劣勢 |
| **3** | **評估交易** ⭐ | 有交易提議時 |
| **4** | 球員排名 | 選秀、撿 FA 時參考 |
| **0** | 退出 | - |

---

## 🎯 你的陣容快速分析

### 當前陣容 (12人)

**健康球員 (10人):**
1. Giannis Antetokounmpo ($69) - 核心
2. Chet Holmgren ($38) - 火鍋+籃板
3. Donovan Mitchell ($42) - 得分王
4. Bradley Beal ($5) - 超值
5. Jalen Suggs ($9) - 防守
6. Jaden McDaniels ($2) - 3D
7. Yves Missi ($2) - 新秀中鋒
8. Lonzo Ball ($1) - ⚠️ 低 FG%
9. Cameron Johnson ($7, Keep) - 側翼
10. Andrew Nembhard ($7, Keep) - 控衛

**傷兵 (2人):**
11. Kyrie Irving ($4) - 下半季回歸
12. Jayson Tatum ($14) - 明年 Keep

---

### ✅ 你的優勢類別 (5個)

| 類別 | 說明 | 核心球員 |
|------|------|----------|
| **3PM** | 三分球 | Mitchell 230, Beal 140, Suggs 136 |
| **FT%** | 罰球率 | Beal .850, Suggs .832, Mitchell .697 |
| **ST** | 抄截 | Mitchell 76, Giannis 70, Suggs 46 |
| **A/T** | 助攻失誤比 | Nembhard, Lonzo 3.0 |
| **PTS** | 得分 | Giannis, Mitchell, Beal |

---

### ❌ 你的劣勢類別 (3個)

| 類別 | 說明 | 問題 |
|------|------|------|
| **FG%** | 投籃命中率 | Lonzo .385, Suggs .442 拖累 |
| **REB** | 籃板 | 只有 Giannis + Chet |
| **DD** | 雙十 | 只有 Giannis 穩定 |

---

## 💡 快速決策指南

### 場景 1: 有人提出交易

**步驟：**
1. `python3 src/main.py` → 選 `3`
2. 輸入交易內容
3. 看系統建議

**判斷標準：**
- ✅ Accept: 改善類別 > 損失類別
- ⚠️ Consider: 改善 = 損失，但補強了弱項
- ❌ Reject: 損失類別 > 改善類別

---

### 場景 2: 自由球員撿人

**推薦撿的類型：**
- 高 FG% 中鋒 (.55+)
- 籃板機器 (10+ RPG)
- 火鍋專家 (1.5+ BPG)

**該放掉的球員：**
- Lonzo Ball (.385 FG% 是毒藥)
- 低效率後衛

---

### 場景 3: 週對戰預測

**勝率公式：**
```
你的優勢類別 ≥ 5 → 贏面大 (70%+)
你的優勢類別 = 4 → 五五開 (50%)
你的優勢類別 ≤ 3 → 危險 (30%-)
```

**你的情況：** 5 個優勢類別 → 穩定贏球！

---

## 🔧 常見問題速查

### Token 過期
```bash
python3 get_auth_url.py
# 瀏覽器授權後...
python3 complete_auth.py
```

### 系統建議交易
```
建議: 用 Tatum 換 Jaren Jackson Jr.
理由: 補強 BLK，讓優勢類別從 5 個變 6 個
```

### 我的策略
```
✅ 主打: 外線流 (3PM, FT%, PTS)
✅ 搭配: 防守 (ST, A/T)
❌ 放棄: FG%, REB, DD (Punt 策略)
```

---

## 📈 系統評分標準

### Z-Score 解讀

| Z-Score | 等級 | 說明 |
|---------|------|------|
| > 2.0 | 神級 | 聯盟前 5% |
| 1.0 ~ 2.0 | 優秀 | 前 15% |
| 0.5 ~ 1.0 | 良好 | 前 30% |
| -0.5 ~ 0.5 | 平均 | 中游 |
| -1.0 ~ -0.5 | 偏弱 | 後 30% |
| < -1.0 | 很弱 | 後 15% (Punt) |

---

## 🎯 本週行動清單

### 週一
- [ ] 執行陣容分析
- [ ] 查看本週對手
- [ ] 評估勝算

### 週三
- [ ] 檢查傷病報告
- [ ] 調整先發陣容

### 週五
- [ ] 查看自由球員市場
- [ ] 考慮是否撿人

### 週日
- [ ] 分析本週表現
- [ ] 規劃下週策略

---

## 🚨 緊急聯絡

遇到問題？

1. 查看 `USER_GUIDE.md` 詳細教學
2. 查看 `SETUP_GUIDE.md` 設定問題
3. 查看 `README.md` 專案說明

---

**記住：系統只是工具，你才是決策者！** 🏆
