"""
生成聯盟洞察數據
包含：賽程分析、位置深度、交易價值參考、每週戰報
"""

import json
from datetime import datetime
from collections import defaultdict

print("=" * 80)
print("  聯盟洞察數據生成系統")
print("=" * 80)
print()

# 載入聯盟數據
print("步驟 1: 載入聯盟數據...")
with open('data/full_league_data.json', 'r', encoding='utf-8') as f:
    league_data = json.load(f)

teams = league_data['teams']
rosters = league_data['rosters']
team_schedules = league_data['team_schedules']
matchups_by_week = league_data['matchups_by_week']
current_week = league_data['current_week']
total_weeks = league_data['total_weeks']

print(f"聯盟: {league_data['league_name']}")
print(f"當前週次: Week {current_week}")
print()

# ============================================================================
# 洞察 1: 賽程難度分析
# ============================================================================
print("步驟 2: 分析賽程難度...")

# 計算每隊勝率
team_win_rates = {}
for team in teams:
    team_id = str(team['team_id'])
    wins = team.get('wins', 0)
    losses = team.get('losses', 0)
    ties = team.get('ties', 0)
    total = wins + losses + ties

    if total == 0:
        win_rate = 0.500
    else:
        win_rate = (wins + ties * 0.5) / total

    team_win_rates[team_id] = win_rate

schedule_analysis = []

for team in teams:
    team_id = str(team['team_id'])
    team_name = team['team_name']
    team_schedule = team_schedules.get(team_id, {})

    # 分析未來4週對手
    future_opponents = []
    total_difficulty = 0

    for week in range(current_week, min(current_week + 4, total_weeks + 1)):
        week_str = str(week)
        if week_str in team_schedule:
            opponent_id = str(team_schedule[week_str]['opponent_id'])
            opponent_name = team_schedule[week_str]['opponent_name']
            opponent_win_rate = team_win_rates.get(opponent_id, 0.500)

            future_opponents.append({
                'week': week,
                'opponent': opponent_name,
                'win_rate': round(opponent_win_rate, 3)
            })

            total_difficulty += opponent_win_rate

    avg_difficulty = total_difficulty / len(future_opponents) if future_opponents else 0.500

    # 難度評級
    if avg_difficulty >= 0.600:
        difficulty_level = "困難"
        emoji = "🔴"
    elif avg_difficulty >= 0.500:
        difficulty_level = "中等"
        emoji = "🟡"
    else:
        difficulty_level = "容易"
        emoji = "🟢"

    schedule_analysis.append({
        'team_name': team_name,
        'team_id': team_id,
        'current_win_rate': round(team_win_rates[team_id], 3),
        'avg_opponent_strength': round(avg_difficulty, 3),
        'difficulty_level': difficulty_level,
        'emoji': emoji,
        'future_opponents': future_opponents
    })

# 依難度排序
schedule_analysis.sort(key=lambda x: x['avg_opponent_strength'], reverse=True)

print(f"賽程分析完成 ({len(schedule_analysis)} 支隊伍)")
print()

# ============================================================================
# 洞察 2: 位置深度分析
# ============================================================================
print("步驟 3: 分析位置深度...")

position_depth = []

for team in teams:
    team_id = str(team['team_id'])
    team_name = team['team_name']
    team_roster = rosters.get(team_id, [])

    # 統計各位置球員數
    pos_counts = defaultdict(int)
    total_players = len(team_roster)

    for player in team_roster:
        positions = player.get('positions', [])
        for pos in positions:
            if pos in ['PG', 'SG', 'SF', 'PF', 'C']:
                pos_counts[pos] += 1

    # 找出最強和最弱位置
    max_pos = max(pos_counts, key=pos_counts.get) if pos_counts else 'N/A'
    min_pos = min(pos_counts, key=pos_counts.get) if pos_counts else 'N/A'

    position_depth.append({
        'team_name': team_name,
        'team_id': team_id,
        'total_players': total_players,
        'positions': {
            'PG': pos_counts['PG'],
            'SG': pos_counts['SG'],
            'SF': pos_counts['SF'],
            'PF': pos_counts['PF'],
            'C': pos_counts['C']
        },
        'strongest_position': max_pos,
        'weakest_position': min_pos
    })

print(f"位置深度分析完成 ({len(position_depth)} 支隊伍)")
print()

# ============================================================================
# 洞察 3: 交易價值參考（簡化版）
# ============================================================================
print("步驟 4: 生成交易價值參考...")

trade_reference = []

for team in teams:
    team_id = str(team['team_id'])
    team_name = team['team_name']
    team_roster = rosters.get(team_id, [])

    for player in team_roster:
        # 簡化評分：多位置 + 健康狀態
        positions = player.get('positions', [])
        num_positions = len(positions)
        status = player.get('status', '')

        # 多位置分數
        if num_positions >= 4:
            versatility_score = 90
        elif num_positions == 3:
            versatility_score = 80
        elif num_positions == 2:
            versatility_score = 70
        else:
            versatility_score = 60

        # 健康調整
        if status in ['O', 'INJ', 'OUT']:
            health_adjustment = -20
            health_status = "受傷"
        elif status in ['GTD', 'DTD']:
            health_adjustment = -10
            health_status = "每日觀察"
        else:
            health_adjustment = 0
            health_status = "健康"

        final_score = versatility_score + health_adjustment

        trade_reference.append({
            'player_name': player['name'],
            'team_name': team_name,
            'positions': positions,
            'num_positions': num_positions,
            'health_status': health_status,
            'versatility_score': versatility_score,
            'health_adjustment': health_adjustment,
            'trade_value': final_score
        })

# 依交易價值排序
trade_reference.sort(key=lambda x: x['trade_value'], reverse=True)

print(f"交易價值參考完成 ({len(trade_reference)} 名球員)")
print()

# ============================================================================
# 洞察 4: 每週戰報
# ============================================================================
print("步驟 5: 生成每週戰報...")

# 本週對戰
current_matchups = matchups_by_week.get(f'week_{current_week}', [])

# 找出最強 vs 最強、最弱 vs 最弱
matchup_analysis = []

for matchup in current_matchups:
    team1_id = str(matchup['team1_id'])
    team2_id = str(matchup['team2_id'])
    team1_name = matchup['team1_name']
    team2_name = matchup['team2_name']

    team1_wr = team_win_rates.get(team1_id, 0.500)
    team2_wr = team_win_rates.get(team2_id, 0.500)

    avg_strength = (team1_wr + team2_wr) / 2
    win_rate_diff = abs(team1_wr - team2_wr)

    # 對戰類型
    if avg_strength >= 0.600:
        matchup_type = "強強對決"
    elif avg_strength <= 0.400:
        matchup_type = "弱弱對決"
    elif win_rate_diff <= 0.100:
        matchup_type = "勢均力敵"
    else:
        matchup_type = "實力懸殊"

    matchup_analysis.append({
        'team1': team1_name,
        'team1_wr': round(team1_wr, 3),
        'team2': team2_name,
        'team2_wr': round(team2_wr, 3),
        'avg_strength': round(avg_strength, 3),
        'matchup_type': matchup_type
    })

# 找出本週最值得關注的對戰
matchup_analysis.sort(key=lambda x: x['avg_strength'], reverse=True)
top_matchup = matchup_analysis[0] if matchup_analysis else None
bottom_matchup = matchup_analysis[-1] if matchup_analysis else None

weekly_report = {
    'current_week': current_week,
    'total_matchups': len(current_matchups),
    'top_matchup': top_matchup,
    'bottom_matchup': bottom_matchup,
    'all_matchups': matchup_analysis
}

print(f"每週戰報完成 (Week {current_week}, {len(current_matchups)} 場對戰)")
print()

# ============================================================================
# 儲存所有洞察
# ============================================================================

insights_data = {
    'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'league_name': league_data['league_name'],
    'current_week': current_week,
    'total_weeks': total_weeks,
    'insights': {
        'schedule_difficulty': schedule_analysis,
        'position_depth': position_depth,
        'trade_reference': trade_reference,
        'weekly_report': weekly_report
    }
}

output_file = 'data/league_insights.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(insights_data, f, indent=2, ensure_ascii=False)

print("=" * 80)
print("  聯盟洞察生成完成！")
print("=" * 80)
print()
print(f"輸出檔案: {output_file}")
print(f"生成時間: {insights_data['generated_at']}")
print()
print("洞察內容:")
print(f"  1. 賽程難度分析 - {len(schedule_analysis)} 支隊伍")
print(f"  2. 位置深度分析 - {len(position_depth)} 支隊伍")
print(f"  3. 交易價值參考 - {len(trade_reference)} 名球員")
print(f"  4. 每週戰報 - Week {current_week} ({len(current_matchups)} 場)")
print()
print("下一步: 執行 python3 sync_league_insights.py 同步到 Google Sheets")
print()
