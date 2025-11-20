"""
測試 Yahoo Fantasy API 連接 (使用已獲取的 token)
"""

import json
import requests

# 載入認證資訊
with open('config/credentials.json', 'r') as f:
    creds = json.load(f)

# 載入 token
with open('config/yahoo_token.json', 'r') as f:
    token_data = json.load(f)

league_id = creds['league']['league_id']
access_token = token_data['access_token']

print("=" * 70)
print(" Yahoo Fantasy API 連接測試")
print("=" * 70)
print()
print(f"聯盟 ID: {league_id}")
print(f"Access Token: {access_token[:20]}...")
print()
print("正在測試 API 連接...")
print()

# 測試 API 請求 - 獲取聯盟資訊
api_url = f"https://fantasysports.yahooapis.com/fantasy/v2/league/nba.l.{league_id}"

headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
}

try:
    response = requests.get(api_url, headers=headers)

    print(f"API 回應狀態碼: {response.status_code}")
    print()

    if response.status_code == 200:
        print("✅ API 連接成功！")
        print()
        print("回應內容預覽:")
        print(response.text[:500])
        print()
        print("=" * 70)
        print(" 系統已準備就緒！")
        print("=" * 70)
        print()
        print("你現在可以:")
        print("1. 執行主程式: python3 src/main.py")
        print("2. 分析你的陣容")
        print("3. 評估交易")
        print()

    else:
        print(f"❌ API 請求失敗！")
        print(f"回應: {response.text[:300]}")
        print()

        if response.status_code == 401:
            print("可能的原因:")
            print("1. Access Token 已過期 (有效期: 1小時)")
            print("2. 需要重新授權")
            print()
        elif response.status_code == 403:
            print("可能的原因:")
            print("1. 你的 Yahoo 帳號沒有加入聯盟 ID 71325")
            print("2. 聯盟 ID 錯誤")
            print()

except Exception as e:
    print(f"❌ 錯誤: {e}")
