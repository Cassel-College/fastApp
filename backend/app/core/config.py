#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Peng.liu
# @Date: 2023-09-14 22:00:00
# @LastEditTime: 2023-09-14 22:00:00
# @FilePath: /fastapi-flutter/app/core/config.py

from pydantic import BaseSettings
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE_PATH = os.path.join(BASE_DIR, 'app.log')

class Settings(BaseSettings):
    app_name: str = "FastAPI Flutter App"
    admin_email: str = "admin@example.com"
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "your_secret_key"
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()