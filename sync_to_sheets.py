"""
同步 Yahoo Fantasy Basketball 數據到 Google Sheets
像你朋友一樣的實時同步系統
"""

import sys
sys.path.insert(0, 'src')

import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

print("=" * 80)
print(" Fantasy Basketball → Google Sheets 同步")
print("=" * 80)
print()
print(f"同步時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 載入配置
with open('config/google_sheets_config.json', 'r', encoding='utf-8') as f:
    sheets_config = json.load(f)

# 載入陣容數據
with open('data/my_roster_full.json', 'r', encoding='utf-8') as f:
    roster_data = json.load(f)

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
# 同步陣容數據
# ============================================================================
print("步驟 2: 同步陣容數據...")

try:
    roster_sheet = spreadsheet.worksheet(sheets_config['sheets']['roster'])
except gspread.WorksheetNotFound:
    roster_sheet = spreadsheet.add_worksheet(
        title=sheets_config['sheets']['roster'],
        rows=20,
        cols=10
    )

# 準備陣容數據
roster_headers = ["#", "球員名稱", "隊伍", "位置", "狀態", "備註"]
roster_rows = [roster_headers]

players = roster_data['players']
healthy_count = 0
injured_count = 0

for i, player in enumerate(players, 1):
    status = player['status'] if player['status'] else "健康"

    if status == "健康":
        status_emoji = "✅"
        healthy_count += 1
    elif status == "GTD":
        status_emoji = "⚠️"
    elif status == "INJ":
        status_emoji = "❌"
        injured_count += 1
    else:
        status_emoji = "❓"

    positions = ','.join(player['positions']) if player['positions'] else "N/A"

    remark = ""
    if status == "INJ":
        remark = "需要處理"
    elif status == "GTD":
        remark = "監控中"

    roster_rows.append([
        i,
        player['name'],
        player['team'],
        positions,
        f"{status_emoji} {status}",
        remark
    ])

# 寫入陣容數據
roster_sheet.clear()
roster_sheet.update('A1', roster_rows)

# 格式化標題
roster_sheet.format('A1:F1', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
    "horizontalAlignment": "CENTER"
})

print(f"✅ 陣容數據已同步 ({len(players)} 位球員)")
print()

# ============================================================================
# 同步統計摘要
# ============================================================================
print("步驟 3: 同步統計摘要...")

try:
    stats_sheet = spreadsheet.worksheet(sheets_config['sheets']['stats'])
except gspread.WorksheetNotFound:
    stats_sheet = spreadsheet.add_worksheet(
        title=sheets_config['sheets']['stats'],
        rows=15,
        cols=5
    )

# 準備統計數據
stats_data = [
    ["統計項目", "數值", ""],
    ["", "", ""],
    ["隊伍名稱", roster_data['team_name'], ""],
    ["聯盟", "大亂鬥 (ID# 71325)", ""],
    ["週次", f"Week {roster_data['week']}", ""],
    ["", "", ""],
    ["陣容狀態", "", ""],
    ["總球員數", len(players), ""],
    ["健康球員", healthy_count, "✅"],
    ["傷病球員", injured_count, "❌"],
    ["", "", ""],
    ["位置分布", "", ""],
]

# 計算位置分布
position_count = {}
for p in players:
    for pos in p['positions']:
        position_count[pos] = position_count.get(pos, 0) + 1

for pos in sorted(position_count.keys()):
    stats_data.append([f"  {pos}", position_count[pos], ""])

# 寫入統計數據
stats_sheet.clear()
stats_sheet.update('A1', stats_data)

# 格式化標題
stats_sheet.format('A1:C1', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
    "horizontalAlignment": "CENTER"
})

# 格式化小標題
stats_sheet.format('A3:A3', {"textFormat": {"bold": True, "fontSize": 12}})
stats_sheet.format('A7:A7', {"textFormat": {"bold": True, "fontSize": 12}})
stats_sheet.format('A12:A12', {"textFormat": {"bold": True, "fontSize": 12}})

print("✅ 統計摘要已同步")
print()

# ============================================================================
# 同步分析建議
# ============================================================================
print("步驟 4: 同步分析建議...")

try:
    analysis_sheet = spreadsheet.worksheet(sheets_config['sheets']['analysis'])
except gspread.WorksheetNotFound:
    analysis_sheet = spreadsheet.add_worksheet(
        title=sheets_config['sheets']['analysis'],
        rows=30,
        cols=3
    )

# 計算多位置球員
multi_pos_count = len([p for p in players if len(p['positions']) > 1])
bigs_count = len([p for p in players if set(p['positions']) == {'PF', 'C'}])
guards_count = len([p for p in players if set(p['positions']) == {'PG', 'SG'}])

# 準備分析數據（更新版 - 考慮多位置）
analysis_data = [
    ["分析項目", "內容", "優先級"],
    ["", "", ""],
    ["🏀 陣容診斷 (多位置分析)", "", ""],
    ["", "", ""],
    ["優勢", f"• 多位置球員: {multi_pos_count}/{len(players)} ({multi_pos_count/len(players)*100:.0f}%)", ""],
    ["", f"• {bigs_count} 名 PF/C 雙棲 (Giannis, Chet, Filipowski)", ""],
    ["", f"• {guards_count} 名 PG/SG 雙棲 (Mitchell, Nembhard, Lonzo)", ""],
    ["", "• 排陣靈活度高，位置調整彈性大", ""],
    ["", "", ""],
    ["劣勢", "• 2 名核心球員受傷 (Tatum, Kyrie)", "🔴"],
    ["", "• 4 名單一位置球員 (彈性較低)", "🟡"],
    ["", "• Kyrie, Westbrook, Suggs 都是純 PG", "🟡"],
    ["", "", ""],
    ["🔴 緊急事項", "", ""],
    ["", "", ""],
    ["1", "確認 Jayson Tatum 傷病狀態", "高"],
    ["", "→ 考慮交易換取即戰力", ""],
    ["", "", ""],
    ["2", "確認 Kyrie Irving 傷病狀態", "高"],
    ["", "→ 評估長期價值", ""],
    ["", "", ""],
    ["3", "監控 Jalen Suggs (GTD)", "中"],
    ["", "→ 確認復出時間", ""],
    ["", "", ""],
    ["💼 交易建議 (更新版)", "", ""],
    ["", "", ""],
    ["結論", "✅ 中鋒問題不嚴重！", ""],
    ["", f"   實際有 {bigs_count+1} 名可打 C 的球員", ""],
    ["", "", ""],
    ["方案1", "送出: Kyrie Irving (PG, INJ)", ""],
    ["", "換來: 健康的多位置球員", ""],
    ["", "理由: Kyrie 單一位置且受傷", ""],
    ["", "", ""],
    ["方案2", "送出: Tatum (SF/PF, INJ)", ""],
    ["", "換來: 即戰力側翼", ""],
    ["", "理由: Tatum 多位置但受傷", ""],
]

# 寫入分析數據
analysis_sheet.clear()
analysis_sheet.update('A1', analysis_data)

# 格式化
analysis_sheet.format('A1:C1', {
    "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
    "horizontalAlignment": "CENTER"
})

analysis_sheet.format('A3:A3', {
    "textFormat": {"bold": True, "fontSize": 14}
})

analysis_sheet.format('A13:A13', {
    "textFormat": {"bold": True, "fontSize": 14}
})

analysis_sheet.format('A24:A24', {
    "textFormat": {"bold": True, "fontSize": 14}
})

print("✅ 分析建議已同步")
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
print(f"  • {sheets_config['sheets']['roster']} - 陣容數據")
print(f"  • {sheets_config['sheets']['stats']} - 統計摘要")
print(f"  • {sheets_config['sheets']['analysis']} - 分析建議")
print()
print("💡 提示:")
print("  • 可以將此連結分享給聯盟成員")
print("  • 設定自動同步: 編輯 crontab 加入定時任務")
print("  • 手機查看: 使用 Google Sheets App")
print()
