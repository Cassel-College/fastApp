#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import json
import os

# import framework
from fastapi import APIRouter, Body, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor
import time
# import other server
from src.model.public.log_model import LogModel
from src.model.public.return_info import ReturnCode, ReturnInfo
from src.tools.public.config_tools import ConfigTools
from src.tools.public.datatime_tools.datatime_tools import DatetimeTools
from src.tools.public.log_tools.log_tools import LogTools
from src.tools.public.io_tools.io_tools import IOTools
from src.tools.public.script_tools.script_tools import ScriptTools
from src.tools.public.user_system_tools.user_folder_tools.user_folder_tools import UserFolderTools
from src.tools.public.user_system_tools.user_info_tools.user_info_tools import UserInfoTools
from src.tools.public.user_system_tools.user_registered_tools.user_registered_tools import UserRegisteredTools
from src.tools.public.user_system_tools.user_loading_tools.user_loading_tools import UserLoadingTools
from src.model.public.user_info import UserInfo

router = APIRouter()

# 定义任务函数
def task(name):
    print(f"{name} 开始")
    time.sleep(2)
    log_info = f"{name}: Test thread pool server"
    LogTools().write_log(log=LogModel(log_info, "INFO"))
    time.sleep(2)
    log_info = f"{name}: Test thread pool server"
    LogTools().write_log(log=LogModel(log_info, "INFO"))
    time.sleep(2)
    log_info = f"{name}: Test thread pool server"
    LogTools().write_log(log=LogModel(log_info, "INFO"))
    time.sleep(2)
    log_info = f"{name}: Test thread pool server"
    LogTools().write_log(log=LogModel(log_info, "INFO"))
    time.sleep(2)
    log_info = f"{name}: Test thread pool server"
    LogTools().write_log(log=LogModel(log_info, "INFO"))
    print(f"{name} 结束")

@router.post("/test_thread_pool_server")
def test_thread_pool(user_info: UserInfo = Body(...)):
    
    operation_name = "test_thread_pool_server"
    dt_bot = DatetimeTools()
    log_info = f"Test thread pool server"
    LogTools().write_log(log=LogModel(log_info, "INFO"))
    
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(task, "任务1")
        executor.submit(task, "任务2")
        executor.submit(task, "任务3")
        executor.submit(task, "任务4")
     
    return_info = ReturnInfo.create(code=ReturnCode.SUCCESS,
                                    message=log_info, 
                                    data={"users": user_info.user_name})
    
    return return_info


from fastapi import BackgroundTasks, APIRouter, Body
import time


def new_task(user_info: UserInfo, operation_name: str, time_str: str):
    
    old_status = "doing"
    new_status = "done"
    user_folder_bot = UserFolderTools(user_info)
    create_status, create_file_path = user_folder_bot.create_action_file(operation_name=operation_name,
                                      time_str=time_str,
                                      status=old_status)
    if not create_status:
        return "Task failed"
    else:
        time.sleep(5)
        IOTools().write_json_to_file(file_path=create_file_path, data={"status": new_status})
    update_status, update_file_path = user_folder_bot.update_action_file(operation_name=operation_name,
                                      time_str=time_str,
                                      old_status=old_status,
                                      new_status=new_status)
    return "Task completed"


@router.post("/test_thread_pool_server_1")
def test_thread_pool_1(user_info: UserInfo = Body(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    
    operation_name = "test_thread_pool_server"
    dt_bot = DatetimeTools()
    time_str = dt_bot.get_td_str()
    log_info = f"Test thread pool server"
    LogTools().write_log(log=LogModel(log_info, "INFO"))

    # 将任务添加到后台任务列表
    background_tasks.add_task(new_task, user_info, operation_name, time_str)

    return_info = ReturnInfo.create(
        code=ReturnCode.SUCCESS,
        message=log_info, 
        data={"users": user_info.user_name}
    )
    return return_info
