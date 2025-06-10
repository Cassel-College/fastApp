#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from typing import Union
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.sessions import SessionMiddleware
# from starlette.requests import Request

from src.tools.public.config_tools import ConfigTools
from src.tools.public.user_system_tools.init_user_system_tools.Init_user_ysystem_tools import InitUserSystemTools
from src.server.public import policy_server
from src.server.private import gen_scenarios_server
from src.server.public import agent_server
from src.server.private import generate_simple_scenas
from src.server.private import webhook
from src.server.public import third_party_script
from src.server.private import generate_full_scenas
from src.server.public import check_porxy
from src.server.public import user_system_server
from src.server.public import thread_pool_server

InitUserSystemTools().run()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，生产环境中应该更具体
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(policy_server.router, prefix="/api/v1/policy")
app.include_router(gen_scenarios_server.router, prefix="/api/v1/gen_scenarios")
app.include_router(agent_server.router, prefix="/api/v1/agent")
app.include_router(generate_simple_scenas.router, prefix="/api/v1/generate_simple_scenas")
app.include_router(webhook.router, prefix="/api/v1/webhook")
app.include_router(third_party_script.router, prefix="/api/v1/third_party_script")
app.include_router(generate_full_scenas.router, prefix="/api/v1/generate_full_scenas")
app.include_router(check_porxy.router, prefix="/api/v1/porxy")
app.include_router(user_system_server.router, prefix="/api/v1/user_system")
app.include_router(thread_pool_server.router, prefix="/api/v1/thread_pool_server")


@app.get("/")
async def root():
    a = ConfigTools()
    print(a.get_config())
    return {"message": "Hello World"}
