"""
陣容資料模型
"""

from dataclasses import dataclass
from typing import List
from .player import Player
from .stats import PlayerStats, CategoryStats, calculate_category_totals


@dataclass
class Roster:
    """Fantasy Basketball 陣容"""

    team_name: str
    players: List[Player]

    def get_active_players(self) -> List[Player]:
        """獲取可上場的球員 (排除 INJ)"""
        return [p for p in self.players if p.is_available()]

    def get_injured_players(self) -> List[Player]:
        """獲取受傷球員"""
        return [p for p in self.players if not p.is_available()]

    def get_category_totals(self, include_injured: bool = False) -> CategoryStats:
        """
        計算陣容的類別總計

        Args:
            include_injured: 是否包含受傷球員

        Returns:
            CategoryStats: 類別總計
        """
        if include_injured:
            players_to_count = self.players
        else:
            players_to_count = self.get_active_players()

        # 篩選有統計數據的球員
        player_stats = [p.stats for p in players_to_count if p.stats is not None]

        if not player_stats:
            return CategoryStats()

        return calculate_category_totals(player_stats)

    def get_roster_summary(self) -> dict:
        """獲取陣容摘要"""
        active = self.get_active_players()
        injured = self.get_injured_players()
        category_stats = self.get_category_totals(include_injured=False)

        return {
            'team_name': self.team_name,
            'total_players': len(self.players),
            'active_players': len(active),
            'injured_players': len(injured),
            'category_totals': category_stats.to_dict(),
            'players': [
                {
                    'name': p.name,
                    'team': p.team,
                    'positions': ', '.join(p.positions),
                    'status': p.injury_status or 'Healthy',
                    'stats': p.stats.to_dict() if p.stats else None
                }
                for p in self.players
            ]
        }
