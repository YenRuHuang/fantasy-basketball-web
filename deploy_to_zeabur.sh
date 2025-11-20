#!/bin/bash

echo "========================================================================"
echo " Fantasy Basketball Data Center - Zeabur 自動部署"
echo "========================================================================"
echo ""

# 顏色定義
GREEN='\033[0.32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 檢查是否在正確的目錄
if [ ! -d "web" ]; then
    echo -e "${RED}❌ 錯誤：找不到 web/ 目錄${NC}"
    echo "請在 fantasy-basketball-analyzer 目錄下執行此腳本"
    exit 1
fi

# 步驟 1: 匯出最新數據
echo -e "${YELLOW}步驟 1: 匯出最新聯盟數據...${NC}"
python3 export_for_web.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 數據匯出失敗${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 數據匯出成功${NC}"
echo ""

# 步驟 2: 進入 web 目錄
cd web/

# 步驟 3: 檢查是否已初始化 Git
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}步驟 2: 初始化 Git 倉庫...${NC}"
    git init
    git add .
    git commit -m "Initial commit: Fantasy Basketball Data Center"

    echo -e "${GREEN}✅ Git 倉庫初始化完成${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  請先完成以下步驟：${NC}"
    echo "1. 在 GitHub 建立新倉庫：fantasy-basketball-web"
    echo "2. 執行以下命令設定遠端倉庫："
    echo ""
    echo -e "${GREEN}   git remote add origin https://github.com/YOUR_USERNAME/fantasy-basketball-web.git${NC}"
    echo -e "${GREEN}   git branch -M main${NC}"
    echo -e "${GREEN}   git push -u origin main${NC}"
    echo ""
    echo "3. 前往 Zeabur Dashboard 連接該倉庫"
    echo ""
    exit 0
fi

# 步驟 4: 檢查是否有遠端倉庫
REMOTE_URL=$(git remote get-url origin 2>/dev/null)

if [ -z "$REMOTE_URL" ]; then
    echo -e "${YELLOW}⚠️  尚未設定遠端倉庫${NC}"
    echo "請執行："
    echo -e "${GREEN}   git remote add origin https://github.com/YOUR_USERNAME/fantasy-basketball-web.git${NC}"
    exit 1
fi

echo -e "${YELLOW}步驟 3: 檢查更新...${NC}"
echo "遠端倉庫: $REMOTE_URL"
echo ""

# 步驟 5: 提交更新
echo -e "${YELLOW}步驟 4: 提交數據更新...${NC}"

# 檢查是否有變更
if git diff --quiet && git diff --cached --quiet; then
    echo -e "${GREEN}✅ 沒有需要更新的數據${NC}"
    exit 0
fi

# 添加所有變更
git add .

# 提交
COMMIT_MSG="Update league data: $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$COMMIT_MSG"

echo -e "${GREEN}✅ 變更已提交${NC}"
echo ""

# 步驟 6: 推送到遠端
echo -e "${YELLOW}步驟 5: 推送到 GitHub...${NC}"
git push

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 推送失敗${NC}"
    echo "請檢查 GitHub 連接和權限"
    exit 1
fi

echo -e "${GREEN}✅ 推送成功${NC}"
echo ""

# 完成
echo "========================================================================"
echo -e " ${GREEN}✅ 部署完成！${NC}"
echo "========================================================================"
echo ""
echo "Zeabur 會在幾分鐘內自動重新部署"
echo ""
echo "檢查部署狀態："
echo "  https://dash.zeabur.com"
echo ""
echo "查看最新提交："
echo "  $REMOTE_URL"
echo ""

# 返回原目錄
cd ..
