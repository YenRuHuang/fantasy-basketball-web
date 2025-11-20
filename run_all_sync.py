#!/usr/bin/env python3
"""
完整的自動同步和部署腳本
每小時執行一次，更新數據並部署到 Zeabur
"""

import subprocess
import sys
import os
from datetime import datetime

# 設定工作目錄
os.chdir('/Users/murs/Documents/fantasy-basketball-snakestar')

def run_command(cmd, description):
    """執行命令並記錄結果"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {description}...")

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 分鐘超時
        )

        if result.returncode == 0:
            print(f"[{timestamp}] ✅ {description} 成功")
            return True
        else:
            print(f"[{timestamp}] ⚠️ {description} 失敗: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"[{timestamp}] ⏱️ {description} 超時")
        return False
    except Exception as e:
        print(f"[{timestamp}] ❌ {description} 錯誤: {str(e)[:200]}")
        return False

def main():
    print("=" * 80)
    print(" 蛇星刁手 Fantasy Basketball - 自動同步")
    print("=" * 80)
    print()

    # 步驟 1: 獲取 Yahoo 數據
    if not run_command('python3 get_full_league_data.py', '獲取 Yahoo 聯盟數據'):
        print("❌ Yahoo 數據獲取失敗，中止")
        sys.exit(1)

    # 步驟 2: 生成聯盟洞察
    run_command('python3 generate_league_insights.py', '生成聯盟洞察')

    # 步驟 3: 生成進階交易價值
    run_command('python3 generate_advanced_trade_value.py', '生成進階交易價值')

    # 步驟 4: 同步到聯盟共享 Sheets
    run_command('python3 sync_league_shared.py', '同步聯盟共享 Sheets')

    # 步驟 5: 同步聯盟洞察
    run_command('python3 sync_league_insights.py', '同步聯盟洞察')

    # 步驟 6: 同步進階交易價值
    run_command('python3 sync_advanced_trade_value.py', '同步進階交易價值')

    # 步驟 7: 同步個人球隊數據
    run_command('python3 sync_my_team.py', '同步個人球隊數據（默斯佛陀）')

    # 步驟 8: 部署到 Zeabur
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 部署到 Zeabur...")

    # 複製數據到 web 目錄
    os.system('cp data/full_league_data.json web/data/ 2>/dev/null')
    os.system('cp data/advanced_trade_value.json web/data/ 2>/dev/null')
    os.system('cp data/league_insights.json web/data/ 2>/dev/null')

    # Git 操作
    os.chdir('web')

    # Pull 最新代碼
    os.system('git pull origin main > /dev/null 2>&1')

    # 檢查是否有變更
    result = subprocess.run('git diff --quiet data/*.json', shell=True)

    if result.returncode != 0:  # 有變更
        # Commit and push
        os.system('git add data/*.json')
        commit_msg = f"""auto: 更新聯盟數據 {datetime.now().strftime('%Y-%m-%d %H:%M')}

📊 自動更新：
- 聯盟數據 (198 名球員, 14 支隊伍)
- 進階交易價值 (5 維度評分)
- 聯盟洞察 (賽程分析/每週戰報)
- 當前週次和對戰資訊

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"""

        os.system(f'git commit -m "{commit_msg}"')
        push_result = os.system('git push origin main')

        if push_result == 0:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Zeabur 部署觸發成功")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🌐 網頁將在 1-2 分鐘內自動更新")
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⚠️ GitHub 推送失敗")
    else:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ℹ️ 數據無變更，跳過部署")

    # 返回主目錄
    os.chdir('..')

    print()
    print("=" * 80)
    print(f" 自動同步完成！{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

if __name__ == '__main__':
    main()
