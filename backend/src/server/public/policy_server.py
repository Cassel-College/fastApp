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
from src.model.private.scene_model import Scene
from src.model.public.log_model import LogModel
from src.model.public.return_info import ReturnCode, ReturnInfo
from src.tools.public.config_tools import ConfigTools
from src.tools.public.io_tools.io_tools import IOTools
from src.tools.public.log_tools.log_tools import LogTools


router = APIRouter()


class Policy(BaseModel):
    policy_name: str


@router.post("/get_target_policy")
def get_target_policy(policy_data: Policy = Body(...)):
    
    log_server = LogTools()
    config = ConfigTools()
    io_tools = IOTools()
    
    policy_name = policy_data.policy_name
    log_server.write_log(log=LogModel(f"Target policy name: {policy_name}.", "INFO"))
    policy_folder = config.get_source_folder_path()
    policy_file_abs_path = os.path.join(policy_folder, policy_name)
    
    if not io_tools.check_target_file_exist(policy_file_abs_path):
        return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                        message=f"Target policy not exist! policy_file_abs_path: {policy_file_abs_path}.", 
                                        data={"policy_name": policy_name})
        log_server.write_log(log=LogModel(f"Target policy not exist! policy_file_abs_path: {policy_file_abs_path}.", "INFO"))
    else:
        if policy_file_abs_path.endswith(".json"):
            data = io_tools.read_json_from_file(policy_file_abs_path)
            policy_file_data = data.get("return_value", {})
        else:
            data = io_tools.read_list_from_file(policy_file_abs_path)
            policy_file_data = data.get("return_value", [])
            
        if data is None:
            return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                            message="Get target policy failed! policy_file_abs_path: {policy_file_abs_path}.", 
                                            data={"policy_name": policy_name})
        else:
            return_info = ReturnInfo.create(code=ReturnCode.SUCCESS, 
                                            message="Get target policy success!", 
                                            data=policy_file_data)
    return return_info
    
    
class SceneUpdate(BaseModel):
    scene: Scene
    policy_name: str
    
@router.post("/append_scene")
def append_policy(scene_data: SceneUpdate = Body(...)):
    
    log_server = LogTools()
    config = ConfigTools()
    io_tools = IOTools()
    
    policy_name = scene_data.policy_name
    log_server.write_log(log=LogModel(f"Target policy name: {policy_name}.", "INFO"))
    policy_folder = config.get_source_folder_path()
    policy_file_abs_path = os.path.join(policy_folder, policy_name)
    
    if not io_tools.check_target_file_exist(policy_file_abs_path):
        return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                        message=f"Target policy not exist! policy_file_abs_path: {policy_file_abs_path}.", 
                                        data={"policy_name": policy_name})
    else:
        if policy_file_abs_path.endswith(".json"):
            data = io_tools.read_json_from_file(policy_file_abs_path)
            policy_file_data = data.get("return_value", {})
        else:
            data = io_tools.read_list_from_file(policy_file_abs_path)
            policy_file_data = data.get("return_value", [])
            
        if data is None:
            return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                            message="Get target policy failed! policy_file_abs_path: {policy_file_abs_path}.", 
                                            data={"policy_name": policy_name})
        else:
            scenarios = policy_file_data.get("scenarios", [])
            log_server.write_log(log=LogModel(f"Get old scenarios, number: {str(len(scenarios))}.", "INFO"))
            max_scene_code = 0
            for scene in scenarios:
                if int(scene.get("code")) > max_scene_code:
                    max_scene_code = int(scene.get("code"))
            scenarios = policy_file_data.get("scenarios", [])
            print(f"type: {str(type(scenarios))}")
            print(type(policy_file_data["scenarios"][0]))
            print(policy_file_data["scenarios"][0])
            scene_data.scene.code = str(max_scene_code + 1)
            log_server.write_log(log=LogModel(f"Build new scene: {scene_data.scene.to_json()}.", "INFO"))
            policy_file_data["scenarios"].append(scene_data.scene.to_dict())
            log_info = f"Gen new scenarios, number: {str(len(policy_file_data['scenarios']))}."
            log_server.write_log(log=LogModel(log_info, "INFO"))
            
            # 重新写入policy_file_abs_path
            save_result = io_tools.write_target_file(target_file_path=policy_file_abs_path,
                                                     content=json.dumps(policy_file_data, ensure_ascii=False, indent=4))
            
            if save_result.code != ReturnCode.SUCCESS:
                return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                                message=save_result.message,
                                                data=save_result.data)

            return_info = ReturnInfo.create(code=ReturnCode.SUCCESS, 
                                            message="Update target policy success!", 
                                            data=policy_file_data)
    return return_info