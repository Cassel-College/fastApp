#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import json
import os
import sys

# import framework
from fastapi import APIRouter, Body, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request
from pydantic import BaseModel

# import other server
from src.model.public.log_model import LogModel
from src.model.public.return_info import ReturnCode, ReturnInfo
from src.tools.public.config_tools import ConfigTools
from src.tools.public.log_tools.log_tools import LogTools


router = APIRouter()


class PorxyInfo(BaseModel):
    ip: str
    port: str
    username: str
    password: str


@router.post("/check_porxy_info")
def check_porxy_info(porxy_info: PorxyInfo = Body(...)):
    
    log_server = LogTools()
    config = ConfigTools()
    log_server.write_log(log=LogModel(f"Check proxy info: {porxy_info}.", "INFO"))
    
    target_password_key = porxy_info.password
    
    target_username = config.get_root_username()
    target_password = config.check_root_passwork()
    
    
    # 检查密码
    if target_password == target_password_key and target_username == porxy_info.username:
        log_server.write_log(log=LogModel(f"Check proxy info success.", "INFO"))
        return_info = ReturnInfo.create(code=ReturnCode.SUCCESS,
                                        message="Check proxy info success.", 
                                        data={"ip": porxy_info.ip, "port": porxy_info.port})
    else:
        log_server.write_log(log=LogModel(f"Check proxy info failed.", "ERROR"))
        error_port = int(porxy_info.port) + 1
        return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                        message="Check proxy info failed. Your password is wrong.", 
                                        data={"ip": porxy_info.ip, "port": str(error_port)})
    return return_info
    