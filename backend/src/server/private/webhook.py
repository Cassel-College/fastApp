#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import json
import os

# import framework
from fastapi import APIRouter, Body, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request
from pydantic import BaseModel

# import other server
from src.model.private.scene_model import Scene
from src.model.public.log_model import LogModel
from src.model.public.return_info import ReturnCode, ReturnInfo
from src.server.public.third_party_script import ScriptInput, exec_third_party_script
from src.tools.public.config_tools import ConfigTools
from src.tools.public.io_tools.io_tools import IOTools
from src.tools.public.log_tools.log_tools import LogTools

from src.tools.public.gmini_tools.gmini_tools import GeminiAPI
from src.tools.private.policy_file_tools.policy_file_tools import PolicyFileTools
from src.tools.private.prompt_tools.prompt_tools import PromptTools

from src.server.public.agent_server import GPT, gmini_agent

router = APIRouter()

class WEBHOOK_INPUT(BaseModel):
    info: str
    script_type: str


@router.post("/search_crawler")
def webhook(webhook_input: WEBHOOK_INPUT = Body(...)):
    
    log_server = LogTools()
    info = webhook_input.info
    script_type = webhook_input.script_type
    
    
    log_info = f"webhook info: {info}, script_type: {script_type}"
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    
    input_info = ScriptInput(input_info=info)
    search_result = exec_third_party_script(input_info)
    
    # data = {"data": "企业特定的搜索爬虫，暂未开放。搜索Keyword: " + info}
    return_info = ReturnInfo.create(code=ReturnCode.SUCCESS,
                                        message="",
                                        data=search_result)
    return return_info