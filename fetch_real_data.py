"""
直接用 yfpy 獲取真實的 Yahoo Fantasy 數據
"""

import sys
sys.path.insert(0, 'src')

import json
from pathlib import Path
from yfpy.query import YahooFantasySportsQuery

print("=" * 70)
print(" 獲取 Yahoo Fantasy 真實數據")
print("=" * 70)
print()

# 載入配置
with open('config/credentials.json', 'r') as f:
    config = json.load(f)

yahoo_config = config['yahoo']
league_config = config['league']

print("步驟 1: 連接 Yahoo API...")
print()

try:
    # 初始化 Yahoo Query
    yahoo_query = YahooFantasySportsQuery(
        auth_dir=str(Path.cwd() / "config"),
        league_id=league_config['league_id'],
        game_code=league_config['game_code'],
        consumer_key=yahoo_config['client_id'],
        consumer_secret=yahoo_config['client_secret'],
        browser_callback=True
    )

    print("✅ API 連接成功")
    print()

    # 獲取聯盟資訊
    print("步驟 2: 獲取聯盟資訊...")
    league = yahoo_query.get_league_info()

    print(f"聯盟名稱: {league.name}")
    print(f"聯盟 ID: {league.league_id}")
    print(f"隊伍數量: {league.num_teams}")
    print(f"當前週次: {league.current_week}")
    print()

    # 獲取所有隊伍
    print("步驟 3: 獲取所有隊伍...")
    teams = yahoo_query.get_league_teams()

    print(f"找到 {len(teams)} 支隊伍:")
    decoded_teams = []
    for i, team in enumerate(teams, 1):
        # 解碼 bytes 名稱
        team_name = team.name
        if isinstance(team_name, bytes):
            team_name = team_name.decode('utf-8')
        decoded_teams.append((team, team_name))
        print(f"  {i}. {team_name} (ID: {team.team_id})")
    print()

    # 找到你的隊伍：默絲佛陀攝影掃地伯
    my_team = None
    for team, team_name in decoded_teams:
        if "默絲佛陀攝影掃地伯" in team_name or team.team_id == 1:
            my_team = team
            break

    if my_team:
        print(f"步驟 4: 找到你的隊伍: {my_team.name}")
        print(f"隊伍 ID: {my_team.team_id}")
        print()

        # 獲取陣容
        print("步驟 5: 獲取陣容數據...")
        roster = yahoo_query.get_team_roster_by_week(my_team.team_id)

        print(f"陣容球員數: {len(roster)}")
        print()

        print("球員列表:")
        print("-" * 70)
        for player in roster:
            # 處理不同的數據格式
            if isinstance(player, str):
                print(f"  {player}")
            else:
                player_name = player.name.full if hasattr(player.name, 'full') else str(player.name)
                team_abbr = player.editorial_team_abbr if hasattr(player, 'editorial_team_abbr') else "N/A"
                injury_status = f" ({player.status})" if hasattr(player, 'status') and player.status else ""
                positions = ','.join(player.eligible_positions) if hasattr(player, 'eligible_positions') else "N/A"
                print(f"  {player_name} - {team_abbr} [{positions}]{injury_status}")
        print()

        # 獲取球員數據
        print("步驟 6: 獲取球員統計數據...")
        print()

        stats_data = []
        for player in roster[:5]:  # 先測試前 5 個球員
            try:
                print(f"正在獲取 {player.name.full} 的數據...")
                player_stats = yahoo_query.get_player_stats_by_week(player.player_id, week=1)

                if player_stats:
                    stats_data.append({
                        'name': player.name.full,
                        'team': player.editorial_team_abbr,
                        'stats': player_stats
                    })
                    print(f"  ✅ 獲取成功")
                else:
                    print(f"  ⚠️  無數據")

            except Exception as e:
                print(f"  ❌ 錯誤: {e}")

        print()
        print("=" * 70)
        print(" 數據獲取完成！")
        print("=" * 70)

        # 儲存數據
        output_file = 'data/my_roster_real.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'team_name': my_team.name,
                'team_id': my_team.team_id,
                'roster': [
                    {
                        'name': p.name.full,
                        'team': p.editorial_team_abbr,
                        'positions': p.eligible_positions if hasattr(p, 'eligible_positions') else [],
                        'status': p.status if hasattr(p, 'status') else None
                    }
                    for p in roster
                ],
                'stats_sample': stats_data
            }, f, indent=2, ensure_ascii=False)

        print()
        print(f"數據已儲存至: {output_file}")

    else:
        print("❌ 找不到隊伍 '霍格格'")
        print("請確認隊伍名稱")

except Exception as e:
    print(f"❌ 錯誤: {e}")
    import traceback
    traceback.print_exc()
