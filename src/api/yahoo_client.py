"""
Yahoo Fantasy Basketball API 客戶端

使用 yfpy 套件連接 Yahoo Fantasy Sports API
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any

from yfpy.query import YahooFantasySportsQuery


class YahooFantasyClient:
    """Yahoo Fantasy Basketball API 客戶端"""

    def __init__(self, credentials_path: Optional[str] = None):
        """
        初始化 Yahoo Fantasy API 客戶端

        Args:
            credentials_path: 認證檔案路徑，預設為 config/credentials.json
        """
        if credentials_path is None:
            project_root = Path(__file__).parent.parent.parent
            credentials_path = project_root / "config" / "credentials.json"

        self.credentials_path = Path(credentials_path)
        self.credentials = self._load_credentials()

        # 初始化 Yahoo Fantasy Query 物件
        self.yahoo_query = self._init_yahoo_query()

    def _load_credentials(self) -> Dict:
        """載入認證資訊"""
        if not self.credentials_path.exists():
            raise FileNotFoundError(
                f"找不到認證檔案: {self.credentials_path}\n"
                f"請複製 credentials.example.json 並填入你的 Yahoo API 認證資訊"
            )

        with open(self.credentials_path, 'r') as f:
            return json.load(f)

    def _init_yahoo_query(self) -> YahooFantasySportsQuery:
        """初始化 Yahoo Fantasy Query 物件"""
        project_root = Path(__file__).parent.parent.parent

        yahoo_config = self.credentials.get('yahoo', {})
        league_config = self.credentials.get('league', {})

        # 建立 yfpy 查詢物件
        yahoo_query = YahooFantasySportsQuery(
            auth_dir=str(project_root / "config"),
            league_id=league_config.get('league_id'),
            game_code=league_config.get('game_code', 'nba'),
            consumer_key=yahoo_config.get('client_id'),
            consumer_secret=yahoo_config.get('client_secret')
        )

        return yahoo_query

    def get_league_info(self) -> Any:
        """
        獲取聯盟基本資訊

        Returns:
            聯盟資訊物件
        """
        return self.yahoo_query.get_league_info()

    def get_league_standings(self) -> Any:
        """
        獲取聯盟排名

        Returns:
            排名資訊
        """
        return self.yahoo_query.get_league_standings()

    def get_league_teams(self) -> List[Any]:
        """
        獲取聯盟所有隊伍

        Returns:
            隊伍列表
        """
        return self.yahoo_query.get_league_teams()

    def get_team_roster(self, team_id: Optional[str] = None) -> List[Any]:
        """
        獲取隊伍陣容

        Args:
            team_id: 隊伍 ID，若不指定則獲取當前用戶的隊伍

        Returns:
            球員列表
        """
        if team_id:
            return self.yahoo_query.get_team_roster_by_week(team_id)
        else:
            # 獲取當前用戶的隊伍
            return self.yahoo_query.get_current_user_roster()

    def get_player_stats(self, player_key: str, stat_type: str = 'season') -> Any:
        """
        獲取球員統計數據

        Args:
            player_key: 球員 key (格式: nba.p.XXXXX)
            stat_type: 統計類型 ('season', 'average', 'week')

        Returns:
            球員統計數據
        """
        return self.yahoo_query.get_player_stats_for_season(player_key)

    def get_all_players(self, status: str = 'A', position: Optional[str] = None) -> List[Any]:
        """
        獲取所有可用球員

        Args:
            status: 球員狀態 ('A' = All, 'FA' = Free Agent, 'W' = Waivers, 'T' = Taken)
            position: 位置篩選 (PG, SG, G, SF, PF, F, C, Util)

        Returns:
            球員列表
        """
        return self.yahoo_query.get_league_players(
            player_count=None,  # 獲取所有球員
            status=status,
            position=position
        )

    def get_free_agents(self, position: Optional[str] = None) -> List[Any]:
        """
        獲取自由球員

        Args:
            position: 位置篩選

        Returns:
            自由球員列表
        """
        return self.get_all_players(status='FA', position=position)

    def get_matchup(self, team_id: str, week: Optional[int] = None) -> Any:
        """
        獲取對戰資訊

        Args:
            team_id: 隊伍 ID
            week: 週次，若不指定則為當前週

        Returns:
            對戰資訊
        """
        if week:
            return self.yahoo_query.get_team_matchup(team_id, week)
        else:
            return self.yahoo_query.get_team_matchup(team_id)

    def get_league_scoreboard(self, week: Optional[int] = None) -> Any:
        """
        獲取聯盟計分板（所有對戰結果）

        Args:
            week: 週次

        Returns:
            計分板資訊
        """
        return self.yahoo_query.get_league_scoreboard_by_week(week)


if __name__ == "__main__":
    # 測試連接
    try:
        client = YahooFantasyClient()
        print("Yahoo Fantasy API 連接成功！")

        # 測試獲取聯盟資訊
        league_info = client.get_league_info()
        print(f"聯盟名稱: {league_info.name}")
        print(f"隊伍數量: {league_info.num_teams}")

    except Exception as e:
        print(f"連接失敗: {e}")
