import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging_config import setup_logging

# 设置日志
setup_logging()

app = FastAPI()

# 设置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)

logger = logging.getLogger(__name__)
logger.info("FastAPI与Flutter的应用已启动!")

# 导入路由
from app.api.v1.endpoints import example

# 包含路由
app.include_router(example.router, prefix="/api/v1/example", tags=["example"])

@app.get("/")
def read_root():
    return {"message": "欢迎使用FastAPI与Flutter的应用!"}