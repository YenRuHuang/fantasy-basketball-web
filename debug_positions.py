"""
檢查 Yahoo API 返回的位置資料格式
"""

import sys
sys.path.insert(0, 'src')

import json
from pathlib import Path
from yfpy.query import YahooFantasySportsQuery

# 載入配置
with open('config/credentials.json', 'r') as f:
    config = json.load(f)

yahoo_config = config['yahoo']
league_config = config['league']

print("連接 Yahoo API...")

yahoo_query = YahooFantasySportsQuery(
    auth_dir=str(Path.cwd() / "config"),
    league_id=league_config['league_id'],
    game_code=league_config['game_code'],
    consumer_key=yahoo_config['client_id'],
    consumer_secret=yahoo_config['client_secret'],
    browser_callback=True
)

team_id = 1
roster_stats = yahoo_query.get_team_roster_player_stats_by_week(team_id, 1)

print("\n檢查前 3 位球員的所有屬性:")
print("=" * 70)

for i, player in enumerate(roster_stats[:3], 1):
    print(f"\n球員 {i}: {player.name.full if hasattr(player.name, 'full') else player.name}")
    print("-" * 70)

    # 列出所有屬性
    for attr in dir(player):
        if not attr.startswith('_'):
            try:
                val = getattr(player, attr)
                if not callable(val):
                    if 'position' in attr.lower() or 'eligible' in attr.lower():
                        print(f"  {attr}: {val}")
            except:
                pass
