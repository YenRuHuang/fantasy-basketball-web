"""
完成 Yahoo OAuth 認證
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

# 授權碼
auth_code = "excg6n2dac2cbcfd2udzbpzmqhgkw65v"

print("=" * 70)
print(" 完成 Yahoo OAuth 認證")
print("=" * 70)
print()
print(f"授權碼: {auth_code}")
print()
print("正在用授權碼換取 access token...")
print()

# 準備請求
token_url = "https://api.login.yahoo.com/oauth2/get_token"

# Basic Auth
auth_string = f"{client_id}:{client_secret}"
auth_bytes = auth_string.encode('ascii')
auth_b64 = base64.b64encode(auth_bytes).decode('ascii')

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

        # 儲存 token
        with open('config/yahoo_token.json', 'w') as f:
            json.dump(token_data, f, indent=2)

        print("✅ OAuth 認證成功！")
        print()
        print("Token 已儲存至: config/yahoo_token.json")
        print()
        print("Token 資訊:")
        print(f"  - Access Token: {token_data['access_token'][:20]}...")
        print(f"  - Refresh Token: {token_data['refresh_token'][:20]}...")
        print(f"  - 有效期限: {token_data['expires_in']} 秒")
        print()
        print("=" * 70)
        print(" 認證完成！現在可以測試連接了")
        print("=" * 70)
        print()
        print("執行: python3 test_connection.py")
        print()

    else:
        print(f"❌ 獲取 token 失敗！")
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.text}")

except Exception as e:
    print(f"❌ 錯誤: {e}")
