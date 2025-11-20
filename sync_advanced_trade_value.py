"""
同步進階交易價值到 Google Sheets
建立「進階交易價值」工作表，顯示完整評分細節
"""

import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

print("=" * 80)
print("  同步進階交易價值 → Google Sheets")
print("=" * 80)
print()

# 載入配置
with open('config/league_sheets_config.json', 'r', encoding='utf-8') as f:
    sheets_config = json.load(f)

# 載入交易價值數據
try:
    with open('data/advanced_trade_value.json', 'r', encoding='utf-8') as f:
        trade_data = json.load(f)
except FileNotFoundError:
    print("錯誤: 找不到 data/advanced_trade_value.json")
    print("請先執行: python3 generate_advanced_trade_value.py")
    exit(1)

print(f"數據生成時間: {trade_data['generated_at']}")
print(f"球員總數: {trade_data['total_players']}")
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

# 建立或取得工作表
print("步驟 2: 建立「進階交易價值」工作表...")

sheet_name = "進階交易價值"

try:
    value_sheet = spreadsheet.worksheet(sheet_name)
    print(f"工作表已存在，將更新內容")
except gspread.WorksheetNotFound:
    value_sheet = spreadsheet.add_worksheet(title=sheet_name, rows=500, cols=20)
    print(f"已建立新工作表")

print()

# 準備數據
print("步驟 3: 準備數據...")

players = trade_data['players']

# 標題行
headers = [
    "排名", "分級", "球員", "NBA球隊", "位置", "狀態",
    "Fantasy球隊", "勝率",
    "總分", "基礎", "位置價值", "多位置", "稀缺性", "健康", "球隊實力", "特殊"
]

rows = [
    ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    [f"進階交易價值評估 - {trade_data['generated_at']}", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    headers
]

# 數據行
for i, player in enumerate(players, 1):
    scores = player['scores']
    positions_str = ','.join(player['positions'])

    rows.append([
        i,
        player['tier'],
        player['player_name'],
        player['nba_team'],
        positions_str,
        player['status'],
        player['fantasy_team'],
        player['win_rate'],
        scores['total'],
        scores['base'],
        scores['position_value'],
        scores['multi_position_bonus'],
        scores['scarcity_bonus'],
        scores['health_value'],
        scores['team_strength'],
        scores['special_bonus']
    ])

print(f"已準備 {len(players)} 筆球員數據")
print()

# 寫入數據
print("步驟 4: 寫入數據...")
value_sheet.clear()
value_sheet.update(values=rows, range_name='A1')
print("數據寫入完成")
print()

# 格式化
print("步驟 5: 套用格式...")

# 標題行格式
value_sheet.format('A2:P2', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 14},
    "horizontalAlignment": "CENTER"
})

# 欄位標題格式
value_sheet.format('A4:P4', {
    "backgroundColor": {"red": 0.7, "green": 0.7, "blue": 0.7},
    "textFormat": {"bold": True},
    "horizontalAlignment": "CENTER"
})

# 分級顏色
tier_colors = {
    'S': {"red": 1, "green": 0.84, "blue": 0},      # 金色
    'A': {"red": 0.75, "green": 0.75, "blue": 0.75},  # 銀色
    'B': {"red": 0.8, "green": 0.52, "blue": 0.25},   # 銅色
    'C': {"red": 0.85, "green": 0.92, "blue": 0.83},  # 淺綠
    'D': {"red": 0.95, "green": 0.95, "blue": 0.95}   # 淺灰
}

print("套用分級顏色...")
for i, player in enumerate(players, 5):  # 從第5行開始（跳過標題）
    tier = player['tier']
    if tier in tier_colors:
        try:
            value_sheet.format(f'B{i}:B{i}', {
                "backgroundColor": tier_colors[tier],
                "textFormat": {"bold": True},
                "horizontalAlignment": "CENTER"
            })
        except:
            pass  # 忽略格式化錯誤

print("格式套用完成")
print()

# 調整欄寬
print("步驟 6: 調整欄寬...")
try:
    requests = [
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': value_sheet.id,
                    'dimension': 'COLUMNS',
                    'startIndex': 0,
                    'endIndex': 1
                },
                'properties': {'pixelSize': 50},
                'fields': 'pixelSize'
            }
        },
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': value_sheet.id,
                    'dimension': 'COLUMNS',
                    'startIndex': 1,
                    'endIndex': 2
                },
                'properties': {'pixelSize': 40},
                'fields': 'pixelSize'
            }
        },
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': value_sheet.id,
                    'dimension': 'COLUMNS',
                    'startIndex': 2,
                    'endIndex': 3
                },
                'properties': {'pixelSize': 150},
                'fields': 'pixelSize'
            }
        },
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': value_sheet.id,
                    'dimension': 'COLUMNS',
                    'startIndex': 6,
                    'endIndex': 7
                },
                'properties': {'pixelSize': 150},
                'fields': 'pixelSize'
            }
        }
    ]
    spreadsheet.batch_update({'requests': requests})
    print("欄寬調整完成")
except Exception as e:
    print(f"欄寬調整失敗: {e}")

print()

# 完成
print("=" * 80)
print("  同步完成！")
print("=" * 80)
print()
print(f"Google Sheets: {spreadsheet.url}")
print(f"工作表: {sheet_name}")
print(f"球員數: {len(players)}")
print()

# 顯示分級統計
tier_dist = trade_data['tier_distribution']
print("分級分佈:")
for tier in ['S', 'A', 'B', 'C', 'D']:
    count = tier_dist.get(tier, 0)
    print(f"  {tier} 級: {count} 人")

print()
print("提示:")
print("  - 使用下拉篩選可以快速找到特定分級的球員")
print("  - 總分越高，交易價值越高")
print("  - 可依需求排序各項評分欄位")
print()
