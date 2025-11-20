"""
獲取整個聯盟的數據 - 給所有成員使用
作為盟主提供給大家的服務
"""

import sys
sys.path.insert(0, 'src')

import json
from pathlib import Path
from yfpy.query import YahooFantasySportsQuery

print("=" * 80)
print(" 大亂鬥聯盟 - 完整數據獲取")
print("=" * 80)
print()

# 載入配置
with open('config/credentials.json', 'r') as f:
    config = json.load(f)

yahoo_config = config['yahoo']
league_config = config['league']

print("步驟 1: 連接 Yahoo API...")

try:
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

    # 獲取聯盟資訊
    print("步驟 2: 獲取聯盟資訊...")
    league = yahoo_query.get_league_info()

    league_name = league.name
    if isinstance(league_name, bytes):
        league_name = league_name.decode('utf-8')

    print(f"聯盟名稱: {league_name}")
    print(f"聯盟 ID: {league.league_id}")
    print(f"隊伍數: {league.num_teams}")
    print(f"當前週次: Week {league.current_week}")
    print()

    # 獲取所有隊伍
    print("步驟 3: 獲取所有隊伍資訊...")
    teams = yahoo_query.get_league_teams()

    teams_data = []
    for i, team in enumerate(teams, 1):
        team_name = team.name
        if isinstance(team_name, bytes):
            team_name = team_name.decode('utf-8')

        # 獲取經理名稱
        manager_name = 'Unknown'
        if hasattr(team, 'managers') and team.managers:
            try:
                first_manager = team.managers[0]
                if hasattr(first_manager, 'nickname'):
                    manager_name = first_manager.nickname
                    if isinstance(manager_name, bytes):
                        manager_name = manager_name.decode('utf-8')
            except:
                pass

        team_info = {
            'rank': i,
            'team_id': team.team_id,
            'team_name': team_name,
            'manager': manager_name
        }

        teams_data.append(team_info)

        print(f"  {i}. {team_name} (Team ID: {team.team_id})")

    print()

    # 獲取聯盟排名（如果有）
    print("步驟 4: 獲取聯盟排名...")
    try:
        standings = yahoo_query.get_league_standings()
        print(f"✅ 獲取到 {len(standings)} 支隊伍的排名")

        for i, team in enumerate(standings, 1):
            team_name = team.name if isinstance(team.name, str) else team.name.decode('utf-8')
            teams_data[i-1]['wins'] = getattr(team, 'team_standings', {}).get('outcome_totals', {}).get('wins', 0) if hasattr(team, 'team_standings') else 0
            teams_data[i-1]['losses'] = getattr(team, 'team_standings', {}).get('outcome_totals', {}).get('losses', 0) if hasattr(team, 'team_standings') else 0
            teams_data[i-1]['ties'] = getattr(team, 'team_standings', {}).get('outcome_totals', {}).get('ties', 0) if hasattr(team, 'team_standings') else 0

    except Exception as e:
        print(f"⚠️  排名數據暫時無法獲取: {e}")
        for team in teams_data:
            team['wins'] = 0
            team['losses'] = 0
            team['ties'] = 0

    print()

    # 獲取本週對戰
    print("步驟 5: 獲取本週對戰...")
    try:
        current_week = league.current_week
        matchups = yahoo_query.get_league_matchups_by_week(current_week)

        matchups_data = []
        for matchup in matchups:
            if hasattr(matchup, 'teams'):
                teams_in_matchup = matchup.teams
                if len(teams_in_matchup) >= 2:
                    team1 = teams_in_matchup[0]
                    team2 = teams_in_matchup[1]

                    team1_name = team1.name if isinstance(team1.name, str) else team1.name.decode('utf-8')
                    team2_name = team2.name if isinstance(team2.name, str) else team2.name.decode('utf-8')

                    matchups_data.append({
                        'team1_id': team1.team_id,
                        'team1_name': team1_name,
                        'team2_id': team2.team_id,
                        'team2_name': team2_name,
                        'week': current_week
                    })

        print(f"✅ Week {current_week} 對戰: {len(matchups_data)} 場")

    except Exception as e:
        print(f"⚠️  對戰數據暫時無法獲取: {e}")
        matchups_data = []

    print()

    # 儲存聯盟數據
    league_data = {
        'league_name': league_name,
        'league_id': league.league_id,
        'num_teams': league.num_teams,
        'current_week': league.current_week,
        'season': league_config.get('season', '2025'),
        'teams': teams_data,
        'matchups': matchups_data,
        'last_updated': '2025-10-22 16:00:00'
    }

    output_file = 'data/league_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(league_data, f, indent=2, ensure_ascii=False)

    print("=" * 80)
    print(" 聯盟數據獲取完成！")
    print("=" * 80)
    print()
    print(f"✅ 數據已儲存至: {output_file}")
    print()
    print(f"聯盟: {league_name}")
    print(f"隊伍: {len(teams_data)} 支")
    print(f"當前週次: Week {league.current_week}")
    print(f"本週對戰: {len(matchups_data)} 場")
    print()
    print("下一步: 執行 python3 sync_league_to_sheets.py 同步到 Google Sheets")
    print()

except Exception as e:
    print(f"❌ 錯誤: {e}")
    import traceback
    traceback.print_exc()
