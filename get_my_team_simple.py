"""
簡化版 - 獲取你的陣容資料
"""

import sys
sys.path.insert(0, 'src')

import json
from pathlib import Path
from yfpy.query import YahooFantasySportsQuery

print("=" * 70)
print(" 獲取「默絲佛陀攝影掃地伯」陣容")
print("=" * 70)
print()

# 載入配置
with open('config/credentials.json', 'r') as f:
    config = json.load(f)

yahoo_config = config['yahoo']
league_config = config['league']

print("連接 Yahoo API...")

try:
    # 初始化
    yahoo_query = YahooFantasySportsQuery(
        auth_dir=str(Path.cwd() / "config"),
        league_id=league_config['league_id'],
        game_code=league_config['game_code'],
        consumer_key=yahoo_config['client_id'],
        consumer_secret=yahoo_config['client_secret'],
        browser_callback=True
    )

    print("✅ 連接成功")
    print()

    # 獲取你的隊伍 roster
    team_id = 1  # 默絲佛陀攝影掃地伯

    print(f"獲取 Team #{team_id} 的資料...")
    print()

    # 嘗試不同的 API 方法
    try:
        team_info = yahoo_query.get_team_info(team_id)
        print("隊伍資訊:")
        print(f"  名稱: {team_info.name if isinstance(team_info.name, str) else team_info.name.decode('utf-8')}")
        print(f"  ID: {team_info.team_id}")
        print()
    except Exception as e:
        print(f"獲取隊伍資訊失敗: {e}")
        print()

    # 嘗試獲取陣容
    try:
        print("嘗試獲取陣容 (方法 1: get_team_roster_player_info)...")
        players = yahoo_query.get_team_roster_player_info(team_id)

        print(f"找到 {len(players)} 個球員")
        print()
        print("球員名單:")
        print("-" * 70)

        player_list = []
        for i, player in enumerate(players, 1):
            # 嘗試不同的屬性
            try:
                if hasattr(player, 'name'):
                    name = player.name.full if hasattr(player.name, 'full') else str(player.name)
                elif hasattr(player, 'player_key'):
                    name = f"Player {player.player_key}"
                else:
                    name = f"Player #{i}"

                team = player.editorial_team_abbr if hasattr(player, 'editorial_team_abbr') else "?"

                print(f"  {i}. {name} ({team})")

                player_list.append({
                    'name': name,
                    'team': team,
                    'player_obj': player
                })

            except Exception as e:
                print(f"  {i}. (無法解析球員資料: {e})")

        print()
        print("=" * 70)
        print(f" 成功獲取 {len(player_list)} 位球員!")
        print("=" * 70)

        # 儲存原始數據供調試
        print()
        print("儲存原始數據到 data/raw_roster.json...")

        # 將物件轉換為可序列化的格式
        raw_data = []
        for p in players[:3]:  # 只取前 3 個做範例
            p_dict = {}
            for attr in dir(p):
                if not attr.startswith('_'):
                    try:
                        val = getattr(p, attr)
                        if not callable(val):
                            if isinstance(val, bytes):
                                p_dict[attr] = val.decode('utf-8')
                            elif isinstance(val, (str, int, float, bool, type(None))):
                                p_dict[attr] = val
                            else:
                                p_dict[attr] = str(val)
                    except:
                        pass
            raw_data.append(p_dict)

        with open('data/raw_roster.json', 'w', encoding='utf-8') as f:
            json.dump(raw_data, f, indent=2, ensure_ascii=False)

        print("✅ 已儲存")

    except Exception as e:
        print(f"❌ 方法 1 失敗: {e}")
        print()

        # 嘗試另一個方法
        try:
            print("嘗試獲取陣容 (方法 2: get_team_roster)...")
            roster = yahoo_query.get_team_roster(team_id)
            print(f"Roster 類型: {type(roster)}")
            print(f"Roster: {roster}")
        except Exception as e2:
            print(f"❌ 方法 2 也失敗: {e2}")

except Exception as e:
    print(f"❌ 主要錯誤: {e}")
    import traceback
    traceback.print_exc()
