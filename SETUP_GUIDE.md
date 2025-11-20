# Fantasy Basketball Analyzer 設定指南

## 步驟 1: 安裝 Python 依賴套件

```bash
cd /Users/murs/Documents/fantasy-basketball-analyzer
pip install -r requirements.txt
```

## 步驟 2: 設定 Yahoo Developer 應用程式

### 2.1 建立 Yahoo App

1. 前往 [Yahoo Developer Network](https://developer.yahoo.com/apps/)
2. 點擊 "Create an App"
3. 填寫應用程式資訊:
   - **Application Name**: Fantasy Basketball Analyzer (或任何名稱)
   - **Application Type**: Web Application
   - **Redirect URI(s)**: `oob` (out-of-band)
   - **API Permissions**: 勾選 "Fantasy Sports" 並選擇 "Read"

4. 建立後，你會獲得:
   - **Client ID** (Consumer Key)
   - **Client Secret** (Consumer Secret)

### 2.2 設定認證檔案

複製範例設定檔並填入你的認證資訊:

```bash
cp config/credentials.example.json config/credentials.json
```

編輯 `config/credentials.json`:

```json
{
  "yahoo": {
    "client_id": "你的_CLIENT_ID",
    "client_secret": "你的_CLIENT_SECRET",
    "redirect_uri": "oob"
  },
  "league": {
    "league_id": "你的_聯盟_ID",
    "season": "2025",
    "game_code": "nba"
  }
}
```

### 2.3 取得聯盟 ID

你的聯盟 ID 可以在 Yahoo Fantasy Basketball 網址中找到:

```
https://basketball.fantasysports.yahoo.com/nba/XXXXX
                                                ^^^^^
                                              這就是你的聯盟 ID
```

## 步驟 3: OAuth 認證

第一次執行時，系統會要求你進行 OAuth 認證:

```bash
python src/main.py
```

1. 系統會顯示一個 Yahoo 授權網址
2. 在瀏覽器中開啟該網址
3. 登入你的 Yahoo 帳號並授權應用程式
4. 複製授權碼 (authorization code)
5. 貼回終端機

認證成功後，認證 token 會儲存在 `config/` 目錄，之後就不需要重新認證了。

## 步驟 4: 測試連接

執行測試腳本確認一切正常:

```bash
python src/api/yahoo_client.py
```

如果成功，你會看到:

```
Yahoo Fantasy API 連接成功！
聯盟名稱: [你的聯盟名稱]
隊伍數量: 14
```

## 常見問題

### Q1: 出現 "FileNotFoundError: 找不到認證檔案"

**解決方法**: 確認你已經建立 `config/credentials.json` 並填入正確資訊

### Q2: OAuth 認證失敗

**可能原因**:
- Client ID 或 Client Secret 錯誤
- Yahoo App 的 Redirect URI 設定不是 "oob"
- 沒有勾選 Fantasy Sports API 權限

### Q3: 無法獲取聯盟數據

**可能原因**:
- 聯盟 ID 錯誤
- 你的 Yahoo 帳號沒有加入該聯盟
- 聯盟設定為私人且你不是成員

### Q4: Token 過期

**解決方法**:
- 刪除 `config/` 目錄下的 token 檔案
- 重新執行程式並完成 OAuth 認證

## 下一步

設定完成後，你可以:

1. **分析你的陣容**
   ```bash
   python src/main.py
   # 選擇選項 2
   ```

2. **評估交易**
   ```bash
   python src/main.py
   # 選擇選項 3
   ```

3. **查看球員排名**
   ```bash
   python src/main.py
   # 選擇選項 4
   ```

## 進階使用

### 自訂類別權重

編輯 `src/analysis/category_scorer.py` 中的 `DEFAULT_WEIGHTS`:

```python
DEFAULT_WEIGHTS = {
    'FG%': 1.5,  # 提高 FG% 的權重
    'FT%': 1.0,
    '3PM': 1.2,  # 提高三分球的權重
    # ...
}
```

### 建立自動化報告

使用 Jupyter Notebook 建立自訂分析:

```bash
jupyter notebook notebooks/
```

## 需要幫助？

- 查看 [Yahoo Fantasy Sports API 官方文檔](https://developer.yahoo.com/fantasysports/guide/)
- 查看 [yfpy 套件文檔](https://yfpy.uberfastman.com/)
- 提交 Issue 或問題
