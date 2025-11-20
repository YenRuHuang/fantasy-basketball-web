"""
同步個人球隊數據到 Google Sheets
Team ID 8 - 默斯佛陀
包含：我的陣容、球員數據、本週對戰、我的賽程、深度分析、交易建議
"""

import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from collections import defaultdict

print("=" * 80)
print("  個人球隊數據同步 - 默斯佛陀")
print("=" * 80)
print()

# 載入配置
with open('config/my_team_config.json', 'r', encoding='utf-8') as f:
    my_config = json.load(f)

# 載入聯盟數據
with open('data/full_league_data.json', 'r', encoding='utf-8') as f:
    league_data = json.load(f)

my_team_id = str(my_config['team_id'])
my_team_name = my_config['team_name']

print(f"球隊: {my_team_name}")
print(f"Team ID: {my_team_id}")
print()

# 連接 Google Sheets
print("步驟 1: 連接 Google Sheets...")

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    my_config['service_account_file'],
    scopes=SCOPES
)

gc = gspread.authorize(credentials)
spreadsheet = gc.open_by_key(my_config['spreadsheet_id'])

print(f"連接成功: {spreadsheet.title}")
print()

# 取得我的陣容
teams = league_data['teams']
rosters = league_data['rosters']
team_schedules = league_data['team_schedules']
matchups_by_week = league_data['matchups_by_week']
current_week = league_data['current_week']
total_weeks = league_data['total_weeks']

my_roster = rosters.get(my_team_id, [])
my_schedule = team_schedules.get(my_team_id, {})

# 找到我的球隊資訊
my_team_info = None
for team in teams:
    if str(team['team_id']) == my_team_id:
        my_team_info = team
        break

if not my_team_info:
    print(f"錯誤: 找不到 Team ID {my_team_id}")
    exit(1)

# ============================================================================
# 工作表 1: 我的陣容
# ============================================================================
print("步驟 2: 建立「我的陣容」工作表...")

sheet_name = my_config['sheets']['roster']
try:
    roster_sheet = spreadsheet.worksheet(sheet_name)
except gspread.WorksheetNotFound:
    roster_sheet = spreadsheet.add_worksheet(title=sheet_name, rows=50, cols=8)

headers = ["#", "球員名稱", "NBA球隊", "位置", "狀態", "位置數", "評價"]

rows = [
    ["", "", "", "", "", "", ""],
    [f"{my_team_name} - 陣容總覽", "", "", "", "", "", ""],
    [f"更新時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""],
    headers
]

for i, player in enumerate(my_roster, 1):
    positions = player.get('positions', [])
    positions_str = ','.join(positions)
    num_positions = len(positions)
    status = player.get('status', '')
    status_display = status if status else "健康"

    # 簡單評價
    if num_positions >= 3:
        rating = "多位置優勢"
    elif 'C' in positions:
        rating = "稀缺位置"
    elif num_positions == 2:
        rating = "雙位置"
    else:
        rating = "單一位置"

    rows.append([
        i,
        player['name'],
        player.get('team', ''),
        positions_str,
        status_display,
        num_positions,
        rating
    ])

roster_sheet.clear()
roster_sheet.update(values=rows, range_name='A1')

# 格式化
roster_sheet.format('A2:G2', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 14},
    "horizontalAlignment": "CENTER"
})

roster_sheet.format('A5:G5', {
    "backgroundColor": {"red": 0.7, "green": 0.7, "blue": 0.7},
    "textFormat": {"bold": True},
    "horizontalAlignment": "CENTER"
})

print(f"「{sheet_name}」完成 ({len(my_roster)} 名球員)")
print()

# ============================================================================
# 工作表 2: 球員數據
# ============================================================================
print("步驟 3: 建立「球員數據」工作表...")

sheet_name = my_config['sheets']['stats']
try:
    stats_sheet = spreadsheet.worksheet(sheet_name)
except gspread.WorksheetNotFound:
    stats_sheet = spreadsheet.add_worksheet(title=sheet_name, rows=50, cols=10)

# 統計位置分佈
pos_counts = defaultdict(int)
for player in my_roster:
    for pos in player.get('positions', []):
        if pos in ['PG', 'SG', 'SF', 'PF', 'C']:
            pos_counts[pos] += 1

# 統計健康狀態
health_counts = {'健康': 0, '受傷': 0, '觀察': 0}
for player in my_roster:
    status = player.get('status', '')
    if status in ['O', 'INJ', 'OUT']:
        health_counts['受傷'] += 1
    elif status in ['GTD', 'DTD']:
        health_counts['觀察'] += 1
    else:
        health_counts['健康'] += 1

# 統計多位置球員
multi_pos = sum(1 for p in my_roster if len(p.get('positions', [])) >= 3)

rows = [
    ["", "", "", ""],
    [f"{my_team_name} - 球員數據統計", "", "", ""],
    ["", "", "", ""],
    ["統計項目", "數值", "備註", ""],
    ["", "", "", ""],
    ["球員總數", len(my_roster), "", ""],
    ["多位置球員 (3+)", multi_pos, f"{multi_pos/len(my_roster)*100:.1f}%", ""],
    ["", "", "", ""],
    ["位置分佈", "", "", ""],
    ["PG", pos_counts['PG'], "", ""],
    ["SG", pos_counts['SG'], "", ""],
    ["SF", pos_counts['SF'], "", ""],
    ["PF", pos_counts['PF'], "", ""],
    ["C", pos_counts['C'], "", ""],
    ["", "", "", ""],
    ["健康狀態", "", "", ""],
    ["健康", health_counts['健康'], f"{health_counts['健康']/len(my_roster)*100:.1f}%", ""],
    ["觀察中", health_counts['觀察'], f"{health_counts['觀察']/len(my_roster)*100:.1f}%", ""],
    ["受傷", health_counts['受傷'], f"{health_counts['受傷']/len(my_roster)*100:.1f}%", ""],
]

stats_sheet.clear()
stats_sheet.update(values=rows, range_name='A1')

# 格式化
stats_sheet.format('A2:D2', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 14},
    "horizontalAlignment": "CENTER"
})

stats_sheet.format('A4:D4', {
    "backgroundColor": {"red": 0.7, "green": 0.7, "blue": 0.7},
    "textFormat": {"bold": True},
    "horizontalAlignment": "CENTER"
})

print(f"「{sheet_name}」完成")
print()

# ============================================================================
# 工作表 3: 本週對戰
# ============================================================================
print("步驟 4: 建立「本週對戰」工作表...")

sheet_name = my_config['sheets']['matchup']
try:
    matchup_sheet = spreadsheet.worksheet(sheet_name)
except gspread.WorksheetNotFound:
    matchup_sheet = spreadsheet.add_worksheet(title=sheet_name, rows=30, cols=8)

# 找出本週對手
current_matchup = my_schedule.get(str(current_week), {})
opponent_name = current_matchup.get('opponent_name', 'N/A')
opponent_id = str(current_matchup.get('opponent_id', ''))

# 取得對手資訊
opponent_roster = rosters.get(opponent_id, [])
opponent_info = None
for team in teams:
    if str(team['team_id']) == opponent_id:
        opponent_info = team
        break

rows = [
    ["", "", "", "", "", "", "", ""],
    [f"Week {current_week} 對戰", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["我的球隊", my_team_name, "", "對手球隊", opponent_name, "", "", ""],
    ["球員數", len(my_roster), "", "球員數", len(opponent_roster), "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["對手陣容", "", "", "", "", "", "", ""],
    ["#", "球員", "NBA球隊", "位置", "狀態", "", "", ""]
]

for i, player in enumerate(opponent_roster, 1):
    positions_str = ','.join(player.get('positions', []))
    status = player.get('status', '')
    status_display = status if status else "健康"

    rows.append([
        i,
        player['name'],
        player.get('team', ''),
        positions_str,
        status_display,
        "", "", ""
    ])

matchup_sheet.clear()
matchup_sheet.update(values=rows, range_name='A1')

# 格式化
matchup_sheet.format('A2:H2', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 14},
    "horizontalAlignment": "CENTER"
})

matchup_sheet.format('A8:H8', {
    "backgroundColor": {"red": 0.7, "green": 0.7, "blue": 0.7},
    "textFormat": {"bold": True},
    "horizontalAlignment": "CENTER"
})

print(f"「{sheet_name}」完成 (對手: {opponent_name})")
print()

# ============================================================================
# 工作表 4: 我的賽程
# ============================================================================
print("步驟 5: 建立「我的賽程」工作表...")

sheet_name = my_config['sheets']['schedule']
try:
    schedule_sheet = spreadsheet.worksheet(sheet_name)
except gspread.WorksheetNotFound:
    schedule_sheet = spreadsheet.add_worksheet(title=sheet_name, rows=30, cols=6)

headers = ["Week", "對手", "狀態", "備註"]

rows = [
    ["", "", "", ""],
    [f"{my_team_name} - 完整賽程", "", "", ""],
    ["", "", "", ""],
    headers
]

for week in range(1, total_weeks + 1):
    week_str = str(week)
    if week_str in my_schedule:
        opp_name = my_schedule[week_str]['opponent_name']

        if week < current_week:
            status = "已結束"
        elif week == current_week:
            status = "本週"
        else:
            status = "未來"

        rows.append([
            f"Week {week}",
            opp_name,
            status,
            ""
        ])

schedule_sheet.clear()
schedule_sheet.update(values=rows, range_name='A1')

# 格式化
schedule_sheet.format('A2:D2', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 14},
    "horizontalAlignment": "CENTER"
})

schedule_sheet.format('A4:D4', {
    "backgroundColor": {"red": 0.7, "green": 0.7, "blue": 0.7},
    "textFormat": {"bold": True},
    "horizontalAlignment": "CENTER"
})

print(f"「{sheet_name}」完成 ({len(my_schedule)} 週賽程)")
print()

# ============================================================================
# 工作表 5: 深度分析
# ============================================================================
print("步驟 6: 建立「深度分析」工作表...")

sheet_name = my_config['sheets']['analysis']
try:
    analysis_sheet = spreadsheet.worksheet(sheet_name)
except gspread.WorksheetNotFound:
    analysis_sheet = spreadsheet.add_worksheet(title=sheet_name, rows=40, cols=6)

# 分析位置優勢劣勢
pos_analysis = []
league_avg_pos = {'PG': 0, 'SG': 0, 'SF': 0, 'PF': 0, 'C': 0}

# 計算聯盟平均
total_teams = len(teams)
for team_id, roster in rosters.items():
    team_pos_counts = defaultdict(int)
    for player in roster:
        for pos in player.get('positions', []):
            if pos in league_avg_pos:
                team_pos_counts[pos] += 1
    for pos in league_avg_pos:
        league_avg_pos[pos] += team_pos_counts[pos]

for pos in league_avg_pos:
    league_avg_pos[pos] = league_avg_pos[pos] / total_teams

# 比較我的陣容
for pos in ['PG', 'SG', 'SF', 'PF', 'C']:
    my_count = pos_counts[pos]
    avg_count = league_avg_pos[pos]
    diff = my_count - avg_count

    if diff > 1:
        analysis = "優勢位置"
        emoji = "🟢"
    elif diff < -1:
        analysis = "劣勢位置"
        emoji = "🔴"
    else:
        analysis = "平均水平"
        emoji = "🟡"

    pos_analysis.append({
        'position': pos,
        'my_count': my_count,
        'avg_count': round(avg_count, 1),
        'diff': round(diff, 1),
        'analysis': analysis,
        'emoji': emoji
    })

rows = [
    ["", "", "", "", "", ""],
    [f"{my_team_name} - 深度分析", "", "", "", "", ""],
    ["", "", "", "", "", ""],
    ["位置深度分析", "", "", "", "", ""],
    ["位置", "我的數量", "聯盟平均", "差距", "分析", ""],
]

for pa in pos_analysis:
    rows.append([
        pa['position'],
        pa['my_count'],
        pa['avg_count'],
        pa['diff'],
        f"{pa['emoji']} {pa['analysis']}",
        ""
    ])

rows.extend([
    ["", "", "", "", "", ""],
    ["陣容診斷", "", "", "", "", ""],
    ["", "", "", "", "", ""]
])

# 生成診斷建議
weak_positions = [pa['position'] for pa in pos_analysis if pa['analysis'] == "劣勢位置"]
strong_positions = [pa['position'] for pa in pos_analysis if pa['analysis'] == "優勢位置"]

if weak_positions:
    rows.append(["弱點位置", ', '.join(weak_positions), "", "", "", ""])
    rows.append(["建議", f"優先補強 {', '.join(weak_positions)} 位置", "", "", "", ""])
else:
    rows.append(["弱點位置", "無明顯弱點", "", "", "", ""])

rows.append(["", "", "", "", "", ""])

if strong_positions:
    rows.append(["優勢位置", ', '.join(strong_positions), "", "", "", ""])
    rows.append(["建議", f"可考慮交易 {', '.join(strong_positions)} 球員換取弱點位置", "", "", "", ""])

rows.append(["", "", "", "", "", ""])
rows.append(["多位置球員數", multi_pos, f"佔比 {multi_pos/len(my_roster)*100:.1f}%", "", "", ""])

if multi_pos / len(my_roster) < 0.3:
    rows.append(["建議", "多位置球員較少，建議增加陣容靈活性", "", "", "", ""])
else:
    rows.append(["評價", "多位置球員充足，陣容靈活", "", "", "", ""])

analysis_sheet.clear()
analysis_sheet.update(values=rows, range_name='A1')

# 格式化
analysis_sheet.format('A2:F2', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 14},
    "horizontalAlignment": "CENTER"
})

print(f"「{sheet_name}」完成")
print()

# ============================================================================
# 工作表 6: 交易建議
# ============================================================================
print("步驟 7: 建立「交易建議」工作表...")

sheet_name = my_config['sheets']['trades']
try:
    trades_sheet = spreadsheet.worksheet(sheet_name)
except gspread.WorksheetNotFound:
    trades_sheet = spreadsheet.add_worksheet(title=sheet_name, rows=50, cols=8)

rows = [
    ["", "", "", "", "", "", "", ""],
    [f"{my_team_name} - 交易建議", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["基於陣容分析的交易建議", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""]
]

if weak_positions:
    rows.extend([
        ["目標", f"尋找 {', '.join(weak_positions)} 位置球員", "", "", "", "", "", ""],
        ["策略", "從優勢位置交易換取弱點位置", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""]
    ])

# 可交易球員（來自優勢位置）
if strong_positions:
    rows.extend([
        ["可交易球員 (優勢位置)", "", "", "", "", "", "", ""],
        ["#", "球員", "位置", "位置數", "評價", "", "", ""]
    ])

    tradable = []
    for player in my_roster:
        positions = player.get('positions', [])
        # 如果球員的位置包含優勢位置
        if any(pos in strong_positions for pos in positions):
            tradable.append(player)

    for i, player in enumerate(tradable, 1):
        positions_str = ','.join(player.get('positions', []))
        num_pos = len(player.get('positions', []))

        if num_pos >= 3:
            value = "高價值 (多位置)"
        elif 'C' in player.get('positions', []):
            value = "高價值 (稀缺)"
        else:
            value = "中等價值"

        rows.append([
            i,
            player['name'],
            positions_str,
            num_pos,
            value,
            "", "", ""
        ])

rows.extend([
    ["", "", "", "", "", "", "", ""],
    ["交易原則", "", "", "", "", "", "", ""],
    ["1", "優先補強弱點位置", "", "", "", "", "", ""],
    ["2", "尋找多位置球員增加靈活性", "", "", "", "", "", ""],
    ["3", "注意球員健康狀態", "", "", "", "", "", ""],
    ["4", "考慮對手賽程難度", "", "", "", "", "", ""],
])

trades_sheet.clear()
trades_sheet.update(values=rows, range_name='A1')

# 格式化
trades_sheet.format('A2:H2', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 14},
    "horizontalAlignment": "CENTER"
})

print(f"「{sheet_name}」完成")
print()

# ============================================================================
# 完成
# ============================================================================
print("=" * 80)
print("  個人球隊同步完成！")
print("=" * 80)
print()
print(f"Google Sheets: {spreadsheet.url}")
print()
print("已同步工作表:")
print(f"  • {my_config['sheets']['roster']} - {len(my_roster)} 名球員")
print(f"  • {my_config['sheets']['stats']} - 數據統計")
print(f"  • {my_config['sheets']['matchup']} - Week {current_week} vs {opponent_name}")
print(f"  • {my_config['sheets']['schedule']} - {len(my_schedule)} 週賽程")
print(f"  • {my_config['sheets']['analysis']} - 陣容深度分析")
print(f"  • {my_config['sheets']['trades']} - 交易建議")
print()
print("提示:")
print("  - 深度分析會自動比對聯盟平均，找出優劣勢")
print("  - 交易建議基於位置深度自動生成")
print("  - 定期執行可追蹤陣容變化")
print()
