#!/bin/bash

echo "========================================================================"
echo " Fantasy 大亂鬥 - 快速數據更新並推送"
echo "========================================================================"
echo ""

cd /Users/murs/Documents/fantasy-basketball-analyzer

# 1. 重新獲取聯盟數據
echo "📊 步驟 1: 獲取最新聯盟數據..."
python3 get_full_league_data.py
if [ $? -ne 0 ]; then
    echo "❌ 數據獲取失敗"
    exit 1
fi

# 2. 生成洞察分析
echo ""
echo "🔍 步驟 2: 生成聯盟洞察..."
python3 generate_league_insights.py

# 3. 生成交易價值
echo ""
echo "💎 步驟 3: 生成進階交易價值..."
python3 generate_advanced_trade_value.py

# 4. 複製到 web 目錄
echo ""
echo "📁 步驟 4: 複製數據到 web 目錄..."
cp data/full_league_data.json web/data/
cp data/league_insights.json web/data/
cp data/advanced_trade_value.json web/data/

# 5. 推送到 GitHub
echo ""
echo "🚀 步驟 5: 推送到 GitHub..."
git add web/data/*.json
git commit -m "Data: Auto update at $(date '+%Y-%m-%d %H:%M')"
git push origin main

echo ""
echo "========================================================================"
echo " ✅ 完成！數據已推送到 GitHub"
echo "========================================================================"
echo ""
echo "現在請前往 Zeabur Dashboard 手動觸發重新部署："
echo "  1. 前往 https://dash.zeabur.com"
echo "  2. 找到 fantasy-basketball-web 專案"
echo "  3. 點擊 Redeploy 按鈕"
echo ""
