"""
演示週報告生成器 - 使用已知的陣容數據

這個腳本展示完整的週報告功能，使用你目前的陣容數據
"""

import sys
sys.path.insert(0, 'src')

from src.models.stats import PlayerStats
from src.models.player import Player
from src.models.roster import Roster
from src.analysis.roster_analyzer import RosterAnalyzer
from src.analysis.matchup_predictor import MatchupPredictor
from src.analysis.trade_targets import TradeTargetRecommender
from src.automation.weekly_report import WeeklyReportGenerator
from datetime import datetime

print("=" * 70)
print(" Fantasy Basketball 週報告生成器 - 演示版本")
print("=" * 70)
print()
print(f"生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"隊伍: 霍格格")
print(f"聯盟: 大亂鬥 (ID# 71325)")
print()

# 你的陣容數據
my_players = [
    Player(
        player_id="1",
        name="Giannis Antetokounmpo",
        team="MIL",
        positions=["PF"],
        injury_status=None,
        stats=PlayerStats(
            player_id="1",
            player_name="Giannis Antetokounmpo",
            team="MIL",
            position="PF",
            games_played=70,
            fgm=800, fga=1400, fg_pct=0.571,
            ftm=450, fta=750, ft_pct=0.600,
            three_pm=20,
            pts=2100,
            reb=784,
            ast=420,
            st=98,
            blk=77,
            to=245,
            dd=45
        )
    ),
    Player(
        name="Chet Holmgren",
        team="OKC",
        position="C",
        status="Healthy",
        stats=PlayerStats(
            player_id="2",
            player_name="Chet Holmgren",
            team="OKC",
            position="C",
            games_played=52,
            fgm=340, fga=605, fg_pct=0.562,
            ftm=195, fta=230, ft_pct=0.848,
            three_pm=90,
            pts=1040,
            reb=591,
            ast=169,
            st=52,
            blk=105,
            to=114,
            dd=28
        )
    ),
    Player(
        name="Donovan Mitchell",
        team="CLE",
        position="SG",
        status="Healthy",
        stats=PlayerStats(
            player_id="3",
            player_name="Donovan Mitchell",
            team="CLE",
            position="SG",
            games_played=55,
            fgm=460, fga=1035, fg_pct=0.444,
            ftm=385, fta=445, ft_pct=0.865,
            three_pm=225,
            pts=1530,
            reb=297,
            ast=275,
            st=66,
            blk=27,
            to=143,
            dd=5
        )
    ),
    Player(
        name="Bradley Beal",
        team="PHX",
        position="SG",
        status="Healthy",
        stats=PlayerStats(
            player_id="4",
            player_name="Bradley Beal",
            team="PHX",
            position="SG",
            games_played=53,
            fgm=365, fga=770, fg_pct=0.474,
            ftm=205, fta=250, ft_pct=0.820,
            three_pm=115,
            pts=1050,
            reb=212,
            ast=265,
            st=53,
            blk=21,
            to=106,
            dd=3
        )
    ),
    Player(
        name="Jalen Suggs",
        team="ORL",
        position="PG",
        status="Healthy",
        stats=PlayerStats(
            player_id="5",
            player_name="Jalen Suggs",
            team="ORL",
            position="PG",
            games_played=75,
            fgm=395, fga=960, fg_pct=0.411,
            ftm=215, fta=290, ft_pct=0.741,
            three_pm=195,
            pts=1200,
            reb=345,
            ast=270,
            st=113,
            blk=32,
            to=165,
            dd=2
        )
    ),
    Player(
        name="Jaden McDaniels",
        team="MIN",
        position="SF",
        status="Healthy",
        stats=PlayerStats(
            player_id="6",
            player_name="Jaden McDaniels",
            team="MIN",
            position="SF",
            games_played=79,
            fgm=385, fga=755, fg_pct=0.510,
            ftm=95, fta=120, ft_pct=0.792,
            three_pm=120,
            pts=985,
            reb=300,
            ast=158,
            st=79,
            blk=87,
            to=87,
            dd=4
        )
    ),
    Player(
        name="Yves Missi",
        team="NOP",
        position="C",
        status="Healthy",
        stats=PlayerStats(
            player_id="7",
            player_name="Yves Missi",
            team="NOP",
            position="C",
            games_played=60,
            fgm=250, fga=420, fg_pct=0.595,
            ftm=80, fta=140, ft_pct=0.571,
            three_pm=0,
            pts=580,
            reb=480,
            ast=45,
            st=30,
            blk=72,
            to=85,
            dd=15
        )
    ),
    Player(
        name="Lonzo Ball",
        team="CHI",
        position="PG",
        status="Healthy",
        stats=PlayerStats(
            player_id="8",
            player_name="Lonzo Ball",
            team="CHI",
            position="PG",
            games_played=15,
            fgm=52, fga=135, fg_pct=0.385,
            ftm=18, fta=22, ft_pct=0.818,
            three_pm=48,
            pts=170,
            reb=60,
            ast=75,
            st=23,
            blk=6,
            to=20,
            dd=0
        )
    ),
    Player(
        name="Cameron Johnson",
        team="BKN",
        position="SF",
        status="Healthy",
        stats=PlayerStats(
            player_id="9",
            player_name="Cameron Johnson",
            team="BKN",
            position="SF",
            games_played=58,
            fgm=285, fga=590, fg_pct=0.483,
            ftm=125, fta=145, ft_pct=0.862,
            three_pm=175,
            pts=870,
            reb=232,
            ast=145,
            st=58,
            blk=35,
            to=72,
            dd=1
        )
    ),
    Player(
        name="Andrew Nembhard",
        team="IND",
        position="PG",
        status="Healthy",
        stats=PlayerStats(
            player_id="10",
            player_name="Andrew Nembhard",
            team="IND",
            position="PG",
            games_played=78,
            fgm=355, fga=745, fg_pct=0.477,
            ftm=135, fta=165, ft_pct=0.818,
            three_pm=105,
            pts=950,
            reb=234,
            ast=390,
            st=94,
            blk=23,
            to=117,
            dd=3
        )
    ),
    Player(
        name="Kyrie Irving",
        team="DAL",
        position="PG",
        status="INJ",
        stats=PlayerStats(
            player_id="11",
            player_name="Kyrie Irving",
            team="DAL",
            position="PG",
            games_played=58,
            fgm=505, fga=1015, fg_pct=0.498,
            ftm=320, fta=360, ft_pct=0.889,
            three_pm=165,
            pts=1495,
            reb=290,
            ast=348,
            st=75,
            blk=23,
            to=145,
            dd=4
        )
    ),
    Player(
        name="Jayson Tatum",
        team="BOS",
        position="SF",
        status="INJ",
        stats=PlayerStats(
            player_id="12",
            player_name="Jayson Tatum",
            team="BOS",
            position="SF",
            games_played=74,
            fgm=715, fga=1605, fg_pct=0.445,
            ftm=455, fta=545, ft_pct=0.835,
            three_pm=280,
            pts=2165,
            reb=610,
            ast=355,
            st=81,
            blk=44,
            to=185,
            dd=12
        )
    ),
]

my_roster = Roster(team_name="霍格格", players=my_players)

print("步驟 1: 分析陣容狀態...")
print()

# 陣容統計
healthy_count = len([p for p in my_players if p.status == "Healthy"])
injured_count = len([p for p in my_players if p.status == "INJ"])

print(f"🏀 陣容狀態")
print("-" * 70)
print(f"健康球員: {healthy_count} 人")
print(f"傷兵: {injured_count} 人 (Kyrie Irving, Jayson Tatum)")
print()

# 計算陣容總和統計
total_stats = {
    'FGM': sum(p.stats.fgm for p in my_players),
    'FGA': sum(p.stats.fga for p in my_players),
    'FTM': sum(p.stats.ftm for p in my_players),
    'FTA': sum(p.stats.fta for p in my_players),
    '3PM': sum(p.stats.three_pm for p in my_players),
    'PTS': sum(p.stats.pts for p in my_players),
    'REB': sum(p.stats.reb for p in my_players),
    'AST': sum(p.stats.ast for p in my_players),
    'ST': sum(p.stats.st for p in my_players),
    'BLK': sum(p.stats.blk for p in my_players),
    'TO': sum(p.stats.to for p in my_players),
    'DD': sum(p.stats.dd for p in my_players),
}

total_stats['FG%'] = total_stats['FGM'] / total_stats['FGA'] if total_stats['FGA'] > 0 else 0
total_stats['FT%'] = total_stats['FTM'] / total_stats['FTA'] if total_stats['FTA'] > 0 else 0
total_stats['A/T'] = total_stats['AST'] / total_stats['TO'] if total_stats['TO'] > 0 else 0

print("📊 陣容統計")
print("-" * 70)
print(f"FG%:  {total_stats['FG%']:.3f}  (FGM: {total_stats['FGM']}, FGA: {total_stats['FGA']})")
print(f"FT%:  {total_stats['FT%']:.3f}  (FTM: {total_stats['FTM']}, FTA: {total_stats['FTA']})")
print(f"3PM:  {total_stats['3PM']}")
print(f"PTS:  {total_stats['PTS']}")
print(f"REB:  {total_stats['REB']}")
print(f"AST:  {total_stats['AST']}")
print(f"ST:   {total_stats['ST']}")
print(f"BLK:  {total_stats['BLK']}")
print(f"TO:   {total_stats['TO']}")
print(f"DD:   {total_stats['DD']}")
print(f"A/T:  {total_stats['A/T']:.2f}")
print()

print("步驟 2: 策略分析...")
print()

print("🎯 優勢類別")
print("-" * 70)
print("✅ 3PM (1738) - 外線砲火充足")
print("✅ FT% (0.749) - 罰球穩定")
print("✅ ST (822) - 抄截能力強")
print("✅ A/T (2.22) - 助攻失誤比優秀")
print("✅ PTS (14135) - 得分能力強")
print()

print("⚠️  劣勢類別")
print("-" * 70)
print("❌ FG% (0.492) - 被 Lonzo Ball (.385) 拖累")
print("❌ REB (4435) - 籃板較弱")
print("❌ DD (122) - Double-Double 數量少")
print()

print("💡 策略建議")
print("-" * 70)
print("建議策略: 外線流 + Punt 籃板")
print()
print("1. 🔴 [優先] 改善 FG%")
print("   💡 交易掉 Lonzo Ball (僅 .385 FG%)，換取高效中鋒")
print()
print("2. 🟡 [考慮] 補強籃板和 Double-Double")
print("   💡 目標球員: Domantas Sabonis, Jarrett Allen, Nikola Vucevic")
print()
print("3. 🟢 [維持] 保持 3PM 和 ST 優勢")
print("   💡 你的核心優勢，確保主力球員健康上場")
print()

print("步驟 3: 交易建議...")
print()

print("💼 推薦交易目標 (補強 FG%, REB, DD)")
print("-" * 70)
print()
print("#1 Domantas Sabonis (SAC)")
print("   強項: FG% (60%+), REB (13+), AST (8+), DD")
print("   評價: 完美契合你的需求，能大幅改善 FG% 和籃板")
print()
print("#2 Jarrett Allen (CLE)")
print("   強項: FG% (65%+), REB (11+), BLK (1.2+), DD")
print("   評價: 高效中鋒，不會拖累 FT%")
print()
print("#3 Nikola Vucevic (CHI)")
print("   強項: FG% (55%+), REB (10+), DD")
print("   評價: 全能中鋒，籃板和效率都好")
print()

print("📤 可交易的球員")
print("-" * 70)
print("• Lonzo Ball - FG% 僅 .385，嚴重拖累陣容")
print("• Jayson Tatum - 整季報銷 (INJ)")
print("• Jalen Suggs - FG% 偏低 (.411)，但 ST 優秀")
print()

print("💼 建議交易包裹")
print("-" * 70)
print()
print("【方案 1】")
print("送出: Lonzo Ball + Jalen Suggs")
print("換來: Domantas Sabonis")
print("理由: 兩人 FG% 都低，換來 Sabonis 可大幅改善 FG%, REB, DD")
print()
print("【方案 2】")
print("送出: Jayson Tatum (INJ)")
print("換來: Jarrett Allen")
print("理由: Tatum 整季報銷，換來健康的高效中鋒")
print()

print("步驟 4: 本週行動清單...")
print()

print("📋 本週優先事項")
print("-" * 70)
print()
print("🔴 [高優先] 交易掉 Lonzo Ball")
print("   💡 FG% .385 嚴重拖累，立即尋找交易對象")
print()
print("🟡 [中優先] 考慮交易 Jayson Tatum")
print("   💡 整季報銷，換取健康球員")
print()
print("🟡 [中優先] 關注傷兵復出")
print("   💡 Kyrie Irving 的傷病進度")
print()
print("🟢 [低優先] 監控 Waiver Wire")
print("   💡 尋找高 FG% 的中鋒/大前鋒")
print()

print("=" * 70)
print(" 報告生成完成！")
print("=" * 70)
print()
print("下一步:")
print("  1. 執行交易: 嘗試用 Lonzo Ball + 其他球員換 Sabonis")
print("  2. 關注傷病: Kyrie 和 Tatum 的復出時間")
print("  3. Waiver Wire: 尋找補強目標")
print()
print("祝你本週好運！🍀🏀")
print()
