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
from src.tools.public.config_tools import ConfigTools
from src.tools.public.io_tools.io_tools import IOTools
from src.tools.public.log_tools.log_tools import LogTools

from src.tools.public.gmini_tools.gmini_tools import GeminiAPI
from src.tools.private.policy_file_tools.policy_file_tools import PolicyFileTools
from src.tools.public.gpt_tools.gpt_tools import GPTAPI

router = APIRouter()

class GPT(BaseModel):
    text: str
    robot_type: str
    gpt_type: str
    api_key: str
    gpt_model: str


@router.post("/gpt")
def gmini_agent(gpt: GPT = Body(...)):
    
    log_server = LogTools()
    config = ConfigTools()
    text = gpt.text
    
    # 替换为你的 API 密钥
    api_key = config.get_gmini_api_key()
    model = config.get_gmini_model_name()
    
    log_info = f"Begin generate scenarios. used gpt from {model}."
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    # 初始化工具类
    gpt_api = GPTAPI(
        gpt_type=gpt.gpt_type,
        api_key=gpt.api_key,
        model=model)
    gpt_bot = gpt_api.gen_bot()
    # gemini_api = GeminiAPI(api_key, model=model)
    
    log_info = f"Create Agent success!"
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    # 调用生成内容的方法
    contents = [f"{str(text)}"]
    try:
        log_info = "Chat with GPT: " + text.replace('\n', '')
        log_server.write_log(log=LogModel(log_info, "INFO"))
        # result = gemini_api.generate_content(contents=contents)
        result = gpt_bot.chat(prompt=text)
    except Exception as e:
        result = {"error": str(e)}
    print("Response with default model: \n", json.dumps(result, ensure_ascii=False, indent=4))
    
    return_good = "choices" in result.keys() or "candidates" in result.keys()
    if isinstance(result, dict) and "error" not in result.keys() and return_good:
        answers = gpt_bot.extract_answers_all(result)
        log_info = "GPT answers: " + str(answers).replace('\n', '')
        log_server.write_log(log=LogModel(log_info, "INFO"))
        
        return_info = ReturnInfo.create(code=ReturnCode.SUCCESS, 
                                        message="Agent generate success!", 
                                        data=result)
    else:
        return_info = ReturnInfo.create(code=ReturnCode.FAILED, 
                                    message="Agent generate failed!", 
                                    data={"text": "Hello world!"})
    return return_info