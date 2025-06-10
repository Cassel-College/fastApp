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
from src.tools.private.policy_file_tools.policy_file_tools import PolicyFileTools
from src.tools.private.scena_tools.scena_tools import ScenaTools
from src.tools.public.config_tools import ConfigTools
from src.tools.public.io_tools.io_tools import IOTools
from src.tools.public.log_tools.log_tools import LogTools


router = APIRouter()


class ScenaCodes(BaseModel):
    codes: list
    policy_name: str
    old_scenarios: dict


@router.post("/gen_scene_list")
def gen_gen_scena_list(request: ScenaCodes = Body(...)):

    log_server = LogTools()
    config = ConfigTools()
    io_tools = IOTools()
    
    log_server.write_log(log=LogModel(f"Gen scene list.", "INFO"))
    
    codes = request.codes
    policy_name = request.policy_name
    old_scenarios = request.old_scenarios
    
    log_server.write_log(log=LogModel(f"Target policy name: {policy_name}.", "INFO"))
    log_server.write_log(log=LogModel(f"Scene codes: {codes}.", "INFO"))
    
    scenarios_data = []
    
    policy_folder = config.get_source_folder_path()
    policy_file_abs_path = os.path.join(policy_folder, policy_name)
    
    policy_file_tools = PolicyFileTools(policy_file_abs_path=policy_file_abs_path)
    scenarios_info = policy_file_tools.get_scenarios_info_as_list()
    
    if scenarios_info.code != ReturnCode.SUCCESS:
        return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                        message=scenarios_info.message, 
                                        data={})
        log_server.write_log(log=LogModel(f"Get target scenarios_info failed!", "ERROR"))
        return return_info
    
    scenarios_data = scenarios_info.data
    scena_tools = ScenaTools(codes=codes, scenarios_info=scenarios_data)
    
    # target_scenarios_info = scena_tools.gen_scena_list_by_codes()
    target_scenarios_info = scena_tools.gen_simple_scena_list_by_codes()
    simple_scena_list = target_scenarios_info.data.get("scena_list", [])
    print(simple_scena_list)
    simple_scena_as_dicts = convert_data(input_data=simple_scena_list)
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print(simple_scena_as_dicts)
    table_data = scena_tools.gen_table_data(simple_scena_list=simple_scena_list)
    # print(table_data)
    
    print(f"old_scenarios type: {str(type(old_scenarios))}")
    if type(old_scenarios) == dict:
        print(json.dumps(old_scenarios, ensure_ascii=False, indent=4))
        log_info = f"Merge old_scenarios and rule simple_scena_as_dicts. old_scenarios number: {len(old_scenarios)}; rule simple_scena_as_dicts number: {len(simple_scena_as_dicts)}."
        log_server.write_log(log=LogModel(log_info, "INFO"))
        simple_scena_as_dicts = scena_tools.merge_dicts(old_scenarios, simple_scena_as_dicts)
    else:
        log_info = f"Can't merge old_scenarios and rule simple_scena_as_dicts. Only return new rule simple_scena old_scenarios type: {str(type(old_scenarios))}; typy data: {old_scenarios}."
        log_server.write_log(log=LogModel(log_info, "WARNING"))
    
    if target_scenarios_info.code != ReturnCode.SUCCESS:
        return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                        message=target_scenarios_info.message, 
                                        data={})
        log_server.write_log(log=LogModel(f"Gen scene list failed!", "ERROR"))
        return return_info
    else:
        # scena_list = target_scenarios_info.data
        return_date = {
            "table_data": table_data,
            "scena_list": simple_scena_list,
            "scena_as_dicts": simple_scena_as_dicts
        }
        return_info = ReturnInfo.create(code=ReturnCode.SUCCESS, 
                                        message="Gen scene list success!", 
                                        data=return_date)
    return return_info

# 转换函数
def convert_data(input_data: list):
    output = {}
    for index, entry in enumerate(input_data, start=1):
        scena_name = f"scena{index}"
        scenario = {item['group_name']: item['label_name'] for item in entry}
        output[scena_name] = scenario
    return output

# # 执行转换
# converted_data = convert_data(data)

# # 转换为 JSON 格式并输出
# print(json.dumps(converted_data, ensure_ascii=False, indent=4))
