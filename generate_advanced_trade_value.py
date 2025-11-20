"""
進階交易價值評估 - 完整版
計算每位球員的綜合交易價值，考慮位置稀缺性、健康狀態、球隊實力
"""

import json
from datetime import datetime
from pathlib import Path

print("=" * 80)
print("  進階交易價值評估系統")
print("=" * 80)
print()

# 載入聯盟數據
print("步驟 1: 載入聯盟數據...")
with open('data/full_league_data.json', 'r', encoding='utf-8') as f:
    league_data = json.load(f)

teams = league_data['teams']
rosters = league_data['rosters']

print(f"聯盟: {league_data['league_name']}")
print(f"隊伍數: {len(teams)}")
print()

# 位置稀缺性配置
POSITION_SCARCITY = {
    'C': 19.6,      # 中鋒最稀缺
    'PF': 16.8,     # 大前鋒次之
    'SF': 15.2,     # 小前鋒
    'SG': 14.1,     # 得分後衛
    'PG': 13.7      # 控球後衛最常見
}

# 健康狀態分數
HEALTH_SCORES = {
    '': 25,         # 健康
    'GTD': 10,      # 每日觀察
    'DTD': 5,       # 每日觀察
    'O': -15,       # 受傷
    'INJ': -15,     # 受傷
    'OUT': -15      # 缺席
}

print("步驟 2: 計算球隊實力（基於勝率）...")

# 計算每支球隊的勝率
team_win_rates = {}
for team in teams:
    team_id = str(team['team_id'])
    wins = team.get('wins', 0)
    losses = team.get('losses', 0)
    ties = team.get('ties', 0)
    total = wins + losses + ties

    # 如果賽季剛開始，給予平均值
    if total == 0:
        win_rate = 0.500
    else:
        win_rate = (wins + ties * 0.5) / total

    team_win_rates[team_id] = win_rate
    print(f"  {team['team_name']}: {win_rate:.3f}")

print()

print("步驟 3: 計算位置稀缺性...")

# 統計所有位置的球員數量
position_counts = {pos: 0 for pos in POSITION_SCARCITY.keys()}
total_players = 0

for team_id, roster in rosters.items():
    for player in roster:
        total_players += 1
        for pos in player.get('positions', []):
            if pos in position_counts:
                position_counts[pos] += 1

# 計算實際百分比
position_percentages = {}
for pos, count in position_counts.items():
    percentage = (count / total_players * 100) if total_players > 0 else 0
    position_percentages[pos] = percentage
    print(f"  {pos}: {count} 人 ({percentage:.1f}%)")

print()

print("步驟 4: 評估所有球員交易價值...")

all_players_value = []

for team in teams:
    team_id = str(team['team_id'])
    team_name = team['team_name']
    team_roster = rosters.get(team_id, [])
    team_win_rate = team_win_rates.get(team_id, 0.500)

    for player in team_roster:
        # 基礎分數
        base_score = 50

        # 1. 位置價值計算 (0-30分)
        positions = player.get('positions', [])
        num_positions = len(positions)

        # 多位置加成 (0-15分)
        multi_pos_bonus = 0
        if num_positions >= 4:
            multi_pos_bonus = 15
        elif num_positions == 3:
            multi_pos_bonus = 10
        elif num_positions == 2:
            multi_pos_bonus = 5

        # 稀缺性加成 (0-15分)
        scarcity_bonus = 0
        for pos in positions:
            if pos in POSITION_SCARCITY:
                pos_scarcity = POSITION_SCARCITY[pos]
                # 越稀缺分數越高
                scarcity_bonus = max(scarcity_bonus, (pos_scarcity - 13.7) * 2.5)

        position_value = multi_pos_bonus + scarcity_bonus

        # 2. 健康狀態 (-15 到 +25分)
        status = player.get('status', '')
        health_value = HEALTH_SCORES.get(status, HEALTH_SCORES[''])

        # 3. 球隊實力 (0-20分)
        # 勝率越高，球員價值越高（因為來自強隊）
        team_strength = team_win_rate * 20

        # 4. 特殊加成 (0-10分)
        special_bonus = 0
        # 純中鋒最稀缺
        if positions == ['C']:
            special_bonus = 10
        # 包含C的多位置球員
        elif 'C' in positions and num_positions >= 2:
            special_bonus = 5

        # 總分計算
        total_score = base_score + position_value + health_value + team_strength + special_bonus

        # 分級
        if total_score >= 95:
            tier = 'S'
        elif total_score >= 85:
            tier = 'A'
        elif total_score >= 75:
            tier = 'B'
        elif total_score >= 65:
            tier = 'C'
        else:
            tier = 'D'

        player_value = {
            'player_name': player['name'],
            'nba_team': player.get('team', ''),
            'positions': positions,
            'fantasy_team': team_name,
            'fantasy_team_id': team_id,
            'status': status if status else 'Healthy',
            'scores': {
                'base': base_score,
                'position_value': round(position_value, 1),
                'multi_position_bonus': multi_pos_bonus,
                'scarcity_bonus': round(scarcity_bonus, 1),
                'health_value': health_value,
                'team_strength': round(team_strength, 1),
                'special_bonus': special_bonus,
                'total': round(total_score, 1)
            },
            'tier': tier,
            'win_rate': round(team_win_rate, 3)
        }

        all_players_value.append(player_value)

# 依總分排序
all_players_value.sort(key=lambda x: x['scores']['total'], reverse=True)

print(f"已評估 {len(all_players_value)} 名球員")
print()

# 顯示前10名
print("Top 10 交易價值球員:")
for i, player in enumerate(all_players_value[:10], 1):
    positions_str = ','.join(player['positions'])
    print(f"  {i}. [{player['tier']}] {player['player_name']} ({positions_str}) - {player['scores']['total']:.1f} 分")

print()

# 統計各分級數量
tier_counts = {}
for player in all_players_value:
    tier = player['tier']
    tier_counts[tier] = tier_counts.get(tier, 0) + 1

print("分級統計:")
for tier in ['S', 'A', 'B', 'C', 'D']:
    count = tier_counts.get(tier, 0)
    print(f"  {tier} 級: {count} 人")

print()

# 儲存結果
output_data = {
    'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'league_name': league_data['league_name'],
    'current_week': league_data['current_week'],
    'total_players': len(all_players_value),
    'tier_distribution': tier_counts,
    'position_scarcity': position_percentages,
    'methodology': {
        'base_score': 50,
        'position_value_range': '0-30 (multi-position: 0-15, scarcity: 0-15)',
        'health_value_range': '-15 to +25',
        'team_strength_range': '0-20 (based on win rate)',
        'special_bonus_range': '0-10 (pure C: +10, multi-pos C: +5)'
    },
    'players': all_players_value
}

output_file = 'data/advanced_trade_value.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print("=" * 80)
print("  交易價值評估完成！")
print("=" * 80)
print()
print(f"輸出檔案: {output_file}")
print(f"評估時間: {output_data['generated_at']}")
print(f"球員總數: {len(all_players_value)}")
print()
print("下一步: 執行 python3 sync_advanced_trade_value.py 同步到 Google Sheets")
print()
