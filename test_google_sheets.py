"""
測試 Google Sheets API 連接
"""

import json
import gspread
from google.oauth2.service_account import Credentials

print("=" * 70)
print(" 測試 Google Sheets API 連接")
print("=" * 70)
print()

# 載入配置
try:
    with open('config/google_sheets_config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    print("✅ 載入配置成功")
except FileNotFoundError:
    print("❌ 找不到 config/google_sheets_config.json")
    exit(1)

# 檢查 Service Account 檔案
service_account_file = config['service_account_file']
try:
    with open(service_account_file, 'r') as f:
        sa_data = json.load(f)
    print(f"✅ 找到 Service Account 檔案")
    print(f"   Project ID: {sa_data.get('project_id')}")
    print(f"   Client Email: {sa_data.get('client_email')}")
    print()
except FileNotFoundError:
    print(f"❌ 找不到 Service Account 檔案: {service_account_file}")
    print()
    print("請按照 GOOGLE_SHEETS_SETUP.md 的步驟：")
    print("1. 前往 Google Cloud Console")
    print("2. 建立 Service Account")
    print("3. 下載 JSON 金鑰")
    print("4. 將檔案移動到 config/google_service_account.json")
    exit(1)

# 檢查 Spreadsheet ID
spreadsheet_id = config.get('spreadsheet_id')
if not spreadsheet_id or spreadsheet_id == "請替換成你的 Spreadsheet ID":
    print("❌ 尚未設定 Spreadsheet ID")
    print()
    print("請按照以下步驟設定：")
    print("1. 建立 Google Sheets：https://sheets.google.com")
    print("2. 分享給 Service Account Email:")
    print(f"   {sa_data.get('client_email')}")
    print("3. 從網址列複製 Spreadsheet ID")
    print("4. 更新 config/google_sheets_config.json 中的 spreadsheet_id")
    exit(1)

print("步驟 1: 連接 Google Sheets API...")

try:
    # 設定權限範圍
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    # 建立憑證
    credentials = Credentials.from_service_account_file(
        service_account_file,
        scopes=SCOPES
    )

    # 連接 Google Sheets
    gc = gspread.authorize(credentials)

    print("✅ Google Sheets API 連接成功")
    print()

    print("步驟 2: 開啟試算表...")

    # 開啟試算表
    spreadsheet = gc.open_by_key(spreadsheet_id)

    print(f"✅ 成功開啟試算表")
    print(f"   名稱: {spreadsheet.title}")
    print(f"   ID: {spreadsheet.id}")
    print(f"   URL: {spreadsheet.url}")
    print()

    print("步驟 3: 寫入測試數據...")

    # 建立或取得測試工作表
    try:
        worksheet = spreadsheet.worksheet("測試")
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title="測試", rows=10, cols=5)

    # 寫入測試數據
    test_data = [
        ["項目", "數值", "狀態"],
        ["連接測試", "成功", "✅"],
        ["時間", "2025-10-22", "✅"],
        ["系統", "Fantasy Basketball 智庫", "✅"]
    ]

    worksheet.update('A1', test_data)

    print("✅ 成功寫入測試數據")
    print()

    print("=" * 70)
    print(" 測試完成！")
    print("=" * 70)
    print()
    print("Google Sheets API 已成功連接並可以寫入數據。")
    print()
    print(f"查看結果：{spreadsheet.url}")
    print()
    print("下一步：執行 sync_to_sheets.py 同步陣容數據")
    print()

except gspread.exceptions.APIError as e:
    print(f"❌ API 錯誤: {e}")
    print()
    print("可能原因：")
    print("1. Spreadsheet ID 不正確")
    print("2. Service Account 沒有權限訪問試算表")
    print()
    print("解決方法：")
    print("1. 確認 Spreadsheet ID 正確")
    print("2. 在 Google Sheets 中點擊「共用」")
    print(f"3. 加入 Service Account Email: {sa_data.get('client_email')}")
    print("4. 權限設為「編輯者」")

except Exception as e:
    print(f"❌ 錯誤: {e}")
    import traceback
    traceback.print_exc()
