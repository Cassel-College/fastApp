# FastAPI & Flutter 项目文档

## 项目概述

该项目是一个基于 FastAPI 和 Flutter 的全栈应用程序，旨在快速开发和部署现代 Web 应用。后端使用 FastAPI 框架构建，提供高性能的 API 接口；前端使用 Flutter 框架构建，提供流畅的用户界面。

## 目录结构

```
fastapi-flutter-app
├── backend
│   ├── app
│   │   ├── main.py                # FastAPI 应用的入口点
│   │   ├── api
│   │   │   └── v1
│   │   │       └── endpoints
│   │   │           └── example.py # 示例 API 端点
│   │   ├── core
│   │   │   └── config.py          # 应用配置
│   │   ├── models
│   │   │   └── example.py          # 数据模型
│   │   ├── schemas
│   │   │   └── example.py          # 数据验证和序列化模式
│   │   ├── crud
│   │   │   └── example.py          # 数据库基本操作
│   │   └── tests
│   │       └── test_example.py     # 单元测试
│   ├── requirements.txt            # Python 依赖包
│   └── README.md                   # 后端文档
├── frontend
│   ├── lib
│   │   ├── main.dart               # Flutter 应用的入口点
│   │   ├── screens
│   │   │   └── home_screen.dart    # 主屏幕 UI
│   │   └── widgets
│   │       └── example_widget.dart  # 示例小部件
│   ├── pubspec.yaml                # Flutter 项目配置
│   └── README.md                   # 前端文档
└── README.md                       # 整个项目文档
```

## 快速开始

1. **克隆项目**

   ```bash
   git clone https://github.com/your-repo/fastapi-flutter-app.git
   cd fastapi-flutter-app
   ```

2. **设置后端**

   - 进入 `backend` 目录
   - 安装依赖

     ```bash
     pip install -r requirements.txt
     ```

   - 运行 FastAPI 应用

     ```bash
     uvicorn app.main:app --reload
     ```

3. **设置前端**

   - 进入 `frontend` 目录
   - 安装依赖

     ```bash
     flutter pub get
     ```

   - 运行 Flutter 应用

     ```bash
     flutter run
     ```

## 贡献

欢迎提交问题和拉取请求！请确保遵循项目的贡献指南。

## 许可证

该项目遵循 MIT 许可证。有关详细信息，请参阅 LICENSE 文件。