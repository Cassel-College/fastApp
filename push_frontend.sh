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
git add ./lib/*
git add ./config/*
git add ./pubspec.yaml
git add ./README.md

# 提交更改
git commit -m "Update frontend code"

# 推送到远程仓库
git push -u origin main

# 返回项目根目录
cd ..

echo "Frontend code pushed to GitHub successfully!"