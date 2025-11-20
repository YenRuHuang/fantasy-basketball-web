"""
生成 Yahoo OAuth 授權網址
"""

import json

# 載入認證資訊
with open('config/credentials.json', 'r') as f:
    creds = json.load(f)

client_id = creds['yahoo']['client_id']
redirect_uri = creds['yahoo']['redirect_uri']

# 生成授權網址
auth_url = f"https://api.login.yahoo.com/oauth2/request_auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&language=en-us"

print("=" * 80)
print(" Yahoo Fantasy API OAuth 授權")
print("=" * 80)
print()
print("請在瀏覽器中開啟以下網址進行授權：")
print()
print(auth_url)
print()
print("=" * 80)
print()
print("授權後，瀏覽器會重定向到:")
print(f"{redirect_uri}/?code=XXXXXX")
print()
print("請複製網址列中 'code=' 後面的授權碼")
print("然後執行: python3 complete_auth.py 並貼上授權碼")
print()
