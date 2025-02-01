#!/bin/bash

# 设置前端目录
FRONTEND_DIR="frontend"

# 检查是否已经是一个 Git 仓库
if [ ! -d ".git" ]; then
    echo "Initializing new Git repository..."
    # git init
    # git remote add origin <your-github-repo-url>
else
    echo "Git repository already exists."
fi

# 进入前端目录
cd $FRONTEND_DIR
NOW_PATH=$(pwd)
echo "Now in $NOW_PATH ..."

# 添加所有更改
git add -f ./lib
echo "git add ./lib"

git add -f ./assets
echo "git add ./assets"

git add -f ./pubspec.yaml
echo "git add ./pubspec.yaml"

git add -f ./README.md
echo "git add ./README.md"

git add -f ../push_frontend.sh
echo "git add ../push_frontend.sh"

# 显示当前的 Git 状态
echo "--------------------------------------------------------------------------------"
git status
echo "--------------------------------------------------------------------------------"

# 询问用户是否继续执行
read -p "Do you want to continue with the commit and push? (y/n): " CONTINUE

if [ "$CONTINUE" != "y" ]; then
    echo "Aborting the commit and push."
    exit 1
fi

# 提交更改
git commit -m "Update frontend code"

# 推送到远程仓库
git push -u origin main

# 返回项目根目录
cd ..

echo "Frontend code pushed to GitHub successfully!"