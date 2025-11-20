"""
Yahoo OAuth 認證設定腳本

手動完成 OAuth 認證流程
"""

from yahoo_oauth import OAuth2
import json

print("=" * 70)
print(" Yahoo Fantasy API OAuth 認證設定")
print("=" * 70)
print()

# 載入認證資訊
with open('config/credentials.json', 'r') as f:
    creds = json.load(f)

client_id = creds['yahoo']['client_id']
client_secret = creds['yahoo']['client_secret']

print("步驟 1: 建立 OAuth 連接...")
print()

# 建立 OAuth 物件
oauth = OAuth2(
    consumer_key=client_id,
    consumer_secret=client_secret,
    redirect_uri='https://localhost:8787'
)

print("步驟 2: 請在瀏覽器中開啟以下網址進行授權：")
print()
print(oauth.get_authorization_url())
print()
print("=" * 70)
print()
print("授權後，瀏覽器會重定向到 https://localhost:8787/?code=XXXXX")
print()
print("請複製整個網址，或只複製 code= 後面的授權碼")
print()

redirect_response = input("請貼上完整的重定向網址或授權碼: ").strip()

# 提取 code
if 'code=' in redirect_response:
    code = redirect_response.split('code=')[1].split('&')[0]
else:
    code = redirect_response

print()
print(f"授權碼: {code[:20]}...")
print()
print("步驟 3: 正在獲取 access token...")

try:
    oauth.get_token_from_code(code)
    print()
    print("✅ OAuth 認證成功！")
    print()
    print("Token 已儲存至 config/ 目錄")
    print()
    print("現在你可以執行: python3 test_connection.py")
    print()

except Exception as e:
    print()
    print(f"❌ 認證失敗: {e}")
    print()
    print("可能的原因:")
    print("1. 授權碼錯誤或已過期")
    print("2. Client ID 或 Client Secret 不正確")
    print("3. Redirect URI 設定不符")
    print()
