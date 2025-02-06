#!/bin/bash

# 打印进入 backend 目录的消息
echo "Entering backend directory..."
cd backend

# 打印运行 backend 的 Docker 镜像构建脚本的消息
echo "Running backend Docker image build script..."
sh build_docker_image.sh

# 打印返回项目根目录的消息
echo "Returning to project root directory..."
cd ..

# 打印进入 frontend 目录的消息
echo "Entering frontend directory..."
cd frontend

# 打印运行 frontend 的 Docker 镜像构建脚本的消息
echo "Running frontend Docker image build script..."
sh gen_docker_image.sh

# 打印返回项目根目录的消息
echo "Returning to project root directory..."
cd ..