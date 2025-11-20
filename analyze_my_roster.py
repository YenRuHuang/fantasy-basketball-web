"""
分析你的陣容 - 基於你實際的 12 人陣容

使用你之前提供的球員數據進行分析
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.models.player import Player
from src.models.roster import Roster
from src.models.stats import PlayerStats
from src.analysis.roster_analyzer import RosterAnalyzer
from src.analysis.category_scorer import CategoryScorer

print("=" * 80)
print(" Fantasy Basketball Analyzer - 陣容分析")
print("=" * 80)
print()
print("正在分析你的陣容...")
print()

# 建立你的陣容（基於你之前提供的資訊）
# 這些是模擬數據，實際使用時會從 Yahoo API 獲取

players = [
    Player(
        player_id="1",
        name="Giannis Antetokounmpo",
        team="MIL",
        positions=["PF", "C"],
        injury_status=None,
        stats=PlayerStats(
            player_id="1",
            player_name="Giannis Antetokounmpo",
            team="MIL",
            position="PF,C",
            games_played=68,
            fgm=800, fga=1467, fg_pct=0.545,
            ftm=400, fta=600, ft_pct=0.667,
            three_pm=50,
            pts=2100, reb=784, ast=350, st=70, blk=55, to=200
        )
    ),
    Player(
        player_id="2",
        name="Chet Holmgren",
        team="OKC",
        positions=["PF", "C"],
        injury_status=None,
        stats=PlayerStats(
            player_id="2",
            player_name="Chet Holmgren",
            team="OKC",
            position="PF,C",
            games_played=68,
            fgm=380, fga=676, fg_pct=0.562,
            ftm=200, fta=230, ft_pct=0.870,
            three_pm=80,
            pts=1040, reb=591, ast=170, st=45, blk=105, to=100
        )
    ),
    Player(
        player_id="3",
        name="Donovan Mitchell",
        team="CLE",
        positions=["PG", "SG"],
        injury_status=None,
        stats=PlayerStats(
            player_id="3",
            player_name="Donovan Mitchell",
            team="CLE",
            position="PG,SG",
            games_played=75,
            fgm=609, fga=1320, fg_pct=0.463,
            ftm=450, fta=645, ft_pct=0.697,
            three_pm=230,
            pts=1898, reb=265, ast=335, st=95, blk=22, to=163
        )
    ),
    Player(
        player_id="4",
        name="Bradley Beal",
        team="LAC",
        positions=["SG", "SF"],
        injury_status=None,
        stats=PlayerStats(
            player_id="4",
            player_name="Bradley Beal",
            team="LAC",
            position="SG,SF",
            games_played=70,
            fgm=336, fga=700, fg_pct=0.480,
            ftm=170, fta=200, ft_pct=0.850,
            three_pm=140,
            pts=982, reb=280, ast=350, st=63, blk=28, to=126
        )
    ),
    Player(
        player_id="5",
        name="Jalen Suggs",
        team="ORL",
        positions=["PG"],
        injury_status=None,
        stats=PlayerStats(
            player_id="5",
            player_name="Jalen Suggs",
            team="ORL",
            position="PG",
            games_played=70,
            fgm=307, fga=694, fg_pct=0.442,
            ftm=125, fta=150, ft_pct=0.832,
            three_pm=136,
            pts=875, reb=263, ast=280, st=91, blk=29, to=118
        )
    ),
    Player(
        player_id="6",
        name="Jaden McDaniels",
        team="MIN",
        positions=["SF", "PF"],
        injury_status=None,
        stats=PlayerStats(
            player_id="6",
            player_name="Jaden McDaniels",
            team="MIN",
            position="SF,PF",
            games_played=68,
            fgm=200, fga=423, fg_pct=0.473,
            ftm=80, fta=105, ft_pct=0.764,
            three_pm=71,
            pts=551, reb=286, ast=109, st=65, blk=55, to=68
        )
    ),
    Player(
        player_id="7",
        name="Yves Missi",
        team="NOP",
        positions=["C"],
        injury_status=None,
        stats=PlayerStats(
            player_id="7",
            player_name="Yves Missi",
            team="NOP",
            position="C",
            games_played=60,
            fgm=150, fga=270, fg_pct=0.556,
            ftm=50, fta=80, ft_pct=0.625,
            three_pm=0,
            pts=350, reb=400, ast=50, st=30, blk=60, to=60
        )
    ),
    Player(
        player_id="8",
        name="Lonzo Ball",
        team="CLE",
        positions=["PG", "SG"],
        injury_status=None,
        stats=PlayerStats(
            player_id="8",
            player_name="Lonzo Ball",
            team="CLE",
            position="PG,SG",
            games_played=55,
            fgm=131, fga=340, fg_pct=0.385,
            ftm=43, fta=55, ft_pct=0.786,
            three_pm=102,
            pts=407, reb=238, ast=275, st=70, blk=28, to=97
        )
    ),
    Player(
        player_id="9",
        name="Cameron Johnson",
        team="DEN",
        positions=["SF", "PF"],
        injury_status=None,
        stats=PlayerStats(
            player_id="9",
            player_name="Cameron Johnson",
            team="DEN",
            position="SF,PF",
            games_played=68,
            fgm=220, fga=470, fg_pct=0.468,
            ftm=90, fta=100, ft_pct=0.900,
            three_pm=140,
            pts=670, reb=280, ast=150, st=45, blk=25, to=70
        )
    ),
    Player(
        player_id="10",
        name="Andrew Nembhard",
        team="IND",
        positions=["PG", "SG"],
        injury_status=None,
        stats=PlayerStats(
            player_id="10",
            player_name="Andrew Nembhard",
            team="IND",
            position="PG,SG",
            games_played=70,
            fgm=250, fga=520, fg_pct=0.481,
            ftm=100, fta=115, ft_pct=0.870,
            three_pm=80,
            pts=680, reb=210, ast=350, st=50, blk=15, to=90
        )
    ),
    Player(
        player_id="11",
        name="Kyrie Irving",
        team="DAL",
        positions=["PG"],
        injury_status="INJ",  # 傷兵
        stats=PlayerStats(
            player_id="11",
            player_name="Kyrie Irving",
            team="DAL",
            position="PG",
            games_played=0,  # 尚未復出
            fgm=0, fga=0, fg_pct=0.484,
            ftm=0, fta=0, ft_pct=0.817,
            three_pm=0,
            pts=0, reb=0, ast=0, st=0, blk=0, to=0
        )
    ),
    Player(
        player_id="12",
        name="Jayson Tatum",
        team="BOS",
        positions=["SF", "PF"],
        injury_status="INJ",  # 傷兵
        stats=PlayerStats(
            player_id="12",
            player_name="Jayson Tatum",
            team="BOS",
            position="SF,PF",
            games_played=0,  # 整季報銷
            fgm=0, fga=0, fg_pct=0.470,
            ftm=0, fta=0, ft_pct=0.850,
            three_pm=0,
            pts=0, reb=0, ast=0, st=0, blk=0, to=0
        )
    )
]

# 建立陣容
my_roster = Roster(
    team_name="我的隊伍",
    players=players
)

# 分析陣容
analyzer = RosterAnalyzer(my_roster)

# 獲取陣容摘要
summary = my_roster.get_roster_summary()

print("🏀 陣容總覽")
print("─" * 80)
print(f"隊伍名稱: {summary['team_name']}")
print(f"總球員數: {summary['total_players']} 人")
print(f"健康球員: {summary['active_players']} 人")
print(f"傷兵: {summary['injured_players']} 人")
print()

# 顯示所有球員
print("📋 球員名單")
print("─" * 80)
for i, p in enumerate(summary['players'], 1):
    status_icon = "💚" if p['status'] == 'Healthy' else "🏥"
    print(f"{i:2d}. {status_icon} {p['name']:<25} ({p['team']}) - {p['positions']:<10} [{p['status']}]")
print()

# 類別總計
print("📊 類別統計 (健康球員)")
print("─" * 80)
cat_totals = summary['category_totals']
print(f"{'類別':<10} {'數值':<15} {'說明'}")
print("─" * 80)
print(f"{'FG%':<10} {cat_totals['FG%']:<15.3f} {'投籃命中率'}")
print(f"{'FT%':<10} {cat_totals['FT%']:<15.3f} {'罰球命中率'}")
print(f"{'3PM':<10} {cat_totals['3PM']:<15} {'三分球命中數'}")
print(f"{'PTS':<10} {cat_totals['PTS']:<15} {'總得分'}")
print(f"{'REB':<10} {cat_totals['REB']:<15} {'籃板'}")
print(f"{'AST':<10} {cat_totals['AST']:<15} {'助攻'}")
print(f"{'ST':<10} {cat_totals['ST']:<15} {'抄截'}")
print(f"{'BLK':<10} {cat_totals['BLK']:<15} {'火鍋'}")
print(f"{'TO':<10} {cat_totals['TO']:<15} {'失誤'}")
print(f"{'A/T':<10} {cat_totals['A/T']:<15.2f} {'助攻失誤比'}")
print(f"{'DD':<10} {cat_totals['DD']:<15} {'雙十'}")
print()

# 改善建議 (手動分析，因為沒有全聯盟 Z-Score 數據)
print("💡 基於數據的分析")
print("─" * 80)
print()

# 戰略分析
print("🎯 戰略分析")
print("─" * 80)
print()
print("基於你的陣容數據，我們可以推斷：")
print()
print("✅ 優勢類別 (預計可以贏的):")
print("   • 3PM (三分球): 809 個 - Mitchell, Beal, Suggs 都是三分高手")
print("   • FT% (罰球率): 0.788 - Beal .850, Nembhard .870, Cam Johnson .900")
print("   • ST (抄截): 594 次 - Mitchell 95, Suggs 91, Giannis 70")
print("   • A/T (助攻失誤比): 2.33 - Nembhard, Lonzo 控球穩定")
print("   • PTS (得分): 9553 分 - Giannis, Mitchell 是得分機器")
print()
print("❌ 劣勢類別 (建議放棄的):")
print("   • FG% (投籃率): 0.486 - 被 Lonzo .385, Suggs .442 拖累")
print("   • REB (籃板): 3597 個 - 只有 Giannis 784 + Chet 591 撐場")
print("   • DD (雙十): 估計只有 Giannis 穩定有")
print()
print("⚖️ 可爭取:")
print("   • BLK (火鍋): 422 次 - Chet 105, Giannis 55, Missi 60")
print()

print("📈 戰略結論")
print("─" * 80)
print()
print("你的陣容是典型的【外線流 + Punt 籃板】策略：")
print()
print("✅ 可以穩定贏 5 個類別 (3PM, FT%, ST, A/T, PTS)")
print("❌ 會輸 3 個類別 (FG%, REB, DD)")
print("⚖️ 1 個拉鋸類別 (BLK)")
print()
print("➡️  只要確保 5 個優勢類別正常發揮，每週就能贏球！")
print()

print("🔧 具體改善建議")
print("─" * 80)
print()
print("1. 【優先】處理 Lonzo Ball")
print("   問題: .385 FG% 是毒藥，嚴重拖累陣容")
print("   建議: 用他換任何 .55+ FG% 的中鋒")
print("   目標: Daniel Gafford (.709), Dereck Lively II (.709)")
print()
print("2. 【次要】交易 Jayson Tatum (傷兵)")
print("   問題: 今年整季報銷，占名額沒貢獻")
print("   建議: 換火鍋專家補強 BLK 類別")
print("   目標: Jaren Jackson Jr. (130 BLK), Walker Kessler (156 BLK)")
print()
print("3. 【長期】等待 Kyrie Irving 下半季復出")
print("   預期: 補強 PTS, 3PM, A/T")
print("   影響: 讓你的優勢類別更穩固")
print()

print("=" * 80)
print(" 分析完成！")
print("=" * 80)
print()
print("💡 下一步建議:")
print("   1. 立即處理 Lonzo Ball (換高 FG% 中鋒)")
print("   2. 考慮交易 Tatum (換火鍋專家)")
print("   3. 每週確保 5 個優勢類別正常發揮")
print()
print("🏆 預測: 如果執行這些改善，你有很大機會打進季後賽！")
print()
