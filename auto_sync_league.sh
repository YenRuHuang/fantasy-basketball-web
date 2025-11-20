#!/bin/bash

# 聯盟數據自動同步腳本

cd /Users/murs/Documents/fantasy-basketball-analyzer

# 啟動虛擬環境（如果有的話）
# source venv/bin/activate

# 獲取完整聯盟數據
echo "$(date): 開始獲取聯盟數據..."
python3 get_full_league_data.py >> logs/league_fetch.log 2>&1

if [ $? -eq 0 ]; then
    echo "$(date): 數據獲取成功，開始同步到 Google Sheets..."
    python3 sync_league_shared.py >> logs/league_sync.log 2>&1

    if [ $? -eq 0 ]; then
        echo "$(date): Google Sheets 同步完成！"

        # 同步到 Zeabur 網頁版
        echo "$(date): 開始部署到 Zeabur..."
        ./deploy_to_zeabur.sh >> logs/zeabur_deploy.log 2>&1

        if [ $? -eq 0 ]; then
            echo "$(date): Zeabur 部署完成！"
        else
            echo "$(date): Zeabur 部署失敗（不影響 Google Sheets）"
        fi
    else
        echo "$(date): Google Sheets 同步失敗"
    fi
else
    echo "$(date): 數據獲取失敗"
fi
