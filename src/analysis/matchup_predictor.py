"""
每週對戰預測引擎

功能：
1. 預測下週對戰的勝率
2. 分析對手的強弱勢
3. 給出針對性策略建議
"""

from typing import Dict, List, Tuple
from ..models.roster import Roster
from ..models.stats import CategoryStats
from .category_scorer import CategoryScorer


class MatchupPredictor:
    """對戰預測器"""

    CATEGORIES = ['FG%', 'FT%', '3PM', 'PTS', 'REB', 'AST', 'ST', 'BLK', 'TO']

    def __init__(self):
        """初始化預測器"""
        self.scorer = CategoryScorer()

    def predict_matchup(
        self,
        my_roster: Roster,
        opponent_roster: Roster
    ) -> Dict:
        """
        預測對戰結果

        Args:
            my_roster: 你的陣容
            opponent_roster: 對手的陣容

        Returns:
            預測結果字典
        """
        # 計算雙方的類別總計
        my_stats = my_roster.get_category_totals(include_injured=False)
        opp_stats = opponent_roster.get_category_totals(include_injured=False)

        # 逐類別比較
        category_predictions = {}
        wins = 0
        losses = 0
        ties = 0

        for cat in self.CATEGORIES:
            result = self._compare_category(cat, my_stats, opp_stats)
            category_predictions[cat] = result

            if result['winner'] == 'me':
                wins += 1
            elif result['winner'] == 'opponent':
                losses += 1
            else:
                ties += 1

        # 計算勝率
        total = wins + losses + ties
        win_probability = (wins + ties * 0.5) / total if total > 0 else 0

        # 生成策略建議
        strategies = self._generate_strategies(category_predictions, my_stats, opp_stats)

        return {
            'prediction': {
                'wins': wins,
                'losses': losses,
                'ties': ties,
                'win_probability': win_probability,
                'outcome': 'Win' if wins > losses else 'Loss' if losses > wins else 'Tie'
            },
            'category_breakdown': category_predictions,
            'strategies': strategies,
            'my_stats': my_stats.to_dict(),
            'opponent_stats': opp_stats.to_dict()
        }

    def _compare_category(
        self,
        category: str,
        my_stats: CategoryStats,
        opp_stats: CategoryStats
    ) -> Dict:
        """
        比較單一類別

        Args:
            category: 類別名稱
            my_stats: 我的統計
            opp_stats: 對手統計

        Returns:
            比較結果
        """
        # 獲取數值
        if category == 'FG%':
            my_val = my_stats.fg_pct
            opp_val = opp_stats.fg_pct
        elif category == 'FT%':
            my_val = my_stats.ft_pct
            opp_val = opp_stats.ft_pct
        elif category == '3PM':
            my_val = my_stats.three_pm
            opp_val = opp_stats.three_pm
        elif category == 'PTS':
            my_val = my_stats.pts
            opp_val = opp_stats.pts
        elif category == 'REB':
            my_val = my_stats.reb
            opp_val = opp_stats.reb
        elif category == 'AST':
            my_val = my_stats.ast
            opp_val = opp_stats.ast
        elif category == 'ST':
            my_val = my_stats.st
            opp_val = opp_stats.st
        elif category == 'BLK':
            my_val = my_stats.blk
            opp_val = opp_stats.blk
        elif category == 'TO':
            # 失誤越少越好
            my_val = my_stats.to
            opp_val = opp_stats.to
            winner = 'me' if my_val < opp_val else 'opponent' if opp_val < my_val else 'tie'
            margin = abs(my_val - opp_val)
            return {
                'my_value': my_val,
                'opponent_value': opp_val,
                'winner': winner,
                'margin': margin,
                'confidence': self._calculate_confidence(margin, my_val, opp_val)
            }
        else:
            my_val = 0
            opp_val = 0

        # 判斷勝負
        if my_val > opp_val:
            winner = 'me'
        elif opp_val > my_val:
            winner = 'opponent'
        else:
            winner = 'tie'

        margin = abs(my_val - opp_val)

        return {
            'my_value': my_val,
            'opponent_value': opp_val,
            'winner': winner,
            'margin': margin,
            'confidence': self._calculate_confidence(margin, my_val, opp_val)
        }

    def _calculate_confidence(self, margin: float, my_val: float, opp_val: float) -> str:
        """
        計算勝負的信心程度

        Args:
            margin: 差距
            my_val: 我的數值
            opp_val: 對手數值

        Returns:
            信心等級 (High, Medium, Low)
        """
        if my_val == 0 or opp_val == 0:
            return "Unknown"

        # 計算差距百分比
        total = max(my_val, opp_val)
        margin_pct = (margin / total) * 100 if total > 0 else 0

        if margin_pct > 20:
            return "High"
        elif margin_pct > 10:
            return "Medium"
        else:
            return "Low"

    def _generate_strategies(
        self,
        category_predictions: Dict,
        my_stats: CategoryStats,
        opp_stats: CategoryStats
    ) -> List[Dict]:
        """
        生成策略建議

        Args:
            category_predictions: 類別預測結果
            my_stats: 我的統計
            opp_stats: 對手統計

        Returns:
            策略建議列表
        """
        strategies = []

        # 分析接近的類別（可爭取的）
        close_categories = []
        for cat, pred in category_predictions.items():
            if pred['confidence'] == 'Low' and pred['winner'] != 'me':
                close_categories.append(cat)

        if close_categories:
            strategies.append({
                'type': 'Focus',
                'priority': 'High',
                'message': f"接近的類別需要加強: {', '.join(close_categories)}",
                'action': f"這些類別還有機會爭取，注意球員的先發陣容調整"
            })

        # 分析穩贏的類別
        safe_wins = [cat for cat, pred in category_predictions.items()
                     if pred['winner'] == 'me' and pred['confidence'] == 'High']

        if safe_wins:
            strategies.append({
                'type': 'Maintain',
                'priority': 'Medium',
                'message': f"穩贏的類別: {', '.join(safe_wins)}",
                'action': "保持現狀，確保主力球員健康上場"
            })

        # 分析必輸的類別
        sure_losses = [cat for cat, pred in category_predictions.items()
                       if pred['winner'] == 'opponent' and pred['confidence'] == 'High']

        if sure_losses:
            strategies.append({
                'type': 'Punt',
                'priority': 'Low',
                'message': f"可能輸掉的類別: {', '.join(sure_losses)}",
                'action': "不用特別在意這些類別，專注在可以贏的類別"
            })

        # 整體策略
        wins = sum(1 for p in category_predictions.values() if p['winner'] == 'me')
        if wins >= 5:
            strategies.append({
                'type': 'Overall',
                'priority': 'High',
                'message': f"預測可以贏 {wins}/9 個類別",
                'action': "✅ 勝算很大！保持陣容穩定即可"
            })
        elif wins >= 4:
            strategies.append({
                'type': 'Overall',
                'priority': 'High',
                'message': f"預測可以贏 {wins}/9 個類別",
                'action': "⚠️ 勝負在伯仲之間，需要仔細調整陣容"
            })
        else:
            strategies.append({
                'type': 'Overall',
                'priority': 'High',
                'message': f"預測可以贏 {wins}/9 個類別",
                'action': "❌ 形勢不利，考慮交易補強或調整策略"
            })

        return strategies

    def generate_matchup_report(self, prediction: Dict) -> str:
        """
        生成對戰報告

        Args:
            prediction: 預測結果

        Returns:
            格式化的報告字串
        """
        report = []
        report.append("=" * 70)
        report.append(" 週對戰預測報告")
        report.append("=" * 70)
        report.append("")

        pred = prediction['prediction']
        report.append(f"預測結果: {pred['outcome']}")
        report.append(f"預計贏: {pred['wins']} 個類別")
        report.append(f"預計輸: {pred['losses']} 個類別")
        report.append(f"預計平: {pred['ties']} 個類別")
        report.append(f"勝率: {pred['win_probability'] * 100:.1f}%")
        report.append("")

        report.append("📊 類別詳細分析")
        report.append("─" * 70)

        for cat, pred_cat in prediction['category_breakdown'].items():
            winner_icon = "✅" if pred_cat['winner'] == 'me' else "❌" if pred_cat['winner'] == 'opponent' else "⚖️"
            my_val = pred_cat['my_value']
            opp_val = pred_cat['opponent_value']
            confidence = pred_cat['confidence']

            if cat in ['FG%', 'FT%']:
                report.append(f"{winner_icon} {cat}: {my_val:.3f} vs {opp_val:.3f} ({confidence})")
            else:
                report.append(f"{winner_icon} {cat}: {my_val} vs {opp_val} ({confidence})")

        report.append("")
        report.append("🎯 策略建議")
        report.append("─" * 70)

        for strategy in prediction['strategies']:
            priority_icon = "🔴" if strategy['priority'] == 'High' else "🟡" if strategy['priority'] == 'Medium' else "🟢"
            report.append(f"{priority_icon} [{strategy['type']}] {strategy['message']}")
            report.append(f"   💡 {strategy['action']}")
            report.append("")

        report.append("=" * 70)

        return "\n".join(report)


# 測試範例
if __name__ == "__main__":
    print("對戰預測引擎已就緒")
    print("使用方式:")
    print()
    print("from src.analysis.matchup_predictor import MatchupPredictor")
    print()
    print("predictor = MatchupPredictor()")
    print("prediction = predictor.predict_matchup(my_roster, opponent_roster)")
    print("report = predictor.generate_matchup_report(prediction)")
    print("print(report)")
