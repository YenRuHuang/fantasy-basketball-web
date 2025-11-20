"""
Google Sheets 自動同步系統

功能：
1. 自動上傳陣容數據到 Google Sheets
2. 同步聯盟排名和對戰結果
3. 更新 Z-Score 球員排名
4. 生成週報告
"""

import json
from typing import Dict, List, Any
from datetime import datetime

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False
    print("警告: gspread 未安裝，Google Sheets 功能不可用")
    print("執行: pip install gspread google-auth")


class GoogleSheetsSync:
    """Google Sheets 同步管理器"""

    # Google Sheets API 範圍
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    def __init__(self, credentials_file: str = None, spreadsheet_id: str = None):
        """
        初始化 Google Sheets 同步器

        Args:
            credentials_file: Google Service Account JSON 檔案路徑
            spreadsheet_id: Google Sheets ID
        """
        if not GSPREAD_AVAILABLE:
            raise ImportError("請先安裝: pip install gspread google-auth")

        self.credentials_file = credentials_file or "config/google_credentials.json"
        self.spreadsheet_id = spreadsheet_id
        self.client = None
        self.spreadsheet = None

    def authenticate(self):
        """
        Google Sheets 認證

        需要先建立 Google Service Account 並下載 JSON 金鑰
        """
        try:
            creds = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=self.SCOPES
            )
            self.client = gspread.authorize(creds)
            print("✅ Google Sheets 認證成功")
            return True
        except FileNotFoundError:
            print(f"❌ 找不到認證檔案: {self.credentials_file}")
            print("\n請按照以下步驟設定：")
            print("1. 前往 Google Cloud Console")
            print("2. 建立 Service Account")
            print("3. 下載 JSON 金鑰檔")
            print("4. 將檔案儲存為 config/google_credentials.json")
            return False
        except Exception as e:
            print(f"❌ 認證失敗: {e}")
            return False

    def connect_spreadsheet(self, spreadsheet_id: str = None):
        """連接到指定的 Google Sheets"""
        if not self.client:
            self.authenticate()

        spreadsheet_id = spreadsheet_id or self.spreadsheet_id

        try:
            self.spreadsheet = self.client.open_by_key(spreadsheet_id)
            print(f"✅ 已連接到: {self.spreadsheet.title}")
            return True
        except Exception as e:
            print(f"❌ 無法連接到 Spreadsheet: {e}")
            return False

    def update_roster_sheet(self, roster_data: Dict):
        """
        更新陣容分頁

        Args:
            roster_data: 陣容數據字典
        """
        if not self.spreadsheet:
            print("請先連接到 Spreadsheet")
            return False

        try:
            # 獲取或建立 "Roster" 分頁
            try:
                worksheet = self.spreadsheet.worksheet("Roster")
            except:
                worksheet = self.spreadsheet.add_worksheet(
                    title="Roster",
                    rows=100,
                    cols=20
                )

            # 準備表頭
            headers = [
                "位置", "球員名稱", "隊伍", "狀態",
                "FG%", "FT%", "3PM", "PTS", "REB", "AST", "ST", "BLK", "TO"
            ]

            # 準備數據
            data = [headers]

            for player in roster_data.get('players', []):
                stats = player.get('stats', {})
                row = [
                    player.get('positions', ''),
                    player.get('name', ''),
                    player.get('team', ''),
                    player.get('status', 'Healthy'),
                    stats.get('FG%', 0),
                    stats.get('FT%', 0),
                    stats.get('3PM', 0),
                    stats.get('PTS', 0),
                    stats.get('REB', 0),
                    stats.get('AST', 0),
                    stats.get('ST', 0),
                    stats.get('BLK', 0),
                    stats.get('TO', 0)
                ]
                data.append(row)

            # 更新資料
            worksheet.clear()
            worksheet.update('A1', data)

            # 格式化
            worksheet.format('A1:M1', {
                'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 0.9},
                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
            })

            print("✅ Roster 分頁已更新")
            return True

        except Exception as e:
            print(f"❌ 更新 Roster 失敗: {e}")
            return False

    def update_matchup_sheet(self, matchup_data: Dict):
        """
        更新對戰分頁

        Args:
            matchup_data: 對戰數據
        """
        if not self.spreadsheet:
            print("請先連接到 Spreadsheet")
            return False

        try:
            try:
                worksheet = self.spreadsheet.worksheet("Matchup")
            except:
                worksheet = self.spreadsheet.add_worksheet(
                    title="Matchup",
                    rows=50,
                    cols=15
                )

            # 表頭
            headers = [
                "週次", "對手", "FG%", "FT%", "3PM", "PTS",
                "REB", "AST", "ST", "BLK", "TO", "結果"
            ]

            data = [headers]

            # 對戰數據
            week = matchup_data.get('week', 1)
            opponent = matchup_data.get('opponent', '')
            my_stats = matchup_data.get('my_stats', {})
            opp_stats = matchup_data.get('opponent_stats', {})
            result = matchup_data.get('result', '')

            row = [
                f"Week {week}",
                opponent,
                f"{my_stats.get('FG%', 0):.3f} vs {opp_stats.get('FG%', 0):.3f}",
                f"{my_stats.get('FT%', 0):.3f} vs {opp_stats.get('FT%', 0):.3f}",
                f"{my_stats.get('3PM', 0)} vs {opp_stats.get('3PM', 0)}",
                f"{my_stats.get('PTS', 0)} vs {opp_stats.get('PTS', 0)}",
                f"{my_stats.get('REB', 0)} vs {opp_stats.get('REB', 0)}",
                f"{my_stats.get('AST', 0)} vs {opp_stats.get('AST', 0)}",
                f"{my_stats.get('ST', 0)} vs {opp_stats.get('ST', 0)}",
                f"{my_stats.get('BLK', 0)} vs {opp_stats.get('BLK', 0)}",
                f"{my_stats.get('TO', 0)} vs {opp_stats.get('TO', 0)}",
                result
            ]
            data.append(row)

            worksheet.clear()
            worksheet.update('A1', data)

            print("✅ Matchup 分頁已更新")
            return True

        except Exception as e:
            print(f"❌ 更新 Matchup 失敗: {e}")
            return False

    def update_analysis_sheet(self, analysis: Dict):
        """
        更新分析結果分頁

        Args:
            analysis: 陣容分析結果
        """
        if not self.spreadsheet:
            return False

        try:
            try:
                worksheet = self.spreadsheet.worksheet("Analysis")
            except:
                worksheet = self.spreadsheet.add_worksheet(
                    title="Analysis",
                    rows=30,
                    cols=10
                )

            # 建立報告
            data = [
                ["Fantasy Basketball 陣容分析報告"],
                ["生成時間", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                [""],
                ["優勢類別"],
            ]

            for cat in analysis.get('strong_categories', []):
                data.append([cat, "✅"])

            data.append([""])
            data.append(["劣勢類別"])

            for cat in analysis.get('punt_categories', []):
                data.append([cat, "❌"])

            data.append([""])
            data.append(["改善建議"])

            for suggestion in analysis.get('suggestions', []):
                data.append([suggestion.get('issue', ''), suggestion.get('recommendation', '')])

            worksheet.clear()
            worksheet.update('A1', data)

            print("✅ Analysis 分頁已更新")
            return True

        except Exception as e:
            print(f"❌ 更新 Analysis 失敗: {e}")
            return False

    def create_dashboard(self):
        """建立完整的儀表板"""
        print("正在建立 Fantasy Basketball 儀表板...")

        # 建立多個分頁
        sheets_to_create = [
            "Roster",       # 陣容
            "Matchup",      # 對戰
            "Analysis",     # 分析
            "Z-Score",      # 球員排名
            "Trade",        # 交易建議
            "Schedule"      # 賽程
        ]

        for sheet_name in sheets_to_create:
            try:
                self.spreadsheet.worksheet(sheet_name)
                print(f"  ✓ {sheet_name} 已存在")
            except:
                self.spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=20)
                print(f"  + 建立 {sheet_name}")

        print("✅ 儀表板建立完成")


# 使用範例
if __name__ == "__main__":
    print("=" * 70)
    print(" Google Sheets 同步設定")
    print("=" * 70)
    print()
    print("此功能需要 Google Service Account 認證")
    print()
    print("設定步驟:")
    print("1. 前往: https://console.cloud.google.com/")
    print("2. 建立新專案或選擇現有專案")
    print("3. 啟用 Google Sheets API 和 Google Drive API")
    print("4. 建立 Service Account")
    print("5. 下載 JSON 金鑰檔")
    print("6. 將檔案重命名為 google_credentials.json")
    print("7. 放到 config/ 目錄")
    print()
    print("完成後執行:")
    print("  python3 -m src.integrations.google_sheets_sync")
    print()
