"""
同步聯盟數據到 Google Sheets - 給所有成員使用
就像你朋友的聯盟那樣！
"""

import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

print("=" * 80)
print(" 大亂鬥聯盟 → Google Sheets 同步（聯盟共享版）")
print("=" * 80)
print()
print(f"同步時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 載入配置
with open('config/google_sheets_config.json', 'r', encoding='utf-8') as f:
    sheets_config = json.load(f)

# 載入聯盟數據
with open('data/league_data.json', 'r', encoding='utf-8') as f:
    league_data = json.load(f)

print("步驟 1: 連接 Google Sheets...")

# 連接 Google Sheets
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    sheets_config['service_account_file'],
    scopes=SCOPES
)

gc = gspread.authorize(credentials)
spreadsheet = gc.open_by_key(sheets_config['spreadsheet_id'])

print(f"✅ 連接成功: {spreadsheet.title}")
print()

# ============================================================================
# 工作表 1: 聯盟排名
# ============================================================================
print("步驟 2: 同步聯盟排名...")

try:
    standings_sheet = spreadsheet.worksheet("聯盟排名")
except gspread.WorksheetNotFound:
    standings_sheet = spreadsheet.add_worksheet(title="聯盟排名", rows=20, cols=10)

# 準備排名數據
standings_headers = ["排名", "隊伍名稱", "經理", "勝", "敗", "和", "勝率", "備註"]
standings_rows = [standings_headers]

teams = league_data['teams']
for i, team in enumerate(teams, 1):
    wins = team.get('wins', 0)
    losses = team.get('losses', 0)
    ties = team.get('ties', 0)

    # 計算勝率
    total_games = wins + losses + ties
    win_rate = f"{wins / total_games:.3f}" if total_games > 0 else "0.000"

    # 你的隊伍標記
    remark = "👑 盟主" if team['team_id'] == 1 else ""

    standings_rows.append([
        i,
        team['team_name'],
        team.get('manager', 'Unknown'),
        wins,
        losses,
        ties,
        win_rate,
        remark
    ])

# 寫入排名數據
standings_sheet.clear()
standings_sheet.update('A1', standings_rows)

# 格式化
standings_sheet.format('A1:H1', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
    "horizontalAlignment": "CENTER"
})

# 標記盟主那一行
standings_sheet.format('A2:H2', {
    "backgroundColor": {"red": 1, "green": 0.95, "blue": 0.8},
    "textFormat": {"bold": True}
})

print(f"✅ 聯盟排名已同步 ({len(teams)} 支隊伍)")
print()

# ============================================================================
# 工作表 2: 本週對戰
# ============================================================================
print("步驟 3: 同步本週對戰...")

try:
    matchup_sheet = spreadsheet.worksheet("本週對戰")
except gspread.WorksheetNotFound:
    matchup_sheet = spreadsheet.add_worksheet(title="本週對戰", rows=15, cols=8)

# 準備對戰數據
current_week = league_data['current_week']
matchups = league_data['matchups']

matchup_headers = ["#", "主隊", "客隊", "預測", "備註"]
matchup_rows = [
    ["", "", "", "", ""],
    [f"Week {current_week} 對戰表", "", "", "", ""],
    ["", "", "", "", ""],
    matchup_headers
]

for i, matchup in enumerate(matchups, 1):
    team1_name = matchup['team1_name']
    team2_name = matchup['team2_name']

    # 標記你的對戰
    remark = ""
    prediction = "待分析"

    if matchup['team1_id'] == 1 or matchup['team2_id'] == 1:
        remark = "你的對戰"

    matchup_rows.append([
        i,
        team1_name,
        "vs",
        team2_name,
        remark
    ])

# 寫入對戰數據
matchup_sheet.clear()
matchup_sheet.update('A1', matchup_rows)

# 格式化標題
matchup_sheet.format('A2:E2', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 14},
    "horizontalAlignment": "CENTER"
})

matchup_sheet.format('A4:E4', {
    "backgroundColor": {"red": 0.8, "green": 0.8, "blue": 0.8},
    "textFormat": {"bold": True},
    "horizontalAlignment": "CENTER"
})

print(f"✅ 本週對戰已同步 ({len(matchups)} 場)")
print()

# ============================================================================
# 工作表 3: 聯盟資訊
# ============================================================================
print("步驟 4: 同步聯盟資訊...")

try:
    info_sheet = spreadsheet.worksheet("聯盟資訊")
except gspread.WorksheetNotFound:
    info_sheet = spreadsheet.add_worksheet(title="聯盟資訊", rows=20, cols=5)

# 準備聯盟資訊
info_data = [
    ["項目", "內容", ""],
    ["", "", ""],
    ["聯盟名稱", league_data['league_name'], ""],
    ["聯盟 ID", league_data['league_id'], ""],
    ["賽季", league_data['season'], ""],
    ["隊伍數", league_data['num_teams'], ""],
    ["當前週次", f"Week {league_data['current_week']}", ""],
    ["", "", ""],
    ["類別", "H2H 9-CAT", ""],
    ["", "", ""],
    ["統計類別", "", ""],
    ["", "• FG%", ""],
    ["", "• FT%", ""],
    ["", "• 3PM", ""],
    ["", "• PTS", ""],
    ["", "• REB", ""],
    ["", "• AST", ""],
    ["", "• ST", ""],
    ["", "• BLK", ""],
    ["", "• TO", ""],
    ["", "", ""],
    ["最後更新", league_data['last_updated'], ""],
    ["", "", ""],
    ["盟主", "默絲佛陀攝影掃地伯", "👑"],
]

# 寫入聯盟資訊
info_sheet.clear()
info_sheet.update('A1', info_data)

# 格式化
info_sheet.format('A1:C1', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
    "horizontalAlignment": "CENTER"
})

info_sheet.format('A3:A3', {"textFormat": {"bold": True, "fontSize": 12}})
info_sheet.format('A11:A11', {"textFormat": {"bold": True, "fontSize": 12}})

print("✅ 聯盟資訊已同步")
print()

# ============================================================================
# 工作表 4: 賽程表（簡化版）
# ============================================================================
print("步驟 5: 建立賽程表...")

try:
    schedule_sheet = spreadsheet.worksheet("賽程表")
except gspread.WorksheetNotFound:
    schedule_sheet = spreadsheet.add_worksheet(title="賽程表", rows=25, cols=15)

# 建立週次表頭
schedule_headers = ["隊伍名稱"] + [f"W{w}" for w in range(1, 11)]  # Week 1-10
schedule_rows = [schedule_headers]

# 每支隊伍的賽程（目前只有 Week 1 的數據）
for team in teams:
    row = [team['team_name']]

    # Week 1 對戰對手
    opponent = ""
    for matchup in matchups:
        if matchup['team1_id'] == team['team_id']:
            opponent = matchup['team2_name'][:10]  # 縮短名稱
            break
        elif matchup['team2_id'] == team['team_id']:
            opponent = matchup['team1_name'][:10]
            break

    # Week 1 有對手，其他週次待更新
    row.append(opponent if opponent else "TBD")
    for w in range(2, 11):
        row.append("TBD")

    schedule_rows.append(row)

# 寫入賽程表
schedule_sheet.clear()
schedule_sheet.update('A1', schedule_rows)

# 格式化
schedule_sheet.format('A1:K1', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
    "horizontalAlignment": "CENTER"
})

print("✅ 賽程表已建立")
print()

# ============================================================================
# 完成
# ============================================================================
print("=" * 80)
print(" 同步完成！")
print("=" * 80)
print()
print(f"📊 Google Sheets: {spreadsheet.url}")
print()
print("已同步工作表:")
print(f"  • 聯盟排名 - {len(teams)} 支隊伍")
print(f"  • 本週對戰 - Week {current_week} ({len(matchups)} 場)")
print(f"  • 聯盟資訊 - 基本資訊")
print(f"  • 賽程表 - 對戰時程")
print()
print("💡 下一步:")
print("  1. 點擊「共用」按鈕")
print("  2. 加入聯盟成員的 Email")
print("  3. 權限設為「檢視者」")
print("  4. 發送連結給大家！")
print()
