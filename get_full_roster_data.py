"""
獲取完整的陣容數據和統計
"""

import sys
sys.path.insert(0, 'src')

import json
from pathlib import Path
from yfpy.query import YahooFantasySportsQuery

print("=" * 70)
print(" 默絲佛陀攝影掃地伯 - 完整陣容數據")
print("=" * 70)
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

    team_id = 1  # 默絲佛陀攝影掃地伯
    current_week = 1

    print(f"步驟 2: 獲取第 {current_week} 週陣容統計...")
    print()

    # 獲取陣容球員統計
    roster_stats = yahoo_query.get_team_roster_player_stats_by_week(team_id, current_week)

    print(f"✅ 找到 {len(roster_stats)} 位球員")
    print()
    print("=" * 70)
    print(" 球員名單 & 統計數據")
    print("=" * 70)
    print()

    player_data = []

    for i, player in enumerate(roster_stats, 1):
        # 解析球員名稱
        if hasattr(player, 'name'):
            if hasattr(player.name, 'full'):
                name = player.name.full
            else:
                name = str(player.name)
                if isinstance(name, bytes):
                    name = name.decode('utf-8')
        else:
            name = f"Player #{i}"

        # 解析隊伍
        team = "?"
        if hasattr(player, 'editorial_team_abbr'):
            team = player.editorial_team_abbr
            if isinstance(team, bytes):
                team = team.decode('utf-8')

        # 解析位置（獲取所有可用位置）
        positions = []

        # display_position 包含所有位置（格式：PG,SG）
        if hasattr(player, 'display_position'):
            display_pos = player.display_position
            if display_pos and isinstance(display_pos, str):
                # 分割逗號分隔的位置
                positions = [p.strip() for p in display_pos.split(',')]
            else:
                positions = [display_pos] if display_pos else []

        # 如果沒有 display_position，使用 eligible_positions
        if not positions and hasattr(player, 'eligible_positions'):
            raw_positions = player.eligible_positions if player.eligible_positions else []
            if isinstance(raw_positions, str):
                raw_positions = [raw_positions]
            positions = [p for p in raw_positions if p not in ['Util', 'BN', 'IL', 'IR', 'IR+']]

        # 確保至少有一個位置
        if not positions:
            positions = ['N/A']

        # 解析傷病狀態
        status = None
        if hasattr(player, 'status'):
            status = player.status

        # 解析統計數據
        stats = {}
        if hasattr(player, 'player_stats'):
            if hasattr(player.player_stats, 'stats'):
                for stat in player.player_stats.stats:
                    if hasattr(stat, 'stat'):
                        stat_id = stat.stat.stat_id if hasattr(stat.stat, 'stat_id') else None
                        value = stat.stat.value if hasattr(stat.stat, 'value') else None
                        if stat_id and value:
                            stats[stat_id] = value

        print(f"{i}. {name}")
        print(f"   隊伍: {team}")
        print(f"   位置: {','.join(positions) if positions else 'N/A'}")
        if status:
            print(f"   狀態: {status}")
        if stats:
            print(f"   統計: {len(stats)} 項數據")
        print()

        player_data.append({
            'name': name,
            'team': team,
            'positions': positions,
            'status': status,
            'stats': stats
        })

    print("=" * 70)
    print(f" 數據獲取完成！共 {len(player_data)} 位球員")
    print("=" * 70)
    print()

    # 儲存數據
    output_file = 'data/my_roster_full.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'team_name': '默絲佛陀攝影掃地伯',
            'team_id': team_id,
            'week': current_week,
            'players': player_data,
            'total_players': len(player_data)
        }, f, indent=2, ensure_ascii=False)

    print(f"✅ 數據已儲存至: {output_file}")
    print()
    print("下一步:")
    print("  1. 查看陣容數據: cat data/my_roster_full.json")
    print("  2. 生成週報告: python3 generate_weekly_report_real.py")
    print()

except Exception as e:
    print(f"❌ 錯誤: {e}")
    import traceback
    traceback.print_exc()
