"""
交易目標推薦系統

基於你的陣容弱點，智能推薦應該交易的目標球員
"""

from typing import List, Dict
from ..models.roster import Roster
from ..models.stats import PlayerStats
from .category_scorer import CategoryScorer
from .roster_analyzer import RosterAnalyzer


class TradeTargetRecommender:
    """交易目標推薦器"""

    def __init__(self, my_roster: Roster, available_players: List[PlayerStats]):
        """
        初始化推薦器

        Args:
            my_roster: 你的陣容
            available_players: 可交易的球員列表（全聯盟或自由球員）
        """
        self.my_roster = my_roster
        self.available_players = available_players
        self.scorer = CategoryScorer()
        self.analyzer = RosterAnalyzer(my_roster, available_players)

        # 計算聯盟平均
        if available_players:
            self.scorer.calculate_league_averages(available_players)

    def recommend_targets(
        self,
        target_categories: List[str] = None,
        exclude_my_players: bool = True,
        max_results: int = 20
    ) -> List[Dict]:
        """
        推薦交易目標

        Args:
            target_categories: 想要補強的類別，若不指定則自動偵測弱項
            exclude_my_players: 是否排除自己的球員
            max_results: 最多返回幾個結果

        Returns:
            推薦球員列表
        """
        # 自動偵測弱項
        if not target_categories:
            punt_cats = self.analyzer.identify_punt_categories(threshold=-0.5)
            target_categories = punt_cats

        if not target_categories:
            print("你的陣容很平衡，沒有明顯弱項！")
            return []

        print(f"正在尋找能補強 {', '.join(target_categories)} 的球員...")

        # 對所有球員評分
        recommendations = []

        for stats in self.available_players:
            if stats.games_played == 0:
                continue

            # 排除自己的球員
            if exclude_my_players:
                if any(p.stats and p.stats.player_id == stats.player_id
                       for p in self.my_roster.players):
                    continue

            # 計算在目標類別的得分
            z_scores = self.scorer.calculate_player_value(stats)
            target_score = sum(z_scores.get(cat, 0) for cat in target_categories)

            # 計算總體價值
            total_value = self.scorer.calculate_total_value(stats)

            recommendations.append({
                'player_name': stats.player_name,
                'team': stats.team,
                'target_score': round(target_score, 2),
                'total_value': round(total_value, 2),
                'category_scores': {
                    cat: round(z_scores.get(cat, 0), 2)
                    for cat in target_categories
                },
                'injury_status': stats.injury_status,
                'stats': {
                    'FG%': stats.fg_pct,
                    'FT%': stats.ft_pct,
                    '3PM': stats.three_pm,
                    'PTS': stats.pts,
                    'REB': stats.reb,
                    'AST': stats.ast,
                    'ST': stats.st,
                    'BLK': stats.blk,
                    'TO': stats.to
                }
            })

        # 按目標分數排序
        recommendations.sort(key=lambda x: x['target_score'], reverse=True)

        return recommendations[:max_results]

    def suggest_trade_packages(
        self,
        give_away_candidates: List[str] = None
    ) -> List[Dict]:
        """
        建議交易包裹

        Args:
            give_away_candidates: 可以送出的球員名單

        Returns:
            交易包裹建議
        """
        # 找出陣容中表現不佳的球員
        if not give_away_candidates:
            give_away_candidates = self._identify_expendable_players()

        punt_cats = self.analyzer.identify_punt_categories()
        strong_cats = self.analyzer.identify_strong_categories()

        trade_packages = []

        for player_name in give_away_candidates:
            # 找到這個球員
            player = next((p for p in self.my_roster.players if p.name == player_name), None)
            if not player or not player.stats:
                continue

            # 分析這個球員的強項
            player_z = self.scorer.calculate_player_value(player.stats)
            player_strong_cats = [cat for cat, z in player_z.items() if z > 0.5]

            # 推薦交易目標（補強我們的弱項）
            targets = self.recommend_targets(
                target_categories=punt_cats,
                max_results=5
            )

            if targets:
                trade_packages.append({
                    'give': player_name,
                    'give_strengths': player_strong_cats,
                    'reason': f"送出 {player_name}，他在你的劣勢類別表現好，但對你用處不大",
                    'get_suggestions': [
                        {
                            'name': t['player_name'],
                            'reason': f"能補強 {', '.join([c for c in punt_cats if t['category_scores'].get(c, 0) > 1.0])}",
                            'value_comparison': f"{player.stats.player_name} 總價值 vs {t['player_name']} 總價值"
                        }
                        for t in targets[:3]
                    ]
                })

        return trade_packages

    def _identify_expendable_players(self) -> List[str]:
        """
        識別可以交易出去的球員

        Returns:
            可交易球員名單
        """
        expendable = []
        strong_cats = self.analyzer.identify_strong_categories()

        for player in self.my_roster.players:
            if not player.stats or player.stats.games_played == 0:
                # 傷兵
                if player.injury_status == 'INJ':
                    expendable.append(player.name)
                continue

            # 計算球員的 Z-Score
            z_scores = self.scorer.calculate_player_value(player.stats)

            # 如果球員在我們的劣勢類別表現好，但在優勢類別表現不好
            player_strong = [cat for cat, z in z_scores.items() if z > 0.5]
            player_weak = [cat for cat, z in z_scores.items() if z < -0.5]

            # 如果球員的強項不在我們的優勢類別中
            if not any(cat in strong_cats for cat in player_strong):
                expendable.append(player.name)

        return expendable

    def generate_trade_report(self) -> str:
        """
        生成交易建議報告

        Returns:
            格式化的報告
        """
        report = []
        report.append("=" * 70)
        report.append(" 交易目標推薦報告")
        report.append("=" * 70)
        report.append("")

        # 分析弱項
        punt_cats = self.analyzer.identify_punt_categories()
        strong_cats = self.analyzer.identify_strong_categories()

        report.append("📊 陣容分析")
        report.append("─" * 70)
        report.append(f"優勢類別: {', '.join(strong_cats)}")
        report.append(f"劣勢類別: {', '.join(punt_cats)}")
        report.append("")

        # 推薦目標
        if punt_cats:
            report.append(f"🎯 推薦補強 {', '.join(punt_cats)} 的球員")
            report.append("─" * 70)

            targets = self.recommend_targets(target_categories=punt_cats, max_results=10)

            for i, target in enumerate(targets, 1):
                report.append(f"\n#{i} {target['player_name']} ({target['team']})")
                report.append(f"   目標分數: {target['target_score']}")
                report.append(f"   總價值: {target['total_value']}")

                strong_in_target = [
                    cat for cat, score in target['category_scores'].items()
                    if score > 1.0
                ]
                if strong_in_target:
                    report.append(f"   強項: {', '.join(strong_in_target)}")

        # 可交易的球員
        report.append("")
        report.append("📤 可以交易出去的球員")
        report.append("─" * 70)

        expendable = self._identify_expendable_players()
        if expendable:
            for player_name in expendable:
                report.append(f"  • {player_name}")
        else:
            report.append("  沒有明顯可交易的球員")

        # 交易包裹建議
        report.append("")
        report.append("💼 交易包裹建議")
        report.append("─" * 70)

        packages = self.suggest_trade_packages(give_away_candidates=expendable[:3])

        if packages:
            for pkg in packages:
                report.append(f"\n送出: {pkg['give']}")
                report.append(f"原因: {pkg['reason']}")
                report.append("換來建議:")
                for sug in pkg['get_suggestions']:
                    report.append(f"  • {sug['name']} - {sug['reason']}")
        else:
            report.append("目前沒有明顯的交易建議")

        report.append("")
        report.append("=" * 70)

        return "\n".join(report)


# 使用範例
if __name__ == "__main__":
    print("交易目標推薦系統已就緒")
    print()
    print("使用方式:")
    print()
    print("from src.analysis.trade_targets import TradeTargetRecommender")
    print()
    print("recommender = TradeTargetRecommender(my_roster, all_players)")
    print("targets = recommender.recommend_targets()")
    print("report = recommender.generate_trade_report()")
    print("print(report)")
