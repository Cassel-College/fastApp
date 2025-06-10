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
from src.model.public.log_model import LogModel
from src.model.public.return_info import ReturnCode, ReturnInfo
from src.tools.public.config_tools import ConfigTools
from src.tools.public.datatime_tools.datatime_tools import DatetimeTools
from src.tools.public.log_tools.log_tools import LogTools
from src.tools.public.io_tools.io_tools import IOTools
from src.tools.public.script_tools.script_tools import ScriptTools
from src.tools.public.user_system_tools.user_info_tools.user_info_tools import UserInfoTools
from src.tools.public.user_system_tools.user_registered_tools.user_registered_tools import UserRegisteredTools
from src.tools.public.user_system_tools.user_loading_tools.user_loading_tools import UserLoadingTools
from src.model.public.user_info import UserInfo

router = APIRouter()

@router.post("/get_user_list")
def get_user_list():
    
    log_server = LogTools()
    config = ConfigTools()
    log_info = f"Get user list"
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    users = []
    try:
        users = UserRegisteredTools().get_user_list()
    except Exception as e:
        log_info = f"Exec third party script failed: {e}"
        log_server.write_log(log=LogModel(log_info, "ERROR"))
        return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                        message=log_info, 
                                        data={"users": users})
        return return_info
    log_info = f"Get users info over."
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    log_info = f"Exec third party script success."
    return_info = ReturnInfo.create(code=ReturnCode.SUCCESS,
                                        message=log_info, 
                                        data={"users": users})
    return return_info
  

@router.post("/user_registered")
def user_registered(user_info: UserInfo = Body(...)):
    
    log_server = LogTools()
    config = ConfigTools()
    log_info = f"User registered: user info: {user_info}"
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    registered_result = ReturnInfo(
        code=ReturnCode.FAILED,
        message="User registered failed",
        data={"user_info": user_info})
    try:
        registered_result = UserRegisteredTools().registered_user(user_info=user_info)
    except Exception as e:
        log_info = f"Register user failed: {e}"
        log_server.write_log(log=LogModel(log_info, "ERROR"))
    return registered_result  

@router.post("/user_landing")
def user_landing(user_info: UserInfo = Body(...)):
    
    log_server = LogTools()
    config = ConfigTools()
    log_info = f"User Landing: user info: {user_info}"
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    landing_result = ReturnInfo(
        code=ReturnCode.FAILED,
        message="User Landing failed",
        data={"user_info": user_info})
    try:
        landing_result = UserLoadingTools().loading_user(user_info=user_info)
    except Exception as e:
        log_info = f"User Landing failed: {e}"
        log_server.write_log(log=LogModel(log_info, "ERROR"))
    return landing_result  


@router.post("/check_user_landing")
def user_landing(user_info: UserInfo = Body(...)):
    
    log_server = LogTools()
    config = ConfigTools()
    log_info = f"Check User Landing: user info: {user_info}"
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    landing_result = ReturnInfo(
        code=ReturnCode.FAILED,
        message="User Landing failed",
        data={"user_info": user_info})
    try:
        landing_result = UserLoadingTools().check_user_loading_verify(user_info=user_info)
    except Exception as e:
        log_info = f"User Landing failed: {e}"
        log_server.write_log(log=LogModel(log_info, "ERROR"))
    return landing_result  


@router.post("/get_user_actions")
def get_user_actions(user_info: UserInfo = Body(...)):
    
    check_last_action_model = False
    log_server = LogTools()
    config = ConfigTools()
    dt_bots = DatetimeTools()
    operation_name="get_user_actions"
    
    log_info = f"get user actions: {user_info}"
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    user_landing_result = user_landing(user_info=user_info)
    if user_landing_result.code != ReturnCode.SUCCESS:
        log_info = f"User Landing failed: {user_info}"
        log_server.write_log(log=LogModel(log_info, "ERROR"))
        return user_landing_result
    else:
        log_info = f"User Landing status success: {user_info.user_name}."
        log_server.write_log(log=LogModel(log_info, "INFO"))
    
    user_actions_result = ReturnInfo(
        code=ReturnCode.FAILED,
        message="User Landing failed",
        data={"user_info": user_info})
    log_info = f"Try get user: {user_info.user_name} actions ..."
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    try:
        if check_last_action_model:
            check_user_operation_result = UserInfoTools().check_user_operation(
                user_info=user_info, 
                operation_name=operation_name)
            if check_user_operation_result.code == ReturnCode.SUCCESS:
                user_actions_result = UserInfoTools().get_user_action(user_info=user_info)
                action = {"action_name": operation_name, "datetime": dt_bots.get_now_YYYY_MM_DD_HH_MM_SS()}
                add_actions_result = UserInfoTools().add_user_action(user_info=user_info, action=action)
            else:
                log_info = f"User {user_info.user_name} operation: check get_user_actions failed."
                log_server.write_log(log=LogModel(log_info, "ERROR"))
                user_actions_result.message = check_user_operation_result.message
        else:
            user_actions_result = UserInfoTools().get_user_action(user_info=user_info)
    except Exception as e:
        log_info = f"User Landing failed: {e}"
        log_server.write_log(log=LogModel(log_info, "ERROR"))
        
    log_info = f"Get user: {user_info.user_name} actions over."
    log_server.write_log(log=LogModel(log_info, "INFO"))
    return user_actions_result  