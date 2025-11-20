"""
交易分析器 - 評估交易對陣容的影響
"""

from typing import List, Dict
from copy import deepcopy
from ..models.roster import Roster
from ..models.player import Player
from ..models.stats import PlayerStats, calculate_category_totals
from .category_scorer import CategoryScorer


class TradeAnalyzer:
    """交易分析器"""

    def __init__(self, roster: Roster, league_players: List[PlayerStats] = None):
        """
        初始化交易分析器

        Args:
            roster: 你的陣容
            league_players: 聯盟所有球員數據
        """
        self.roster = roster
        self.league_players = league_players
        self.scorer = CategoryScorer()

        if league_players:
            self.scorer.calculate_league_averages(league_players)

    def evaluate_trade(
        self,
        give_players: List[Player],
        receive_players: List[Player]
    ) -> Dict:
        """
        評估交易對陣容的影響

        Args:
            give_players: 送出的球員列表
            receive_players: 換來的球員列表

        Returns:
            交易分析報告
        """
        # 計算交易前的陣容數據
        before_roster = deepcopy(self.roster)
        before_stats = before_roster.get_category_totals(include_injured=False)

        # 計算交易後的陣容數據
        after_roster = deepcopy(self.roster)

        # 移除送出的球員
        after_roster.players = [
            p for p in after_roster.players
            if p.player_id not in [gp.player_id for gp in give_players]
        ]

        # 加入換來的球員
        after_roster.players.extend(receive_players)

        after_stats = after_roster.get_category_totals(include_injured=False)

        # 計算各類別的變化
        category_changes = self._calculate_category_changes(before_stats, after_stats)

        # 計算總價值變化 (如果有聯盟數據)
        value_change = self._calculate_value_change(
            give_players,
            receive_players
        )

        # 生成建議
        recommendation = self._generate_recommendation(category_changes, value_change)

        return {
            'trade_summary': {
                'give': [p.name for p in give_players],
                'receive': [p.name for p in receive_players]
            },
            'category_changes': category_changes,
            'value_change': value_change,
            'recommendation': recommendation,
            'before_stats': before_stats.to_dict(),
            'after_stats': after_stats.to_dict()
        }

    def _calculate_category_changes(self, before, after) -> Dict[str, Dict]:
        """計算各類別的變化"""
        changes = {}

        categories = {
            'FG%': (before.fg_pct, after.fg_pct),
            'FT%': (before.ft_pct, after.ft_pct),
            '3PM': (before.three_pm, after.three_pm),
            'PTS': (before.pts, after.pts),
            'REB': (before.reb, after.reb),
            'AST': (before.ast, after.ast),
            'ST': (before.st, after.st),
            'BLK': (before.blk, after.blk),
            'TO': (before.to, after.to)
        }

        for cat, (before_val, after_val) in categories.items():
            change = after_val - before_val

            # 對百分比類別特殊處理
            if cat in ['FG%', 'FT%']:
                change_pct = ((after_val - before_val) / before_val * 100) if before_val != 0 else 0
                impact = 'Positive' if change > 0 else 'Negative' if change < 0 else 'Neutral'
            elif cat == 'TO':
                # 失誤減少是正面影響
                change_pct = ((after_val - before_val) / before_val * 100) if before_val != 0 else 0
                impact = 'Positive' if change < 0 else 'Negative' if change > 0 else 'Neutral'
            else:
                change_pct = ((after_val - before_val) / before_val * 100) if before_val != 0 else 0
                impact = 'Positive' if change > 0 else 'Negative' if change < 0 else 'Neutral'

            changes[cat] = {
                'before': round(before_val, 3) if cat in ['FG%', 'FT%'] else before_val,
                'after': round(after_val, 3) if cat in ['FG%', 'FT%'] else after_val,
                'change': round(change, 3) if cat in ['FG%', 'FT%'] else change,
                'change_pct': round(change_pct, 1),
                'impact': impact
            }

        return changes

    def _calculate_value_change(
        self,
        give_players: List[Player],
        receive_players: List[Player]
    ) -> Dict:
        """計算總價值變化"""
        if not self.league_players:
            return {'total_value_given': 'N/A', 'total_value_received': 'N/A', 'net_change': 'N/A'}

        # 計算送出球員的總價值
        give_values = []
        for player in give_players:
            if player.stats and player.stats.games_played > 0:
                value = self.scorer.calculate_total_value(player.stats)
                give_values.append({'player': player.name, 'value': round(value, 2)})

        total_give = sum(v['value'] for v in give_values)

        # 計算換來球員的總價值
        receive_values = []
        for player in receive_players:
            if player.stats and player.stats.games_played > 0:
                value = self.scorer.calculate_total_value(player.stats)
                receive_values.append({'player': player.name, 'value': round(value, 2)})

        total_receive = sum(v['value'] for v in receive_values)

        net_change = total_receive - total_give

        return {
            'players_given': give_values,
            'players_received': receive_values,
            'total_value_given': round(total_give, 2),
            'total_value_received': round(total_receive, 2),
            'net_change': round(net_change, 2),
            'verdict': 'Win' if net_change > 0 else 'Loss' if net_change < 0 else 'Fair'
        }

    def _generate_recommendation(self, category_changes: Dict, value_change: Dict) -> Dict:
        """生成交易建議"""
        # 計算正面影響和負面影響的類別數量
        positive_cats = [cat for cat, data in category_changes.items() if data['impact'] == 'Positive']
        negative_cats = [cat for cat, data in category_changes.items() if data['impact'] == 'Negative']

        # 判斷整體影響
        if len(positive_cats) > len(negative_cats):
            overall = 'Favorable'
            reason = f'改善了 {len(positive_cats)} 個類別，只損失 {len(negative_cats)} 個類別'
        elif len(positive_cats) < len(negative_cats):
            overall = 'Unfavorable'
            reason = f'損失了 {len(negative_cats)} 個類別，只改善 {len(positive_cats)} 個類別'
        else:
            overall = 'Neutral'
            reason = f'改善和損失的類別數量相同 ({len(positive_cats)} vs {len(negative_cats)})'

        # 考慮總價值變化 (如果有)
        if isinstance(value_change.get('net_change'), (int, float)):
            net_value = value_change['net_change']
            if net_value > 0.5:
                overall = 'Favorable'
                reason += f'，且總價值增加 {net_value:.2f}'
            elif net_value < -0.5:
                overall = 'Unfavorable'
                reason += f'，且總價值減少 {abs(net_value):.2f}'

        return {
            'overall': overall,
            'reason': reason,
            'improved_categories': positive_cats,
            'weakened_categories': negative_cats,
            'decision': 'Accept' if overall == 'Favorable' else 'Reject' if overall == 'Unfavorable' else 'Consider'
        }

    def suggest_trade_targets(
        self,
        target_categories: List[str],
        max_results: int = 10
    ) -> List[Dict]:
        """
        建議交易目標球員

        Args:
            target_categories: 想要補強的類別
            max_results: 最多返回幾個結果

        Returns:
            推薦球員列表
        """
        if not self.league_players:
            return []

        # 對所有球員在目標類別進行排名
        rankings = []
        for stats in self.league_players:
            if stats.games_played == 0:
                continue

            z_scores = self.scorer.calculate_player_value(stats)

            # 計算在目標類別的總分
            target_score = sum(z_scores.get(cat, 0) for cat in target_categories)

            rankings.append({
                'player_name': stats.player_name,
                'team': stats.team,
                'target_score': round(target_score, 2),
                'category_scores': {cat: round(z_scores.get(cat, 0), 2) for cat in target_categories}
            })

        # 按目標分數排序
        rankings.sort(key=lambda x: x['target_score'], reverse=True)

        return rankings[:max_results]
