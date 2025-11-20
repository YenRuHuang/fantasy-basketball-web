"""
獲取完整聯盟數據 - 包含所有週次的對戰
"""

import sys
sys.path.insert(0, 'src')

import json
from pathlib import Path
from datetime import datetime
from yfpy.query import YahooFantasySportsQuery

print("=" * 80)
print(" 大亂鬥聯盟 - 完整數據獲取（含所有週次）")
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

    num_weeks = getattr(league, 'end_week', 22)  # Yahoo Fantasy 通常是22週

    print(f"聯盟名稱: {league_name}")
    print(f"聯盟 ID: {league.league_id}")
    print(f"隊伍數: {league.num_teams}")
    print(f"當前週次: Week {league.current_week}")
    print(f"總週數: Week {num_weeks}")
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

        # 獲取戰績
        wins = 0
        losses = 0
        ties = 0
        if hasattr(team, 'team_standings'):
            standings = team.team_standings
            if hasattr(standings, 'outcome_totals'):
                outcome = standings.outcome_totals
                wins = int(outcome.wins) if hasattr(outcome, 'wins') and outcome.wins else 0
                losses = int(outcome.losses) if hasattr(outcome, 'losses') and outcome.losses else 0
                ties = int(outcome.ties) if hasattr(outcome, 'ties') and outcome.ties else 0

        team_info = {
            'rank': i,
            'team_id': team.team_id,
            'team_name': team_name,
            'manager': manager_name,
            'wins': wins,
            'losses': losses,
            'ties': ties
        }

        teams_data.append(team_info)
        print(f"  {i}. {team_name} (Team ID: {team.team_id}) - {wins}-{losses}-{ties}")

    print()

    # 獲取所有週次的對戰
    print(f"步驟 4: 獲取所有週次對戰（Week 1 - {num_weeks}）...")

    all_matchups = {}

    for week in range(1, num_weeks + 1):
        try:
            print(f"  獲取 Week {week}...", end=" ")
            matchups = yahoo_query.get_league_matchups_by_week(week)

            week_matchups = []
            for matchup in matchups:
                if hasattr(matchup, 'teams'):
                    teams_in_matchup = matchup.teams
                    if len(teams_in_matchup) >= 2:
                        team1 = teams_in_matchup[0]
                        team2 = teams_in_matchup[1]

                        team1_name = team1.name if isinstance(team1.name, str) else team1.name.decode('utf-8')
                        team2_name = team2.name if isinstance(team2.name, str) else team2.name.decode('utf-8')

                        week_matchups.append({
                            'team1_id': team1.team_id,
                            'team1_name': team1_name,
                            'team2_id': team2.team_id,
                            'team2_name': team2_name
                        })

            all_matchups[f'week_{week}'] = week_matchups
            print(f"✅ {len(week_matchups)} 場")

        except Exception as e:
            print(f"⚠️ 無法獲取: {e}")
            all_matchups[f'week_{week}'] = []

    print()

    # 建立對戰矩陣（每支隊伍的對手）
    print("步驟 5: 建立對戰矩陣...")

    team_schedule = {}
    for team in teams_data:
        team_schedule[team['team_id']] = {}

    for week, matchups in all_matchups.items():
        week_num = int(week.split('_')[1])
        for matchup in matchups:
            team1_id = matchup['team1_id']
            team2_id = matchup['team2_id']

            team_schedule[team1_id][week_num] = {
                'opponent_id': team2_id,
                'opponent_name': matchup['team2_name']
            }
            team_schedule[team2_id][week_num] = {
                'opponent_id': team1_id,
                'opponent_name': matchup['team1_name']
            }

    print(f"✅ 已建立 {len(teams_data)} 支隊伍的完整賽程")
    print()

    # 獲取所有隊伍的球員陣容
    print("步驟 6: 獲取所有隊伍的球員陣容...")

    all_rosters = {}
    for team in teams_data:
        team_id = team['team_id']
        try:
            print(f"  獲取 {team['team_name']}...", end=" ")
            roster = yahoo_query.get_team_roster_player_stats_by_week(team_id, league.current_week)

            players_data = []
            for player in roster:
                # 解析球員名稱
                if hasattr(player, 'name'):
                    if hasattr(player.name, 'full'):
                        player_name = player.name.full
                    else:
                        player_name = str(player.name)
                else:
                    player_name = 'Unknown'

                if isinstance(player_name, bytes):
                    player_name = player_name.decode('utf-8')

                # 解析位置（使用 display_position）
                positions = []
                if hasattr(player, 'display_position'):
                    display_pos = player.display_position
                    if display_pos and isinstance(display_pos, str):
                        positions = [p.strip() for p in display_pos.split(',')]

                if not positions and hasattr(player, 'eligible_positions'):
                    raw_positions = player.eligible_positions if player.eligible_positions else []
                    if isinstance(raw_positions, str):
                        raw_positions = [raw_positions]
                    positions = [p for p in raw_positions if p not in ['Util', 'BN', 'IL', 'IR', 'IR+']]

                if not positions:
                    positions = ['N/A']

                # 獲取球員狀態
                status = ''
                if hasattr(player, 'status'):
                    status = player.status if player.status else ''

                # 獲取球隊
                nba_team = ''
                if hasattr(player, 'editorial_team_abbr'):
                    nba_team = player.editorial_team_abbr
                    if isinstance(nba_team, bytes):
                        nba_team = nba_team.decode('utf-8')

                player_info = {
                    'player_id': player.player_id,
                    'name': player_name,
                    'positions': positions,
                    'status': status,
                    'team': nba_team
                }

                players_data.append(player_info)

            all_rosters[str(team_id)] = players_data
            print(f"✅ {len(players_data)} 名球員")

        except Exception as e:
            print(f"⚠️ 無法獲取: {e}")
            all_rosters[str(team_id)] = []

    print()

    # 儲存聯盟數據
    league_data = {
        'league_name': league_name,
        'league_id': league.league_id,
        'num_teams': league.num_teams,
        'current_week': league.current_week,
        'total_weeks': num_weeks,
        'season': league_config.get('season', '2025'),
        'teams': teams_data,
        'matchups_by_week': all_matchups,
        'team_schedules': team_schedule,
        'rosters': all_rosters,
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    output_file = 'data/full_league_data.json'
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
    print(f"總週數: {num_weeks} 週")
    print(f"對戰數據: {sum(len(m) for m in all_matchups.values())} 場")
    total_players = sum(len(roster) for roster in all_rosters.values())
    print(f"球員數據: {total_players} 名")
    print()
    print("下一步: 執行 python3 sync_league_shared.py 同步到新的 Google Sheets")
    print()

except Exception as e:
    print(f"❌ 錯誤: {e}")
    import traceback
    traceback.print_exc()
