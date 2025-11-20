"""
球員資料模型
"""

from dataclasses import dataclass
from typing import Optional
from .stats import PlayerStats


@dataclass
class Player:
    """球員基本資料"""

    player_id: str
    name: str
    team: str
    positions: list[str]  # 可擔任的位置 (e.g., ['PG', 'SG'])
    injury_status: Optional[str] = None
    stats: Optional[PlayerStats] = None

    def __repr__(self) -> str:
        positions_str = ','.join(self.positions)
        status = f" ({self.injury_status})" if self.injury_status else ""
        return f"{self.name} ({self.team} - {positions_str}){status}"

    def is_healthy(self) -> bool:
        """檢查球員是否健康"""
        return self.injury_status in [None, 'GTD', '']

    def is_available(self) -> bool:
        """檢查球員是否可上場 (INJ 不考慮)"""
        return self.injury_status not in ['INJ', 'O', 'IR']
