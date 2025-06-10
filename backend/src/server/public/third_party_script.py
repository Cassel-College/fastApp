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
from src.tools.public.log_tools.log_tools import LogTools
from src.tools.public.io_tools.io_tools import IOTools
from src.tools.public.script_tools.script_tools import ScriptTools


router = APIRouter()

class ScriptInput(BaseModel):
    input_info: str

@router.post("/exec_script")
def exec_third_party_script(input: ScriptInput = Body(...)):
    
    log_server = LogTools()
    config = ConfigTools()
    
    scripy_name = "script.py"
    scripy_folder = config.get_source_folder_path()
    script_file_abs_path = os.path.join(scripy_folder, scripy_name)
    log_info = f"Generate third party script: {script_file_abs_path}."
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    if not os.path.exists(script_file_abs_path):
        log_info = f"Third party script not exist! script_file_abs_path: {script_file_abs_path}."
        log_server.write_log(log=LogModel(log_info, "ERROR"))
        return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                        message=log_info, 
                                        data={"return_value": ""})
        return return_info
    input = input.input_info
    log_info = f"Third party script input info: {input}."
    log_server.write_log(log=LogModel(log_info, "INFO"))
    python_script_tools = ScriptTools()
    script_output = ""
    try:
        script_output = python_script_tools.run_script(script_file_abs_path, input)
    except Exception as e:
        log_info = f"Exec third party script failed: {e}"
        log_server.write_log(log=LogModel(log_info, "ERROR"))
        return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                        message=log_info, 
                                        data={"return_value": script_output})
        return return_info
    log_info = f"Third party script output: {script_output}."
    log_server.write_log(log=LogModel(log_info, "INFO"))
    log_info = f"Exec third party script success."
    return_info = ReturnInfo.create(code=ReturnCode.SUCCESS,
                                        message=log_info, 
                                        data={"return_value": script_output})
    return return_info
    


@router.post("/update_script")
def update_third_party_script(input: ScriptInput = Body(...)):
    
    log_server = LogTools()
    config = ConfigTools()
    io_tools = IOTools()
    
    scripy_name = "script.py"
    scripy_folder = config.get_source_folder_path()
    script_file_abs_path = os.path.join(scripy_folder, scripy_name)
    log_info = f"Generate third party script: {script_file_abs_path}."
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    if not os.path.exists(script_file_abs_path):
        log_info = f"Third party script not exist! Create third party script: script_file_abs_path: {script_file_abs_path}."
        io_tools.create_file(script_file_abs_path)
    else:
        log_info = f"Third party script exist! script_file_abs_path: {script_file_abs_path}."
        log_server.write_log(log=LogModel(log_info, "INFO"))
        
    if not os.path.exists(script_file_abs_path):
        log_info = f"Create third party script failed! Third party script not exist! script_file_abs_path: {script_file_abs_path}."
        log_server.write_log(log=LogModel(log_info, "ERROR"))
        return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                        message=log_info, 
                                        data={"script_file_abs_path": script_file_abs_path})
        return return_info
    
    new_script = input.input_info
    log_info = f"Third party script input info: {new_script}."
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    python_script_tools = ScriptTools()
    update_status = False
    try:
        update_status = python_script_tools.update_script(script_file_abs_path, new_script)
    except Exception as e:
        log_info = f"Exec third party script failed: {e}"
        log_server.write_log(log=LogModel(log_info, "ERROR"))
        return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                        message=log_info, 
                                        data={"update_status": update_status})
        return return_info
    log_info = f"Third party script update status: {update_status}."
    log_server.write_log(log=LogModel(log_info, "INFO"))
    log_info = f"Exec third party script success."
    return_info = ReturnInfo.create(code=ReturnCode.SUCCESS,
                                        message=log_info, 
                                        data={"update_status": update_status})
    return return_info
    
    
@router.get("/get_script")
def get_third_party_script():
    
    log_server = LogTools()
    config = ConfigTools()
    io_tools = IOTools()
    
    scripy_name = "script.py"
    scripy_folder = config.get_source_folder_path()
    script_file_abs_path = os.path.join(scripy_folder, scripy_name)
    log_info = f"Generate third party script: {script_file_abs_path}."
    log_server.write_log(log=LogModel(log_info, "INFO"))
    

    if not os.path.exists(script_file_abs_path):
        log_info = f"Create third party script failed! Third party script not exist! script_file_abs_path: {script_file_abs_path}."
        log_server.write_log(log=LogModel(log_info, "ERROR"))
        return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                        message=log_info, 
                                        data={"script_file_abs_path": script_file_abs_path})
        return return_info
    
    python_script_tools = ScriptTools()
    script_info = ""
    try:
        script_info = python_script_tools.get_script(script_file_abs_path)
    except Exception as e:
        log_info = f"Exec third party script failed: {e}"
        log_server.write_log(log=LogModel(log_info, "ERROR"))
        return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                        message=log_info, 
                                        data={"script_info": script_info})
        return return_info
    log_info = f"Third party script info: {script_info}."
    log_server.write_log(log=LogModel(log_info, "INFO"))
    log_info = f"Exec third party script success."
    return_info = ReturnInfo.create(code=ReturnCode.SUCCESS,
                                        message=log_info, 
                                        data={"script_info": script_info})
    return return_info