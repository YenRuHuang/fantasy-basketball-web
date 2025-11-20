"""
使用提供的驗證碼完成 OAuth 認證
"""

import json
import requests
import base64

# 載入認證資訊
with open('config/credentials.json', 'r') as f:
    creds = json.load(f)

client_id = creds['yahoo']['client_id']
client_secret = creds['yahoo']['client_secret']
redirect_uri = creds['yahoo']['redirect_uri']

# 使用者提供的驗證碼
auth_code = "5zaskuw"

print("=" * 70)
print(" 使用驗證碼完成 Yahoo OAuth 認證")
print("=" * 70)
print()
print(f"驗證碼: {auth_code}")
print()
print("正在獲取 access token...")

# 準備請求
token_url = "https://api.login.yahoo.com/oauth2/get_token"

# Base64 編碼 client credentials
auth_string = f"{client_id}:{client_secret}"
auth_b64 = base64.b64encode(auth_string.encode()).decode()

headers = {
    'Authorization': f'Basic {auth_b64}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {
    'grant_type': 'authorization_code',
    'redirect_uri': redirect_uri,
    'code': auth_code
}

try:
    response = requests.post(token_url, headers=headers, data=data)

    if response.status_code == 200:
        token_data = response.json()

        print("✅ 成功獲取 access token!")
        print()
        print(f"Access Token: {token_data['access_token'][:30]}...")
        print(f"Token Type: {token_data['token_type']}")
        print(f"有效期限: {token_data['expires_in']} 秒")
        print(f"Refresh Token: {token_data['refresh_token'][:30]}...")
        print()

        # 儲存 token
        with open('config/yahoo_token.json', 'w') as f:
            json.dump(token_data, f, indent=2)

        print("Token 已儲存至 config/yahoo_token.json")
        print()
        print("現在可以執行: python3 test_connection.py")
        print()

    else:
        print(f"❌ 錯誤 {response.status_code}")
        print()
        print(response.text)
        print()
        print("可能的原因:")
        print("1. 驗證碼已過期 (需要重新授權)")
        print("2. 驗證碼已被使用")
        print("3. Client ID 或 Secret 不正確")

except Exception as e:
    print(f"❌ 發生錯誤: {e}")
    print()
