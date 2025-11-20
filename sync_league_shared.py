"""
同步聯盟數據到共享 Google Sheets
- 不包含個人分析（保持私密）
- 包含下拉選單選擇球隊
- 移除主客隊概念
- 完整賽程（Week 1-19）
"""

import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

print("=" * 80)
print(" 大亂鬥聯盟 → 共享 Google Sheets 同步")
print("=" * 80)
print()
print(f"同步時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 載入配置
with open('config/league_sheets_config.json', 'r', encoding='utf-8') as f:
    sheets_config = json.load(f)

# 檢查是否已設定 Spreadsheet ID
if sheets_config['spreadsheet_id'] == "請建立新的 Google Sheets 並填入 ID":
    print("❌ 尚未設定 Spreadsheet ID")
    print()
    print("請先建立新的 Google Sheets:")
    print("1. 前往 https://sheets.google.com")
    print("2. 建立新試算表")
    print("3. 命名為:大亂鬥聯盟 - 數據中心")
    print("4. 分享給 Service Account (編輯者權限)")
    print("5. 複製 Spreadsheet ID 到 config/league_sheets_config.json")
    exit(1)

# 載入聯盟數據
with open('data/full_league_data.json', 'r', encoding='utf-8') as f:
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

teams = league_data['teams']
current_week = league_data['current_week']
total_weeks = league_data['total_weeks']

# ============================================================================
# 工作表 1: 聯盟排名
# ============================================================================
print("步驟 2: 同步聯盟排名...")

try:
    standings_sheet = spreadsheet.worksheet(sheets_config['sheets']['standings'])
except gspread.WorksheetNotFound:
    standings_sheet = spreadsheet.add_worksheet(title=sheets_config['sheets']['standings'], rows=20, cols=8)

standings_headers = ["排名", "隊伍名稱", "經理", "勝", "敗", "和", "勝率"]
standings_rows = [standings_headers]

for i, team in enumerate(teams, 1):
    wins = team.get('wins', 0)
    losses = team.get('losses', 0)
    ties = team.get('ties', 0)
    total_games = wins + losses + ties
    win_rate = f"{wins / total_games:.3f}" if total_games > 0 else "0.000"

    standings_rows.append([
        i,
        team['team_name'],
        team.get('manager', 'Unknown'),
        wins,
        losses,
        ties,
        win_rate
    ])

standings_sheet.clear()
standings_sheet.update(values=standings_rows, range_name='A1')

# 格式化
standings_sheet.format('A1:G1', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
    "horizontalAlignment": "CENTER"
})

print(f"✅ 聯盟排名已同步 ({len(teams)} 支隊伍)")
print()

# ============================================================================
# 工作表 2: 本週對戰（無主客隊）
# ============================================================================
print(f"步驟 3: 同步本週對戰 (Week {current_week})...")

try:
    matchup_sheet = spreadsheet.worksheet(sheets_config['sheets']['matchups'])
except gspread.WorksheetNotFound:
    matchup_sheet = spreadsheet.add_worksheet(title=sheets_config['sheets']['matchups'], rows=15, cols=5)

matchups = league_data['matchups_by_week'][f'week_{current_week}']

matchup_headers = ["#", "隊伍 A", "隊伍 B", "備註"]
matchup_rows = [
    ["", "", "", ""],
    [f"Week {current_week} 對戰表", "", "", ""],
    ["", "", "", ""],
    matchup_headers
]

for i, matchup in enumerate(matchups, 1):
    matchup_rows.append([
        i,
        matchup['team1_name'],
        matchup['team2_name'],
        ""
    ])

matchup_sheet.clear()
matchup_sheet.update(values=matchup_rows, range_name='A1')

# 格式化
matchup_sheet.format('A2:D2', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 14},
    "horizontalAlignment": "CENTER"
})

matchup_sheet.format('A4:D4', {
    "backgroundColor": {"red": 0.8, "green": 0.8, "blue": 0.8},
    "textFormat": {"bold": True},
    "horizontalAlignment": "CENTER"
})

print(f"✅ 本週對戰已同步 ({len(matchups)} 場)")
print()

# ============================================================================
# 工作表 3: 完整賽程（Week 1-19，無TBD）
# ============================================================================
print("步驟 4: 建立完整賽程表...")

try:
    schedule_sheet = spreadsheet.worksheet(sheets_config['sheets']['schedule'])
except gspread.WorksheetNotFound:
    schedule_sheet = spreadsheet.add_worksheet(title=sheets_config['sheets']['schedule'], rows=20, cols=25)

# 建立週次表頭（只顯示有對戰的週次）
active_weeks = []
for week in range(1, total_weeks + 1):
    week_key = f'week_{week}'
    if week_key in league_data['matchups_by_week'] and league_data['matchups_by_week'][week_key]:
        active_weeks.append(week)

schedule_headers = ["隊伍名稱"] + [f"W{w}" for w in active_weeks]
schedule_rows = [schedule_headers]

# 每支隊伍的賽程
team_schedules = league_data['team_schedules']

for team in teams:
    team_id = team['team_id']
    row = [team['team_name']]

    # 每週的對手
    for week in active_weeks:
        week_key = str(week)  # team_schedules 的 key 是字串
        if week_key in team_schedules.get(str(team_id), {}):
            opponent_name = team_schedules[str(team_id)][week_key]['opponent_name']
            # 縮短名稱以適應格子
            short_name = opponent_name[:12] if len(opponent_name) > 12 else opponent_name
            row.append(short_name)
        else:
            row.append("-")

    schedule_rows.append(row)

schedule_sheet.clear()
schedule_sheet.update(values=schedule_rows, range_name='A1')

# 格式化
num_weeks = len(active_weeks)
last_col = chr(65 + num_weeks)  # A + num_weeks
schedule_sheet.format(f'A1:{last_col}1', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
    "horizontalAlignment": "CENTER"
})

# 標記當前週次
current_week_col = chr(65 + active_weeks.index(current_week) + 1) if current_week in active_weeks else None
if current_week_col:
    schedule_sheet.format(f'{current_week_col}1:{current_week_col}1', {
        "backgroundColor": {"red": 1, "green": 0.65, "blue": 0},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "horizontalAlignment": "CENTER"
    })

print(f"✅ 完整賽程已建立 ({len(active_weeks)} 週)")
print()

# ============================================================================
# 工作表 4A: 球員數據源（隱藏工作表）
# ============================================================================
print("步驟 5a: 建立球員數據源...")

try:
    data_sheet = spreadsheet.worksheet("_球員數據源")
except gspread.WorksheetNotFound:
    data_sheet = spreadsheet.add_worksheet(title="_球員數據源", rows=500, cols=6)

# 建立所有球員的完整數據
rosters = league_data.get('rosters', {})
all_player_data = [["隊伍名稱", "球員名稱", "NBA隊伍", "位置", "狀態", "隊伍ID"]]

for team in teams:
    team_id = str(team['team_id'])
    team_name = team['team_name']
    team_roster = rosters.get(team_id, [])

    for player in team_roster:
        all_player_data.append([
            team_name,
            player['name'],
            player.get('team', ''),
            ','.join(player.get('positions', [])),
            player.get('status', ''),
            team_id
        ])

data_sheet.clear()
data_sheet.update(values=all_player_data, range_name='A1')

# 隱藏數據源工作表
try:
    requests = [{
        'updateSheetProperties': {
            'properties': {
                'sheetId': data_sheet.id,
                'hidden': True
            },
            'fields': 'hidden'
        }
    }]
    spreadsheet.batch_update({'requests': requests})
except:
    pass

print(f"✅ 球員數據源已建立 ({len(all_player_data)-1} 名球員)")

# ============================================================================
# 工作表 4B: 球員陣容（使用 FILTER 公式）
# ============================================================================
print("步驟 5b: 建立球員陣容工作表...")

try:
    roster_sheet = spreadsheet.worksheet(sheets_config['sheets']['roster'])
except gspread.WorksheetNotFound:
    roster_sheet = spreadsheet.add_worksheet(title=sheets_config['sheets']['roster'], rows=50, cols=8)

# 準備隊伍名稱列表
team_names = [team['team_name'] for team in teams]
default_team = teams[0]

# 建立帶公式的陣容頁面
roster_display = [
    ["選擇隊伍:", default_team['team_name'], "", "", "", "", ""],
    ["", "", "", "", "", "", ""],
    ["#", "球員名稱", "NBA隊伍", "位置", "狀態", "", ""],
]

# 使用 FILTER 公式動態顯示球員（從第4行開始）
# 公式會根據 B1 的值自動篩選 _球員數據源 的資料
filter_formula = f'=IF(ISBLANK(B1),"",FILTER(\'_球員數據源\'!B2:E,\'_球員數據源\'!A2:A=B1))'

roster_sheet.clear()
roster_sheet.update(range_name='A1', values=roster_display)

# 在 B4 插入 FILTER 公式 (使用 USER_ENTERED 以執行公式)
roster_sheet.update(range_name='B4', values=[[filter_formula]], value_input_option='USER_ENTERED')

# 設定數據驗證（下拉選單）- 使用 batch update
try:
    # 取得 sheet ID
    roster_sheet_id = roster_sheet.id

    # 建立下拉選單請求
    requests = [{
        'setDataValidation': {
            'range': {
                'sheetId': roster_sheet_id,
                'startRowIndex': 0,
                'endRowIndex': 1,
                'startColumnIndex': 1,
                'endColumnIndex': 2
            },
            'rule': {
                'condition': {
                    'type': 'ONE_OF_LIST',
                    'values': [{'userEnteredValue': name} for name in team_names]
                },
                'showCustomUi': True,
                'strict': True
            }
        }
    }]

    spreadsheet.batch_update({'requests': requests})
except Exception as e:
    print(f"⚠️  下拉選單設定失敗: {e}")

# 格式化
roster_sheet.format('A1:A1', {
    "textFormat": {"bold": True, "fontSize": 12}
})

roster_sheet.format('A3:G3', {
    "backgroundColor": {"red": 0.8, "green": 0.8, "blue": 0.8},
    "textFormat": {"bold": True},
    "horizontalAlignment": "CENTER"
})

print("✅ 球員陣容工作表已建立（含下拉選單）")
print()

# ============================================================================
# 工作表 5: 球隊統計（含下拉選單）
# ============================================================================
print("步驟 6: 建立球隊統計工作表...")

try:
    stats_sheet = spreadsheet.worksheet(sheets_config['sheets']['stats'])
except gspread.WorksheetNotFound:
    stats_sheet = spreadsheet.add_worksheet(title=sheets_config['sheets']['stats'], rows=20, cols=5)

# 建立球隊統計頁面（使用公式動態計算）
stats_display = [
    ["選擇隊伍:", default_team['team_name'], ""],
    ["", "", ""],
    ["統計項目", "數值", ""],
    ["球員數量", '=COUNTIF(\'_球員數據源\'!A:A,B1)', ""],
    ["經理", '=IFERROR(VLOOKUP(B1,\'聯盟排名\'!B:C,2,FALSE),"")', ""],
    ["戰績", '=IFERROR(VLOOKUP(B1,\'聯盟排名\'!B:D,2,FALSE)&"-"&VLOOKUP(B1,\'聯盟排名\'!B:E,2,FALSE)&"-"&VLOOKUP(B1,\'聯盟排名\'!B:F,2,FALSE),"")', ""],
    ["", "", ""],
    ["位置分佈", "", ""],
]

# 加入位置統計（使用 COUNTIFS 公式）
for pos in ['PG', 'SG', 'SF', 'PF', 'C']:
    stats_display.append([
        f"  {pos}",
        f'=COUNTIFS(\'_球員數據源\'!A:A,B1,\'_球員數據源\'!D:D,"*{pos}*")',
        ""
    ])

stats_sheet.clear()
stats_sheet.update(range_name='A1', values=stats_display, value_input_option='USER_ENTERED')

try:
    # 取得 sheet ID
    stats_sheet_id = stats_sheet.id

    # 建立下拉選單請求
    requests = [{
        'setDataValidation': {
            'range': {
                'sheetId': stats_sheet_id,
                'startRowIndex': 0,
                'endRowIndex': 1,
                'startColumnIndex': 1,
                'endColumnIndex': 2
            },
            'rule': {
                'condition': {
                    'type': 'ONE_OF_LIST',
                    'values': [{'userEnteredValue': name} for name in team_names]
                },
                'showCustomUi': True,
                'strict': True
            }
        }
    }]

    spreadsheet.batch_update({'requests': requests})
except Exception as e:
    print(f"⚠️  下拉選單設定失敗: {e}")

# 格式化
stats_sheet.format('A1:A1', {
    "textFormat": {"bold": True, "fontSize": 12}
})

stats_sheet.format('A3:C3', {
    "backgroundColor": {"red": 0.8, "green": 0.8, "blue": 0.8},
    "textFormat": {"bold": True},
    "horizontalAlignment": "CENTER"
})

print("✅ 球隊統計工作表已建立（含下拉選單）")
print()

# ============================================================================
# 工作表 6: 聯盟資訊
# ============================================================================
print("步驟 7: 同步聯盟資訊...")

try:
    info_sheet = spreadsheet.worksheet(sheets_config['sheets']['info'])
except gspread.WorksheetNotFound:
    info_sheet = spreadsheet.add_worksheet(title=sheets_config['sheets']['info'], rows=25, cols=5)

info_data = [
    ["項目", "內容", ""],
    ["", "", ""],
    ["聯盟名稱", league_data['league_name'], ""],
    ["聯盟 ID", league_data['league_id'], ""],
    ["賽季", league_data['season'], ""],
    ["隊伍數", league_data['num_teams'], ""],
    ["當前週次", f"Week {league_data['current_week']}", ""],
    ["總週數", f"{len(active_weeks)} 週", ""],
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
]

info_sheet.clear()
info_sheet.update(values=info_data, range_name='A1')

# 格式化
info_sheet.format('A1:C1', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
    "horizontalAlignment": "CENTER"
})

print("✅ 聯盟資訊已同步")
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
print(f"  • {sheets_config['sheets']['standings']} - {len(teams)} 支隊伍")
print(f"  • {sheets_config['sheets']['matchups']} - Week {current_week} ({len(matchups)} 場)")
print(f"  • {sheets_config['sheets']['schedule']} - 完整賽程 ({len(active_weeks)} 週)")
print(f"  • {sheets_config['sheets']['roster']} - 球員陣容（含下拉選單）")
print(f"  • {sheets_config['sheets']['stats']} - 球隊統計（含下拉選單）")
print(f"  • {sheets_config['sheets']['info']} - 聯盟資訊")
print()
print("💡 下一步:")
print("  1. 點擊「共用」按鈕")
print("  2. 選擇「知道連結的任何人都可以檢視」")
print("  3. 複製連結分享給聯盟成員！")
print()
print("⚠️  注意: 不包含「分析」工作表，你的策略保持私密！")
print()
