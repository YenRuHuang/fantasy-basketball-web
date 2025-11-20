#!/bin/bash

# Fantasy Basketball - 快速同步到 Google Sheets
# 作者: Claude Code
# 用途: 一鍵更新陣容數據並同步到 Google Sheets

echo "============================================================"
echo " Fantasy Basketball 快速同步系統"
echo "============================================================"
echo ""

# 切換到專案目錄
cd /Users/murs/Documents/fantasy-basketball-analyzer

# 檢查是否已設定 Google Service Account
if [ ! -f "config/google_service_account.json" ]; then
    echo "❌ 尚未設定 Google Service Account"
    echo ""
    echo "請先完成以下步驟："
    echo "1. 閱讀 GOOGLE_SHEETS_SETUP.md"
    echo "2. 建立 Google Service Account"
    echo "3. 下載 JSON 金鑰檔案"
    echo "4. 移動到 config/google_service_account.json"
    echo ""
    exit 1
fi

# 檢查是否已設定 Spreadsheet ID
if grep -q "請替換成你的 Spreadsheet ID" config/google_sheets_config.json; then
    echo "❌ 尚未設定 Spreadsheet ID"
    echo ""
    echo "請編輯 config/google_sheets_config.json"
    echo "將 spreadsheet_id 改為你的 Google Sheets ID"
    echo ""
    exit 1
fi

echo "步驟 1: 更新 Yahoo Fantasy 陣容數據..."
echo ""

# 更新陣容數據（使用已保存的 token）
echo "5zaskuw" | python3 get_full_roster_data.py > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ 陣容數據已更新"
    echo ""
else
    echo "⚠️  無法連接 Yahoo API，使用現有數據"
    echo ""
fi

echo "步驟 2: 同步到 Google Sheets..."
echo ""

# 同步到 Google Sheets
python3 sync_to_sheets.py

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo " ✅ 同步完成！"
    echo "============================================================"
    echo ""
    echo "你的 Fantasy Basketball 數據已同步到 Google Sheets"
    echo ""
else
    echo ""
    echo "============================================================"
    echo " ❌ 同步失敗"
    echo "============================================================"
    echo ""
    echo "請檢查："
    echo "1. Google Service Account 設定正確"
    echo "2. Spreadsheet ID 正確"
    echo "3. Service Account 已加入 Google Sheets 共用名單"
    echo ""
    exit 1
fi
