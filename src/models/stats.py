"""
統計數據模型 - 針對 9-Cat Fantasy Basketball
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PlayerStats:
    """
    球員統計數據 (9-Cat)

    Categories:
    - FG%: Field Goal Percentage (投籃命中率)
    - FT%: Free Throw Percentage (罰球命中率)
    - 3PM: Three Pointers Made (三分球命中數)
    - PTS: Points (得分)
    - REB: Rebounds (籃板)
    - AST: Assists (助攻)
    - ST: Steals (抄截)
    - BLK: Blocks (火鍋)
    - TO: Turnovers (失誤) 或 A/T: Assist/Turnover Ratio
    """

    # 球員基本資訊
    player_id: str
    player_name: str
    team: str
    position: str

    # 比賽場次
    games_played: int

    # 投籃相關
    fgm: int = 0  # Field Goals Made
    fga: int = 0  # Field Goals Attempted
    fg_pct: float = 0.0  # Field Goal Percentage

    # 罰球相關
    ftm: int = 0  # Free Throws Made
    fta: int = 0  # Free Throws Attempted
    ft_pct: float = 0.0  # Free Throw Percentage

    # 三分球
    three_pm: int = 0  # Three Pointers Made

    # 統計數據
    pts: int = 0  # Points
    reb: int = 0  # Rebounds
    ast: int = 0  # Assists
    st: int = 0   # Steals
    blk: int = 0  # Blocks
    to: int = 0   # Turnovers

    # 雙十 (可選)
    dd: int = 0   # Double-Doubles

    # 傷病狀態
    injury_status: Optional[str] = None  # GTD, INJ, O, etc.

    def get_at_ratio(self) -> float:
        """計算 A/T ratio (助攻失誤比)"""
        if self.to == 0:
            return float('inf') if self.ast > 0 else 0.0
        return self.ast / self.to

    def to_dict(self) -> dict:
        """轉換為字典格式"""
        return {
            'player_id': self.player_id,
            'player_name': self.player_name,
            'team': self.team,
            'position': self.position,
            'games_played': self.games_played,
            'FG%': self.fg_pct,
            'FT%': self.ft_pct,
            '3PM': self.three_pm,
            'PTS': self.pts,
            'REB': self.reb,
            'AST': self.ast,
            'ST': self.st,
            'BLK': self.blk,
            'TO': self.to,
            'A/T': self.get_at_ratio(),
            'DD': self.dd,
            'injury': self.injury_status
        }


@dataclass
class CategoryStats:
    """
    類別統計 - 用於陣容整體分析
    """

    fg_pct: float = 0.0
    ft_pct: float = 0.0
    three_pm: int = 0
    pts: int = 0
    reb: int = 0
    ast: int = 0
    st: int = 0
    blk: int = 0
    to: int = 0
    dd: int = 0

    def get_at_ratio(self) -> float:
        """計算整體 A/T ratio"""
        if self.to == 0:
            return float('inf') if self.ast > 0 else 0.0
        return self.ast / self.to

    def to_dict(self) -> dict:
        """轉換為字典格式"""
        return {
            'FG%': round(self.fg_pct, 3),
            'FT%': round(self.ft_pct, 3),
            '3PM': self.three_pm,
            'PTS': self.pts,
            'REB': self.reb,
            'AST': self.ast,
            'ST': self.st,
            'BLK': self.blk,
            'TO': self.to,
            'A/T': round(self.get_at_ratio(), 2),
            'DD': self.dd
        }


def calculate_category_totals(player_stats_list: list[PlayerStats]) -> CategoryStats:
    """
    計算多個球員的類別總和

    Args:
        player_stats_list: 球員統計列表

    Returns:
        CategoryStats: 類別總計
    """
    total_fgm = sum(p.fgm for p in player_stats_list)
    total_fga = sum(p.fga for p in player_stats_list)
    total_ftm = sum(p.ftm for p in player_stats_list)
    total_fta = sum(p.fta for p in player_stats_list)

    fg_pct = total_fgm / total_fga if total_fga > 0 else 0.0
    ft_pct = total_ftm / total_fta if total_fta > 0 else 0.0

    return CategoryStats(
        fg_pct=fg_pct,
        ft_pct=ft_pct,
        three_pm=sum(p.three_pm for p in player_stats_list),
        pts=sum(p.pts for p in player_stats_list),
        reb=sum(p.reb for p in player_stats_list),
        ast=sum(p.ast for p in player_stats_list),
        st=sum(p.st for p in player_stats_list),
        blk=sum(p.blk for p in player_stats_list),
        to=sum(p.to for p in player_stats_list),
        dd=sum(p.dd for p in player_stats_list)
    )
