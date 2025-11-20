"""
陣容分析器 - 評估陣容在 9-Cat 的優劣勢
"""

from typing import List, Dict
from ..models.roster import Roster
from ..models.stats import PlayerStats
from .category_scorer import CategoryScorer


class RosterAnalyzer:
    """陣容分析器"""

    def __init__(self, roster: Roster, league_players: List[PlayerStats] = None):
        """
        初始化陣容分析器

        Args:
            roster: 你的陣容
            league_players: 聯盟所有球員數據 (用於計算 Z-Score)
        """
        self.roster = roster
        self.league_players = league_players
        self.scorer = CategoryScorer()

        if league_players:
            self.scorer.calculate_league_averages(league_players)

    def get_category_strengths(self) -> Dict[str, Dict]:
        """
        分析陣容在各類別的強弱勢

        Returns:
            各類別的分析結果
        """
        active_players = self.roster.get_active_players()
        player_stats = [p.stats for p in active_players if p.stats]

        if not player_stats:
            return {}

        category_totals = self.roster.get_category_totals(include_injured=False)

        # 計算陣容整體的 Z-Score (如果有聯盟數據)
        category_analysis = {}

        for cat in CategoryScorer.CATEGORIES:
            if cat == 'FG%':
                value = category_totals.fg_pct
            elif cat == 'FT%':
                value = category_totals.ft_pct
            elif cat == '3PM':
                value = category_totals.three_pm
            elif cat == 'PTS':
                value = category_totals.pts
            elif cat == 'REB':
                value = category_totals.reb
            elif cat == 'AST':
                value = category_totals.ast
            elif cat == 'ST':
                value = category_totals.st
            elif cat == 'BLK':
                value = category_totals.blk
            elif cat == 'TO':
                value = category_totals.to
            else:
                value = 0

            category_analysis[cat] = {
                'value': value,
                'z_score': self.scorer.calculate_z_score(value, cat) if self.league_players else None
            }

        return category_analysis

    def identify_punt_categories(self, threshold: float = -0.5) -> List[str]:
        """
        識別應該放棄的類別 (Punt策略)

        Args:
            threshold: Z-Score 門檻值，低於此值的類別建議放棄

        Returns:
            建議放棄的類別列表
        """
        strengths = self.get_category_strengths()
        punt_categories = []

        for cat, data in strengths.items():
            z_score = data.get('z_score')
            if z_score is not None and z_score < threshold:
                punt_categories.append(cat)

        return punt_categories

    def identify_strong_categories(self, threshold: float = 0.5) -> List[str]:
        """
        識別優勢類別

        Args:
            threshold: Z-Score 門檻值，高於此值的類別為優勢

        Returns:
            優勢類別列表
        """
        strengths = self.get_category_strengths()
        strong_categories = []

        for cat, data in strengths.items():
            z_score = data.get('z_score')
            if z_score is not None and z_score > threshold:
                strong_categories.append(cat)

        return strong_categories

    def get_roster_report(self) -> Dict:
        """
        生成完整的陣容分析報告

        Returns:
            分析報告字典
        """
        active = self.roster.get_active_players()
        injured = self.roster.get_injured_players()
        category_totals = self.roster.get_category_totals(include_injured=False)
        strengths = self.get_category_strengths()

        strong_cats = self.identify_strong_categories()
        punt_cats = self.identify_punt_categories()

        return {
            'team_name': self.roster.team_name,
            'roster_size': {
                'total': len(self.roster.players),
                'active': len(active),
                'injured': len(injured)
            },
            'category_totals': category_totals.to_dict(),
            'category_analysis': {
                cat: {
                    'value': data['value'],
                    'z_score': round(data['z_score'], 2) if data['z_score'] else 'N/A',
                    'strength': 'Strong' if cat in strong_cats else 'Punt' if cat in punt_cats else 'Average'
                }
                for cat, data in strengths.items()
            },
            'strategic_summary': {
                'strong_categories': strong_cats,
                'punt_categories': punt_cats,
                'winning_potential': f"{len(strong_cats)}/9 類別"
            },
            'players': [
                {
                    'name': p.name,
                    'team': p.team,
                    'status': p.injury_status or 'Healthy'
                }
                for p in self.roster.players
            ]
        }

    def suggest_improvements(self) -> List[Dict]:
        """
        建議改善方向

        Returns:
            改善建議列表
        """
        suggestions = []
        punt_cats = self.identify_punt_categories()
        strong_cats = self.identify_strong_categories()

        # 如果優勢類別太少
        if len(strong_cats) < 5:
            suggestions.append({
                'priority': 'High',
                'issue': f'優勢類別只有 {len(strong_cats)} 個，需要至少 5 個才能穩定贏球',
                'recommendation': '透過交易補強弱勢類別，或徹底放棄某些類別專注於其他'
            })

        # 如果有太多劣勢類別
        if len(punt_cats) > 4:
            suggestions.append({
                'priority': 'High',
                'issue': f'劣勢類別有 {len(punt_cats)} 個，太多了',
                'recommendation': '建議明確選擇 Punt 策略：選擇 2-3 個類別完全放棄，用換來的資源補強其他類別'
            })

        # 針對特定類別的建議
        strengths = self.get_category_strengths()

        if strengths.get('FG%', {}).get('z_score', 0) < -1.0:
            suggestions.append({
                'priority': 'Medium',
                'issue': 'FG% 嚴重偏低',
                'recommendation': '交易掉低命中率後衛，換取高效率大前鋒/中鋒 (例如: .55+ FG% 的球員)'
            })

        if strengths.get('REB', {}).get('z_score', 0) < -1.0:
            suggestions.append({
                'priority': 'Medium',
                'issue': '籃板嚴重不足',
                'recommendation': '需要補強籃板大個子 (例如: 10+ RPG 的中鋒或大前鋒)'
            })

        return suggestions
