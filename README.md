# FastAPI & Flutter Web App

## 项目简介
这是一个使用 FastAPI 作为后端和 Flutter 作为前端的快速开发 Web 应用模板。该项目旨在提供一个简单的起始点，帮助开发者快速构建和部署全栈应用。

## 项目结构
```
fastapi-flutter-app
├── backend                # 后端代码
│   ├── app                # FastAPI 应用
│   │   ├── main.py        # 应用入口
│   │   ├── api            # API 路由
│   │   │   └── v1
│   │   │       └── endpoints
│   │   │           └── example.py  # 示例端点
│   │   ├── core           # 核心配置
│   │   │   └── config.py  # 配置文件
│   │   ├── models         # 数据模型
│   │   │   └── example.py  # 示例模型
│   │   ├── schemas        # 数据验证模式
│   │   │   └── example.py  # 示例模式
│   │   ├── crud           # 数据库操作
│   │   │   └── example.py  # 示例 CRUD 操作
│   │   └── tests          # 单元测试
│   │       └── test_example.py  # 示例测试
│   ├── requirements.txt    # Python 依赖
│   └── README.md           # 后端文档
├── frontend               # 前端代码
│   ├── lib                # Flutter 应用
│   │   ├── main.dart      # 应用入口
│   │   ├── screens        # 屏幕
│   │   │   └── home_screen.dart  # 主屏幕
│   │   └── widgets        # 组件
│   │       └── example_widget.dart  # 示例组件
│   ├── pubspec.yaml       # Flutter 配置
│   └── README.md          # 前端文档
└── README.md              # 整个项目文档
```

## 安装与运行

### 后端
1. 进入 `backend` 目录。
2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```
3. 运行 FastAPI 应用：
   ```
   uvicorn app.main:app --reload
   ```

### 前端
1. 进入 `frontend` 目录。
2. 安装依赖：
   ```
   flutter pub get
   ```
3. 运行 Flutter 应用：
   ```
   flutter run
   ```

## 贡献
欢迎任何形式的贡献！请提交问题或拉取请求。

## 许可证
本项目采用 MIT 许可证。