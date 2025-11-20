"""
同步聯盟洞察到 Google Sheets
建立 4 個工作表：賽程分析、位置深度、交易價值、每週戰報
"""

import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

print("=" * 80)
print("  同步聯盟洞察 → Google Sheets")
print("=" * 80)
print()

# 載入配置
with open('config/league_sheets_config.json', 'r', encoding='utf-8') as f:
    sheets_config = json.load(f)

# 載入洞察數據
try:
    with open('data/league_insights.json', 'r', encoding='utf-8') as f:
        insights_data = json.load(f)
except FileNotFoundError:
    print("錯誤: 找不到 data/league_insights.json")
    print("請先執行: python3 generate_league_insights.py")
    exit(1)

print(f"數據生成時間: {insights_data['generated_at']}")
print(f"當前週次: Week {insights_data['current_week']}")
print()

# 連接 Google Sheets
print("步驟 1: 連接 Google Sheets...")

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

print(f"連接成功: {spreadsheet.title}")
print()

insights = insights_data['insights']

# ============================================================================
# 工作表 1: 賽程分析
# ============================================================================
print("步驟 2: 建立「賽程分析」工作表...")

sheet_name = "賽程分析"
try:
    schedule_sheet = spreadsheet.worksheet(sheet_name)
except gspread.WorksheetNotFound:
    schedule_sheet = spreadsheet.add_worksheet(title=sheet_name, rows=30, cols=12)

schedule_data = insights['schedule_difficulty']

headers = [
    "排名", "難度", "隊伍", "當前勝率", "對手平均實力",
    "Week", "對手", "對手勝率",
    "Week", "對手", "對手勝率",
    "評語"
]

rows = [
    ["", "", "", "", "", "", "", "", "", "", "", ""],
    [f"未來賽程難度分析 (Week {insights_data['current_week']}-{insights_data['current_week']+3})", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", "", "", ""],
    headers
]

for i, team_sched in enumerate(schedule_data, 1):
    opponents = team_sched['future_opponents']

    row = [
        i,
        f"{team_sched['emoji']} {team_sched['difficulty_level']}",
        team_sched['team_name'],
        team_sched['current_win_rate'],
        team_sched['avg_opponent_strength'],
    ]

    # 前兩場對戰
    for j in range(2):
        if j < len(opponents):
            opp = opponents[j]
            row.extend([f"W{opp['week']}", opp['opponent'], opp['win_rate']])
        else:
            row.extend(["", "", ""])

    # 評語
    if team_sched['difficulty_level'] == "困難":
        comment = "賽程艱難，需做好準備"
    elif team_sched['difficulty_level'] == "容易":
        comment = "絕佳機會，把握勝場"
    else:
        comment = "中等難度，穩定發揮"

    row.append(comment)
    rows.append(row)

schedule_sheet.clear()
schedule_sheet.update(values=rows, range_name='A1')

# 格式化
schedule_sheet.format('A2:L2', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 14},
    "horizontalAlignment": "CENTER"
})

schedule_sheet.format('A4:L4', {
    "backgroundColor": {"red": 0.7, "green": 0.7, "blue": 0.7},
    "textFormat": {"bold": True},
    "horizontalAlignment": "CENTER"
})

print(f"「{sheet_name}」完成 ({len(schedule_data)} 支隊伍)")
print()

# ============================================================================
# 工作表 2: 位置深度
# ============================================================================
print("步驟 3: 建立「位置深度」工作表...")

sheet_name = "位置深度"
try:
    depth_sheet = spreadsheet.worksheet(sheet_name)
except gspread.WorksheetNotFound:
    depth_sheet = spreadsheet.add_worksheet(title=sheet_name, rows=30, cols=10)

depth_data = insights['position_depth']

headers = [
    "排名", "隊伍", "球員總數",
    "PG", "SG", "SF", "PF", "C",
    "最強位置", "最弱位置"
]

rows = [
    ["", "", "", "", "", "", "", "", "", ""],
    [f"各隊位置深度分析", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", ""],
    headers
]

# 依總球員數排序
depth_data_sorted = sorted(depth_data, key=lambda x: x['total_players'], reverse=True)

for i, team_depth in enumerate(depth_data_sorted, 1):
    pos = team_depth['positions']
    rows.append([
        i,
        team_depth['team_name'],
        team_depth['total_players'],
        pos['PG'],
        pos['SG'],
        pos['SF'],
        pos['PF'],
        pos['C'],
        team_depth['strongest_position'],
        team_depth['weakest_position']
    ])

depth_sheet.clear()
depth_sheet.update(values=rows, range_name='A1')

# 格式化
depth_sheet.format('A2:J2', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 14},
    "horizontalAlignment": "CENTER"
})

depth_sheet.format('A4:J4', {
    "backgroundColor": {"red": 0.7, "green": 0.7, "blue": 0.7},
    "textFormat": {"bold": True},
    "horizontalAlignment": "CENTER"
})

print(f"「{sheet_name}」完成 ({len(depth_data)} 支隊伍)")
print()

# ============================================================================
# 工作表 3: 交易價值
# ============================================================================
print("步驟 4: 建立「交易價值」工作表...")

sheet_name = "交易價值"
try:
    trade_sheet = spreadsheet.worksheet(sheet_name)
except gspread.WorksheetNotFound:
    trade_sheet = spreadsheet.add_worksheet(title=sheet_name, rows=300, cols=10)

trade_data = insights['trade_reference']

headers = [
    "排名", "球員", "Fantasy球隊", "位置數", "位置",
    "健康狀態", "多位置分", "健康調整", "交易價值"
]

rows = [
    ["", "", "", "", "", "", "", "", ""],
    [f"交易價值參考（簡化版）", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", ""],
    headers
]

# 只顯示前100名
for i, player in enumerate(trade_data[:100], 1):
    positions_str = ','.join(player['positions'])

    rows.append([
        i,
        player['player_name'],
        player['team_name'],
        player['num_positions'],
        positions_str,
        player['health_status'],
        player['versatility_score'],
        player['health_adjustment'],
        player['trade_value']
    ])

trade_sheet.clear()
trade_sheet.update(values=rows, range_name='A1')

# 格式化
trade_sheet.format('A2:I2', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 14},
    "horizontalAlignment": "CENTER"
})

trade_sheet.format('A4:I4', {
    "backgroundColor": {"red": 0.7, "green": 0.7, "blue": 0.7},
    "textFormat": {"bold": True},
    "horizontalAlignment": "CENTER"
})

print(f"「{sheet_name}」完成 (Top 100 球員)")
print()

# ============================================================================
# 工作表 4: 每週戰報
# ============================================================================
print("步驟 5: 建立「每週戰報」工作表...")

sheet_name = "每週戰報"
try:
    report_sheet = spreadsheet.worksheet(sheet_name)
except gspread.WorksheetNotFound:
    report_sheet = spreadsheet.add_worksheet(title=sheet_name, rows=30, cols=8)

weekly = insights['weekly_report']

rows = [
    ["", "", "", "", "", "", "", ""],
    [f"Week {weekly['current_week']} 戰報", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["本週對戰數", weekly['total_matchups'], "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["本週焦點對戰", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""]
]

if weekly['top_matchup']:
    top = weekly['top_matchup']
    rows.extend([
        ["類型", "強強對決", "", "", "", "", "", ""],
        ["隊伍 A", top['team1'], f"勝率: {top['team1_wr']}", "", "", "", "", ""],
        ["隊伍 B", top['team2'], f"勝率: {top['team2_wr']}", "", "", "", "", ""],
        ["評語", "本週最值得關注的對決！", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""]
    ])

if weekly['bottom_matchup']:
    bottom = weekly['bottom_matchup']
    rows.extend([
        ["", "", "", "", "", "", "", ""],
        ["弱弱對決", "", "", "", "", "", "", ""],
        ["隊伍 A", bottom['team1'], f"勝率: {bottom['team1_wr']}", "", "", "", "", ""],
        ["隊伍 B", bottom['team2'], f"勝率: {bottom['team2_wr']}", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""]
    ])

rows.extend([
    ["", "", "", "", "", "", "", ""],
    ["所有對戰", "", "", "", "", "", "", ""],
    ["#", "隊伍 A", "勝率", "隊伍 B", "勝率", "平均實力", "類型", ""]
])

for i, matchup in enumerate(weekly['all_matchups'], 1):
    rows.append([
        i,
        matchup['team1'],
        matchup['team1_wr'],
        matchup['team2'],
        matchup['team2_wr'],
        matchup['avg_strength'],
        matchup['matchup_type'],
        ""
    ])

report_sheet.clear()
report_sheet.update(values=rows, range_name='A1')

# 格式化
report_sheet.format('A2:H2', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 14},
    "horizontalAlignment": "CENTER"
})

print(f"「{sheet_name}」完成 (Week {weekly['current_week']})")
print()

# ============================================================================
# 完成
# ============================================================================
print("=" * 80)
print("  同步完成！")
print("=" * 80)
print()
print(f"Google Sheets: {spreadsheet.url}")
print()
print("已同步工作表:")
print("  • 賽程分析 - 未來賽程難度評估")
print("  • 位置深度 - 各隊位置分佈")
print("  • 交易價值 - 簡化版交易參考")
print(f"  • 每週戰報 - Week {weekly['current_week']} 對戰分析")
print()
print("提示:")
print("  - 賽程分析可幫助你找出輕鬆賽程的隊伍（交易目標）")
print("  - 位置深度可找出各隊的位置弱點")
print("  - 交易價值幫助你快速評估球員價值")
print("  - 每週戰報讓你了解本週重點對決")
print()
