"""
Fantasy Basketball Analyzer 主程式

使用範例和快速入門
"""

import json
from pathlib import Path
from api.yahoo_client import YahooFantasyClient
from models.player import Player
from models.roster import Roster
from models.stats import PlayerStats
from analysis.roster_analyzer import RosterAnalyzer
from analysis.trade_analyzer import TradeAnalyzer
from analysis.category_scorer import CategoryScorer


def example_1_get_league_data():
    """範例 1: 獲取聯盟數據"""
    print("=" * 60)
    print("範例 1: 獲取聯盟數據")
    print("=" * 60)

    # 初始化客戶端
    client = YahooFantasyClient()

    # 獲取聯盟資訊
    league_info = client.get_league_info()
    print(f"\n聯盟名稱: {league_info.name}")
    print(f"隊伍數量: {league_info.num_teams}")
    print(f"當前週次: {league_info.current_week}")

    # 獲取排名
    standings = client.get_league_standings()
    print("\n聯盟排名:")
    for team in standings:
        print(f"  {team.name}: {team.team_standings.rank}名")


def example_2_analyze_roster():
    """範例 2: 分析你的陣容"""
    print("\n" + "=" * 60)
    print("範例 2: 分析陣容優劣勢")
    print("=" * 60)

    # 這裡使用模擬數據示範
    # 實際使用時，你會從 Yahoo API 獲取真實數據

    # 建立你的陣容（示例）
    giannis = Player(
        player_id="nba.p.4912",
        name="Giannis Antetokounmpo",
        team="MIL",
        positions=["PF", "C"],
        stats=PlayerStats(
            player_id="nba.p.4912",
            player_name="Giannis Antetokounmpo",
            team="MIL",
            position="PF,C",
            games_played=68,
            fgm=800, fga=1400, fg_pct=0.571,
            ftm=400, fta=600, ft_pct=0.667,
            three_pm=50,
            pts=2100, reb=784, ast=350, st=70, blk=55, to=200
        )
    )

    mitchell = Player(
        player_id="nba.p.5432",
        name="Donovan Mitchell",
        team="CLE",
        positions=["PG", "SG"],
        stats=PlayerStats(
            player_id="nba.p.5432",
            player_name="Donovan Mitchell",
            team="CLE",
            position="PG,SG",
            games_played=75,
            fgm=650, fga=1400, fg_pct=0.464,
            ftm=450, fta=500, ft_pct=0.900,
            three_pm=230,
            pts=1800, reb=250, ast=420, st=95, blk=20, to=150
        )
    )

    my_roster = Roster(
        team_name="我的隊伍",
        players=[giannis, mitchell]
    )

    # 分析陣容
    analyzer = RosterAnalyzer(my_roster)
    report = analyzer.get_roster_report()

    print(f"\n隊伍名稱: {report['team_name']}")
    print(f"陣容人數: {report['roster_size']['active']} 人")

    print("\n類別總計:")
    for cat, value in report['category_totals'].items():
        print(f"  {cat}: {value}")

    print("\n改善建議:")
    suggestions = analyzer.suggest_improvements()
    for suggestion in suggestions:
        print(f"\n  [{suggestion['priority']}] {suggestion['issue']}")
        print(f"  建議: {suggestion['recommendation']}")


def example_3_evaluate_trade():
    """範例 3: 評估交易"""
    print("\n" + "=" * 60)
    print("範例 3: 評估交易影響")
    print("=" * 60)

    # 建立陣容（示例）
    my_roster = Roster(
        team_name="我的隊伍",
        players=[
            Player(
                player_id="nba.p.1",
                name="Donovan Mitchell",
                team="CLE",
                positions=["PG", "SG"],
                stats=PlayerStats(
                    player_id="nba.p.1",
                    player_name="Donovan Mitchell",
                    team="CLE",
                    position="PG,SG",
                    games_played=75,
                    fgm=650, fga=1400, fg_pct=0.464,
                    ftm=450, fta=500, ft_pct=0.900,
                    three_pm=230,
                    pts=1800, reb=250, ast=420, st=95, blk=20, to=150
                )
            )
        ]
    )

    # 評估交易: 送出 Mitchell，換來 Sabonis
    trade_analyzer = TradeAnalyzer(my_roster)

    give_players = [my_roster.players[0]]  # Mitchell

    receive_players = [
        Player(
            player_id="nba.p.2",
            name="Domantas Sabonis",
            team="SAC",
            positions=["PF", "C"],
            stats=PlayerStats(
                player_id="nba.p.2",
                player_name="Domantas Sabonis",
                team="SAC",
                position="PF,C",
                games_played=70,
                fgm=700, fga=1200, fg_pct=0.583,
                ftm=300, fta=400, ft_pct=0.750,
                three_pm=20,
                pts=1600, reb=900, ast=550, st=60, blk=30, to=180
            )
        )
    ]

    result = trade_analyzer.evaluate_trade(give_players, receive_players)

    print(f"\n交易方案:")
    print(f"  送出: {', '.join(result['trade_summary']['give'])}")
    print(f"  換來: {', '.join(result['trade_summary']['receive'])}")

    print(f"\n總評: {result['recommendation']['overall']}")
    print(f"原因: {result['recommendation']['reason']}")
    print(f"建議: {result['recommendation']['decision']}")

    print("\n類別影響:")
    for cat, data in result['category_changes'].items():
        if data['impact'] != 'Neutral':
            print(f"  {cat}: {data['before']} → {data['after']} ({data['impact']})")


def example_4_rank_players():
    """範例 4: 球員排名"""
    print("\n" + "=" * 60)
    print("範例 4: 球員價值排名 (基於 Z-Score)")
    print("=" * 60)

    # 建立球員列表（示例）
    players_stats = [
        PlayerStats(
            player_id="1", player_name="Giannis", team="MIL", position="PF",
            games_played=68,
            fgm=800, fga=1400, fg_pct=0.571,
            ftm=400, fta=600, ft_pct=0.667,
            three_pm=50, pts=2100, reb=784, ast=350, st=70, blk=55, to=200
        ),
        PlayerStats(
            player_id="2", player_name="Luka Doncic", team="DAL", position="PG",
            games_played=70,
            fgm=750, fga=1500, fg_pct=0.500,
            ftm=550, fta=650, ft_pct=0.846,
            three_pm=180, pts=2000, reb=600, ast=700, st=80, blk=30, to=250
        ),
        PlayerStats(
            player_id="3", player_name="Sabonis", team="SAC", position="C",
            games_played=70,
            fgm=700, fga=1200, fg_pct=0.583,
            ftm=300, fta=400, ft_pct=0.750,
            three_pm=20, pts=1600, reb=900, ast=550, st=60, blk=30, to=180
        )
    ]

    scorer = CategoryScorer()
    rankings = scorer.rank_players(players_stats)

    print("\n球員排名:")
    for player in rankings[:10]:  # 顯示前 10 名
        print(f"\n#{player['rank']} {player['player_name']} ({player['team']})")
        print(f"  總價值: {player['total_value']:.2f}")
        print(f"  優勢類別: ", end="")
        strong_cats = [cat for cat in CategoryScorer.CATEGORIES if player.get(cat, 0) > 1.0]
        print(", ".join(strong_cats) if strong_cats else "無明顯優勢")


def main():
    """主程式"""
    print("\n" + "=" * 60)
    print(" Fantasy Basketball Analyzer - 使用範例")
    print("=" * 60)

    print("\n請選擇要執行的範例:")
    print("1. 獲取聯盟數據 (需要 Yahoo API 認證)")
    print("2. 分析陣容優劣勢")
    print("3. 評估交易影響")
    print("4. 球員價值排名")
    print("0. 退出")

    choice = input("\n請輸入選項 (0-4): ")

    if choice == "1":
        try:
            example_1_get_league_data()
        except Exception as e:
            print(f"\n錯誤: {e}")
            print("\n請確認:")
            print("1. 已建立 config/credentials.json 並填入正確的 Yahoo API 認證資訊")
            print("2. 已完成 OAuth 認證流程")
    elif choice == "2":
        example_2_analyze_roster()
    elif choice == "3":
        example_3_evaluate_trade()
    elif choice == "4":
        example_4_rank_players()
    elif choice == "0":
        print("\n再見！")
    else:
        print("\n無效的選項")


if __name__ == "__main__":
    main()
