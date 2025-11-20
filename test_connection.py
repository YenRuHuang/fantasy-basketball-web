"""
測試 Yahoo Fantasy API 連接

第一次執行時會要求 OAuth 認證
"""

import sys
sys.path.append('src')

from api.yahoo_client import YahooFantasyClient

print("=" * 60)
print(" Yahoo Fantasy Basketball API 連接測試")
print("=" * 60)
print()
print("第一次執行需要進行 OAuth 認證：")
print("1. 程式會顯示一個 Yahoo 授權網址")
print("2. 請在瀏覽器中開啟該網址")
print("3. 登入你的 Yahoo 帳號並授權")
print("4. 授權後 Yahoo 會重定向到 localhost:8787")
print("5. 複製網址列中的 'code=XXXXX' 部分的 XXXXX")
print("6. 貼回這裡")
print()
print("=" * 60)
print()

try:
    # 初始化客戶端（會自動觸發 OAuth 流程）
    client = YahooFantasyClient()

    print("\n✅ Yahoo Fantasy API 連接成功！")
    print()

    # 測試獲取聯盟資訊
    print("正在獲取聯盟資訊...")
    league_info = client.get_league_info()

    print(f"\n聯盟名稱: {league_info.name}")
    print(f"聯盟 ID: {league_info.league_id}")
    print(f"隊伍數量: {league_info.num_teams}")
    print(f"當前週次: {league_info.current_week}")
    print(f"賽季: {league_info.season}")

    print("\n" + "=" * 60)
    print(" 連接測試完成！系統已準備就緒！")
    print("=" * 60)

except KeyboardInterrupt:
    print("\n\n使用者取消操作")
    sys.exit(1)

except Exception as e:
    print(f"\n❌ 連接失敗: {e}")
    print("\n請檢查:")
    print("1. config/credentials.json 中的 Client ID 和 Client Secret 是否正確")
    print("2. 你的 Yahoo 帳號是否有加入聯盟 ID 71325")
    print("3. 網路連接是否正常")
    sys.exit(1)
