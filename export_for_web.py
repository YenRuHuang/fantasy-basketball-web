"""
匯出數據給網頁使用
"""

import json
import shutil
from pathlib import Path

print("=" * 80)
print(" 匯出數據給網頁使用")
print("=" * 80)
print()

# 讀取數據
with open('data/full_league_data.json', 'r', encoding='utf-8') as f:
    league_data = json.load(f)

# 建立 web 目錄
web_dir = Path('web')
web_dir.mkdir(exist_ok=True)

# 複製 HTML 檔案
shutil.copy('web_viewer.html', web_dir / 'index.html')

# 建立 data 目錄
(web_dir / 'data').mkdir(exist_ok=True)

# 匯出 JSON
with open(web_dir / 'data' / 'full_league_data.json', 'w', encoding='utf-8') as f:
    json.dump(league_data, f, ensure_ascii=False, indent=2)

print("✅ 網頁檔案已匯出至 web/ 目錄")
print()
print("包含檔案:")
print("  • index.html - 網頁界面")
print("  • data/full_league_data.json - 聯盟數據")
print()
print("=" * 80)
print(" 部署選項")
print("=" * 80)
print()
print("選項 1: GitHub Pages (免費)")
print("  1. 在 GitHub 建立 repository")
print("  2. 上傳 web/ 目錄內的所有檔案")
print("  3. 在 Settings > Pages 啟用 GitHub Pages")
print("  4. 你會得到一個網址如: https://yourusername.github.io/repo-name/")
print()
print("選項 2: Netlify Drop (最簡單)")
print("  1. 前往 https://app.netlify.com/drop")
print("  2. 直接拖拽 web/ 資料夾")
print("  3. 立即取得網址!")
print()
print("選項 3: Vercel (推薦)")
print("  1. 前往 https://vercel.com")
print("  2. Import web/ 資料夾")
print("  3. 自動部署!")
print()
print("💡 每次執行 auto_sync_league.sh 後，記得重新執行此腳本並重新部署")
print()
