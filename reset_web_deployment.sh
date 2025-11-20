#!/bin/bash

echo "========================================================================"
echo " 重新設定 Zeabur 部署 - 只部署 web 目錄"
echo "========================================================================"
echo ""

# 進入 web 目錄
cd web/

# 檢查是否已經有 .git
if [ -d ".git" ]; then
    echo "清理舊的 git 配置..."
    rm -rf .git
fi

# 初始化新的 git 倉庫
echo "初始化 web 目錄的 git 倉庫..."
git init
git add .
git commit -m "Initial commit: Web frontend only"

# 設定遠端倉庫
echo ""
echo "設定遠端倉庫..."
git remote add origin https://github.com/YenRuHuang/fantasy-basketball-web.git
git branch -M main

# 強制推送（覆蓋遠端）
echo ""
echo "⚠️  即將強制推送到 GitHub（會覆蓋現有內容）"
read -p "確定要繼續嗎？ (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push -f origin main
    echo ""
    echo "========================================================================"
    echo " ✅ 完成！Zeabur 現在應該能正確部署了"
    echo "========================================================================"
    echo ""
    echo "Zeabur 會自動偵測到更新並重新部署"
    echo "這次應該會成功識別為 Node.js 專案"
else
    echo "取消操作"
fi

cd ..
