#!/bin/bash

# 大亂鬥聯盟 - 一鍵更新腳本
# 盟主專用：更新聯盟數據並同步到 Google Sheets

echo "============================================================"
echo " 大亂鬥聯盟 - 數據更新"
echo "============================================================"
echo ""

# 切換到專案目錄
cd /Users/murs/Documents/fantasy-basketball-analyzer

echo "步驟 1: 獲取最新聯盟數據..."
echo ""

# 獲取聯盟數據
echo "5zaskuw" | python3 get_league_data.py > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ 聯盟數據已獲取"
    echo ""
else
    echo "❌ 獲取聯盟數據失敗"
    echo ""
    exit 1
fi

echo "步驟 2: 同步到 Google Sheets..."
echo ""

# 同步到 Google Sheets
python3 sync_league_to_sheets.py > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Google Sheets 已更新"
    echo ""
else
    echo "❌ 同步失敗"
    echo ""
    exit 1
fi

echo "============================================================"
echo " ✅ 更新完成！"
echo "============================================================"
echo ""
echo "📊 Google Sheets:"
echo "https://docs.google.com/spreadsheets/d/19EPLNaYJTHlqZbMLlaQgF-OtmjLDMmb46ldem1380-o"
echo ""
echo "已更新:"
echo "  • 聯盟排名（14 支隊伍）"
echo "  • 本週對戰"
echo "  • 賽程表"
echo ""
echo "你的個人數據會每小時自動更新，不需手動操作！"
echo ""
