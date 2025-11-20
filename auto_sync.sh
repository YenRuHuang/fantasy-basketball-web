#!/bin/bash

# Fantasy Basketball 自動同步腳本
# 用於 crontab 定時執行

# 設定專案目錄
PROJECT_DIR="/Users/murs/Documents/fantasy-basketball-analyzer"
LOG_FILE="$PROJECT_DIR/logs/auto_sync.log"

# 記錄開始時間
echo "========================================" >> "$LOG_FILE"
echo "開始同步: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"

# 切換到專案目錄
cd "$PROJECT_DIR"

# 執行同步（靜默模式，只記錄錯誤）
python3 sync_to_sheets.py >> "$LOG_FILE" 2>&1

# 檢查執行結果
if [ $? -eq 0 ]; then
    echo "✅ 同步成功: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
else
    echo "❌ 同步失敗: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"

# 保持日誌文件不超過 1000 行
tail -n 1000 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
