"""
9-Cat 類別評分系統

基於 Z-Score 的球員價值計算
"""

import numpy as np
import pandas as pd
from typing import List, Dict
from ..models.stats import PlayerStats, CategoryStats


class CategoryScorer:
    """
    9-Cat 類別評分器

    使用 Z-Score 方法計算球員在各類別的價值
    """

    # 9個統計類別
    CATEGORIES = ['FG%', 'FT%', '3PM', 'PTS', 'REB', 'AST', 'ST', 'BLK', 'TO']

    # 類別權重 (可自定義)
    DEFAULT_WEIGHTS = {
        'FG%': 1.0,
        'FT%': 1.0,
        '3PM': 1.0,
        'PTS': 1.0,
        'REB': 1.0,
        'AST': 1.0,
        'ST': 1.0,
        'BLK': 1.0,
        'TO': -1.0  # 失誤是負面影響
    }

    def __init__(self, weights: Dict[str, float] = None):
        """
        初始化評分器

        Args:
            weights: 類別權重，若不指定則使用預設權重
        """
        self.weights = weights or self.DEFAULT_WEIGHTS
        self.league_stats: Dict[str, Dict[str, float]] = {}  # 儲存聯盟平均和標準差

    def calculate_league_averages(self, players_stats: List[PlayerStats]) -> None:
        """
        計算聯盟平均值和標準差

        Args:
            players_stats: 所有球員的統計數據
        """
        if not players_stats:
            raise ValueError("球員數據不能為空")

        # 轉換為 DataFrame 以便計算
        data = []
        for stats in players_stats:
            if stats.games_played == 0:
                continue

            data.append({
                'FG%': stats.fg_pct,
                'FT%': stats.ft_pct,
                '3PM': stats.three_pm,
                'PTS': stats.pts,
                'REB': stats.reb,
                'AST': stats.ast,
                'ST': stats.st,
                'BLK': stats.blk,
                'TO': stats.to
            })

        df = pd.DataFrame(data)

        # 計算平均值和標準差
        self.league_stats = {
            cat: {
                'mean': df[cat].mean(),
                'std': df[cat].std()
            }
            for cat in self.CATEGORIES
        }

    def calculate_z_score(self, value: float, category: str) -> float:
        """
        計算單一類別的 Z-Score

        Z-Score = (value - mean) / std

        Args:
            value: 球員該類別的數值
            category: 類別名稱

        Returns:
            Z-Score 值
        """
        if category not in self.league_stats:
            raise ValueError(f"尚未計算聯盟平均值，請先執行 calculate_league_averages()")

        mean = self.league_stats[category]['mean']
        std = self.league_stats[category]['std']

        if std == 0:
            return 0.0

        z_score = (value - mean) / std

        # 失誤是負面，所以反轉
        if category == 'TO':
            z_score = -z_score

        return z_score

    def calculate_player_value(self, stats: PlayerStats) -> Dict[str, float]:
        """
        計算球員在各類別的 Z-Score 值

        Args:
            stats: 球員統計數據

        Returns:
            各類別的 Z-Score 字典
        """
        if not self.league_stats:
            raise ValueError("尚未計算聯盟平均值")

        player_values = {
            'FG%': self.calculate_z_score(stats.fg_pct, 'FG%'),
            'FT%': self.calculate_z_score(stats.ft_pct, 'FT%'),
            '3PM': self.calculate_z_score(stats.three_pm, '3PM'),
            'PTS': self.calculate_z_score(stats.pts, 'PTS'),
            'REB': self.calculate_z_score(stats.reb, 'REB'),
            'AST': self.calculate_z_score(stats.ast, 'AST'),
            'ST': self.calculate_z_score(stats.st, 'ST'),
            'BLK': self.calculate_z_score(stats.blk, 'BLK'),
            'TO': self.calculate_z_score(stats.to, 'TO')
        }

        return player_values

    def calculate_total_value(self, stats: PlayerStats) -> float:
        """
        計算球員的總價值 (所有類別的加權 Z-Score 總和)

        Args:
            stats: 球員統計數據

        Returns:
            總價值
        """
        z_scores = self.calculate_player_value(stats)
        total = sum(z_scores[cat] * self.weights.get(cat, 1.0) for cat in self.CATEGORIES)
        return total

    def rank_players(self, players_stats: List[PlayerStats]) -> List[Dict]:
        """
        對球員進行排名

        Args:
            players_stats: 球員統計數據列表

        Returns:
            排名列表 (包含球員名稱、總價值、各類別 Z-Score)
        """
        if not self.league_stats:
            self.calculate_league_averages(players_stats)

        rankings = []
        for stats in players_stats:
            if stats.games_played == 0:
                continue

            z_scores = self.calculate_player_value(stats)
            total_value = self.calculate_total_value(stats)

            rankings.append({
                'player_name': stats.player_name,
                'team': stats.team,
                'total_value': total_value,
                **z_scores
            })

        # 按總價值排序
        rankings.sort(key=lambda x: x['total_value'], reverse=True)

        # 加入排名
        for i, player in enumerate(rankings, 1):
            player['rank'] = i

        return rankings

    def compare_categories(self, stats1: PlayerStats, stats2: PlayerStats) -> Dict[str, Dict]:
        """
        比較兩個球員在各類別的差異

        Args:
            stats1: 球員 1 統計
            stats2: 球員 2 統計

        Returns:
            差異分析字典
        """
        z1 = self.calculate_player_value(stats1)
        z2 = self.calculate_player_value(stats2)

        comparison = {}
        for cat in self.CATEGORIES:
            diff = z1[cat] - z2[cat]
            comparison[cat] = {
                f'{stats1.player_name}_z': round(z1[cat], 2),
                f'{stats2.player_name}_z': round(z2[cat], 2),
                'difference': round(diff, 2),
                'advantage': stats1.player_name if diff > 0 else stats2.player_name
            }

        return comparison
