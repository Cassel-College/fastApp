#!/bin/bash

# 激活虚拟环境
# source venv/bin/activate

# 启动 FastAPI 应用
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
python3 -m uvicorn --host 0.0.0.0 --port 8000 main:app --reload