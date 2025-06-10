#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import json
import os

# import framework
from fastapi import BackgroundTasks, APIRouter, Body, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request
from pydantic import BaseModel
import time
# import other server
from src.model.private.scene_model import Scene
from src.model.public.log_model import LogModel
from src.model.public.return_info import ReturnCode, ReturnInfo
from src.model.public.user_info import UserInfo
from src.tools.private.scena_tools.scena_tools import ScenaTools
from src.tools.public.config_tools import ConfigTools
from src.tools.public.datatime_tools.datatime_tools import DatetimeTools
from src.tools.public.gpt_tools.gpt_tools import GPTAPI
from src.tools.public.io_tools.io_tools import IOTools
from src.tools.public.log_tools.log_tools import LogTools

from src.tools.public.gmini_tools.gmini_tools import GeminiAPI
from src.tools.private.policy_file_tools.policy_file_tools import PolicyFileTools
from src.tools.private.prompt_tools.prompt_tools import PromptTools

from src.server.public.agent_server import GPT, gmini_agent
from src.tools.public.user_system_tools.user_folder_tools.user_folder_tools import UserFolderTools
from src.tools.public.user_system_tools.user_info_tools.user_info_tools import UserInfoTools
from src.tools.public.user_system_tools.user_loading_tools.user_loading_tools import UserLoadingTools

router = APIRouter()

class GEN_INPUT(BaseModel):
    background: str
    scenarios: dict
    replenish: str
    robot_type: str
    gpt_type: str
    api_key: str
    gpt_model: str
    user_name: str
    token: str


def gen_full_scenarios_core(scenarios_input: dict, background: str, replenish: str, gen_node: GEN_INPUT):
    
    log_server = LogTools()
    config = ConfigTools()
    io_tools = IOTools()
    scena_tools = ScenaTools(codes=[], scenarios_info=[])
    markdown_report = ""
    all_answers = ""
    if True:
        log_info = f"Start gen full scenarios ..."
        log_server.write_log(log=LogModel(log_info, "INFO"))
        scena_scplify_scenarios = "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        for scenarios_name, simplify_scenarios_item in scenarios_input.items():
            print(f"{scenarios_name}: {simplify_scenarios_item}")
            prompt = PromptTools().gen_full_scenarios_prompt(
                background=background,
                simplify_scenarios_data=simplify_scenarios_item,
                replenish=replenish)
            log_info = f"My prompt: {prompt}"
            log_server.write_log(log=LogModel(log_info, "INFO"))
            markdown_report = markdown_report + f"### {scenarios_name}\n" + prompt + "\n"
            full_scenarios_info = gmini_agent(gpt=GPT(
                text=prompt,
                robot_type=gen_node.robot_type,
                gpt_type=gen_node.gpt_type,
                api_key=gen_node.api_key,
                gpt_model=gen_node.gpt_model))
        
            if full_scenarios_info.code != ReturnCode.SUCCESS:
                return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                                message=full_scenarios_info.message, 
                                                data={})
            else:
                gemini_api = GeminiAPI(api_key="", model="")
                log_info = f"Full scenarios info: {json.dumps(full_scenarios_info.data, ensure_ascii=False, indent=4)}"
                log_server.write_log(log=LogModel(log_info, "INFO"))
                gpt_api = GPTAPI(
                    gpt_type=gen_node.gpt_type,
                    api_key=gen_node.api_key,
                    model=gen_node.gpt_model)
                gpt_bot = gpt_api.gen_bot()
                answers = gpt_bot.extract_answers_all(full_scenarios_info.data)
                answers = answers.replace("```python", "").replace("```json", "").replace("```markdown", "")
                answers = answers.replace("```", "")
                all_answers = all_answers + f"## {scenarios_name}" + "\n\n"
                all_answers = all_answers + answers + f"\n{scena_scplify_scenarios}\n"
        s_split = scena_scplify_scenarios
        e_split = '*********'
        ns = scena_tools.split_test_items(input_data=all_answers, s_split=s_split, e_split=e_split)
        print(json.dumps(ns, ensure_ascii=False, indent=4))
        return ns
    
def async_gen_full_scenarios_core(
    user_info: UserInfo, 
    operation_name: str,
    time_str: str,
    scenarios_input: dict,
    background: str,
    replenish: str,
    gen_node: GEN_INPUT):
    
    
    log_server = LogTools()
    log_info = f"Start async gen full scenarios ..."
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    old_status = "doing"
    new_status = "done"
    user_folder_bot = UserFolderTools(user_info)
    create_status, create_file_path = user_folder_bot.create_action_file(operation_name=operation_name,
                                      time_str=time_str,
                                      status=old_status)
    
    ns = gen_full_scenarios_core(scenarios_input=scenarios_input, background=background, replenish=replenish, gen_node=gen_node)
    IOTools().write_json_to_file(file_path=create_file_path, data=ns)
    
    update_status, update_file_path = user_folder_bot.update_action_file(operation_name=operation_name,
                                      time_str=time_str,
                                      old_status=old_status,
                                      new_status=new_status)
    log_info = f"Async gen full scenarios Over!"
    log_server.write_log(log=LogModel(log_info, "INFO"))
    return ns

@router.post("/gen_full_scenarios")
def gen_full_scenarios(gen_node: GEN_INPUT = Body(...),
                       background_tasks: BackgroundTasks = BackgroundTasks()):
    
    log_server = LogTools()
    config = ConfigTools()
    io_tools = IOTools()
    scena_tools = ScenaTools(codes=[], scenarios_info=[])
    background = gen_node.background
    scenarios_input = gen_node.scenarios
    replenish = gen_node.replenish
    policy_name = "scenarios.json"
    operation_name = "gen_full_scenarios"
    async_key = True
    new_version = True
    dt_bot = DatetimeTools()
    time_str = dt_bot.get_td_str()
    
    user_info = UserInfo(id="",user_name=gen_node.user_name, token=gen_node.token, user_password="", user_folder_path="")
    
    policy_folder = config.get_source_folder_path()
    policy_file_abs_path = os.path.join(policy_folder, policy_name)
    
    if not io_tools.check_target_file_exist(policy_file_abs_path):
        log_server.write_log(log=LogModel(f"Scenarios file not exist! and Con't build scenarios list.", "ERROR"))
        return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                        message=f"Target policy not exist! policy_file_abs_path: {policy_file_abs_path}.", 
                                        data={"policy_name": policy_name})
        return return_info
    else:
        log_info = f"Scenarios file exist! policy_file_abs_path: {policy_file_abs_path}."
        log_server.write_log(log=LogModel(log_info, "INFO"))
        
        policy_file_tools = PolicyFileTools(policy_file_abs_path=policy_file_abs_path)
        scenarios_info = policy_file_tools.get_policy_info_as_json()
        
        if scenarios_info.code != ReturnCode.SUCCESS:
            return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                            message=scenarios_info.message, 
                                            data={})
            log_server.write_log(log=LogModel(f"Get scenarios data failed! and Con't build scenarios list.", "ERROR"))
            return return_info
        else:
            scenarios_data = scenarios_info.data
            simplify_scenarios_data = policy_file_tools.simplify_scenarios(data=scenarios_data)
            print(simplify_scenarios_data)
    
    print(f"type(scenarios): {type(scenarios_input)}")
    # print(scenarios)
    # background = "关注自车在低速拥挤路段与行人的交互"
    markdown_report = ""
    all_answers = ""
    
    UserInfoTools().add_user_action(user_info=user_info, action={"action_name": operation_name, "datetime": time_str})
    if async_key:
        log_info = f"Start async gen full scenarios ..."
        
        background_tasks.add_task(async_gen_full_scenarios_core, user_info, operation_name, time_str, scenarios_input, background, replenish, gen_node)
        
        return_info = ReturnInfo.create(code=ReturnCode.SUCCESS,
                                        message=log_info, 
                                        data={"answers": []})
        return return_info
    else:
        if new_version:
            ns = gen_full_scenarios_core(scenarios_input=scenarios_input, background=background, replenish=replenish, gen_node=gen_node)
        else:
            log_info = f"Start gen full scenarios ..."
            log_server.write_log(log=LogModel(log_info, "INFO"))
            scena_scplify_scenarios = "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
            for scenarios_name, simplify_scenarios_item in scenarios_input.items():
                print(f"{scenarios_name}: {simplify_scenarios_item}")
                prompt = PromptTools().gen_full_scenarios_prompt(
                    background=background,
                    simplify_scenarios_data=simplify_scenarios_item,
                    replenish=replenish)
                log_info = f"My prompt: {prompt}"
                log_server.write_log(log=LogModel(log_info, "INFO"))
                markdown_report = markdown_report + f"### {scenarios_name}\n" + prompt + "\n"
                full_scenarios_info = gmini_agent(gpt=GPT(
                    text=prompt,
                    robot_type=gen_node.robot_type,
                    gpt_type=gen_node.gpt_type,
                    api_key=gen_node.api_key,
                    gpt_model=gen_node.gpt_model))
            
                if full_scenarios_info.code != ReturnCode.SUCCESS:
                    return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                                    message=full_scenarios_info.message, 
                                                    data={})
                else:
                    gemini_api = GeminiAPI(api_key="", model="")
                    log_info = f"Full scenarios info: {json.dumps(full_scenarios_info.data, ensure_ascii=False, indent=4)}"
                    log_server.write_log(log=LogModel(log_info, "INFO"))
                    gpt_api = GPTAPI(
                        gpt_type=gen_node.gpt_type,
                        api_key=gen_node.api_key,
                        model=gen_node.gpt_model)
                    gpt_bot = gpt_api.gen_bot()
                    answers = gpt_bot.extract_answers_all(full_scenarios_info.data)
                    answers = answers.replace("```python", "").replace("```json", "").replace("```markdown", "")
                    answers = answers.replace("```", "")
                    all_answers = all_answers + f"## {scenarios_name}" + "\n\n"
                    all_answers = all_answers + answers + f"\n{scena_scplify_scenarios}\n"
            s_split = scena_scplify_scenarios
            e_split = '*********'
            ns = scena_tools.split_test_items(input_data=all_answers, s_split=s_split, e_split=e_split)
        print(json.dumps(ns, ensure_ascii=False, indent=4))
    
    return_info = ReturnInfo.create(code=ReturnCode.SUCCESS,
                                            message="", 
                                            data={"answers": ns})
    return return_info


@router.post("/update_full_scenarios")
def update_full_scenarios(gen_node: GEN_INPUT = Body(...)):
    
    log_server = LogTools()
    config = ConfigTools()
    io_tools = IOTools()
    scena_tools = ScenaTools(codes=[], scenarios_info=[])
    background = gen_node.background
    scenarios_input = gen_node.scenarios
    print(f"type(scenarios): {type(scenarios_input)}")
    print(scenarios_input)
    md_str = scenarios_input.get("md_str", "")
    replenish = gen_node.replenish
    
    async_key = False
    
    prompt = PromptTools().update_full_scenarios_prompt(
        background=background,
        scenarios_data=md_str,
        replenish=replenish)
    print(prompt)
    full_scenarios_info = gmini_agent(gpt=GPT(
        text=prompt,
        robot_type=gen_node.robot_type,
        gpt_type=gen_node.gpt_type,
        api_key=gen_node.api_key,
        gpt_model=gen_node.gpt_model))
    
    if full_scenarios_info.code != ReturnCode.SUCCESS:
        return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                        message=full_scenarios_info.message, 
                                        data={})
    else:
        if async_key:
            log_info = f"Start async update full scenarios ..."
            
            return_info = ReturnInfo.create(code=ReturnCode.SUCCESS,
                                            message=log_info, 
                                            data={"new_node": new_node})
        else:
            # gemini_api = GeminiAPI(api_key="", model="")
            gpt_api = GPTAPI(
                gpt_type=gen_node.gpt_type,
                api_key=gen_node.api_key,
                model=gen_node.gpt_model)
            gpt_bot = gpt_api.gen_bot()
            # print(full_scenarios_info.data)
            print(json.dumps(full_scenarios_info.data, ensure_ascii=False, indent=4))
            answers = gpt_bot.extract_answers_all(full_scenarios_info.data)
            answers = answers.replace("```python", "").replace("```json", "").replace("```markdown", "")
            answers = answers.replace("```", "")
            s_split = "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
            e_split = '*********'
            ns = scena_tools.split_test_items(input_data=answers, s_split=s_split, e_split=e_split)
            print(json.dumps(ns, ensure_ascii=False, indent=4))
            new_node = {}
            for item in ns:
                if "node_type" in item and item["node_type"] == "md":
                    new_node = item
                    break
            new_node["node_index"] = scenarios_input.get("node_index", 0)
            return_info = ReturnInfo.create(code=ReturnCode.SUCCESS,
                                                    message="", 
                                                    data={"new_node": new_node})
    return return_info

@router.post("/get_md_full_scenarios_from_cloud")
def get_md_from_cloud(gen_node: GEN_INPUT = Body(...)):
    
    log_server = LogTools()
    user_loading_tools = UserLoadingTools()
    user_info_tools = UserInfoTools()
    dt_tools = DatetimeTools()
    operation_name = "get_md_full_scenarios_from_cloud"
    target_action_name = "gen_full_scenarios"
    now_dts = dt_tools.get_now_YYYY_MM_DD_HH_MM_SS()
    
    log_info = f"Begin {operation_name} ..."
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    log_info = f"params: {json.dumps(gen_node.dict(), ensure_ascii=False, indent=4)}"
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    log_info = f"Begin check user token ..."
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    token = gen_node.token
    user_name_ = gen_node.user_name
    user_info = UserInfo(id="",user_name=user_name_, token=token, user_password="", user_folder_path="")
    
    user_name, is_valid = user_loading_tools.verify_token(token)
    if not is_valid:
        log_info = f"User: {user_name_}'s token is invalid: token: {token}"
        log_server.write_log(log=LogModel(log_info, "ERROR"))
        return_info = ReturnInfo.create(
            code=ReturnCode.FAILED, message = log_info, data={})
        return return_info
    else:
        log_info = f"User: {user_name_}'s token is valid: token: {token}"
        log_server.write_log(log=LogModel(log_info, "INFO"))
    if user_name != user_name_:
        log_info = f"User name: {user_name} is invalid ."
        log_server.write_log(log=LogModel(log_info, "ERROR"))
        return_info = ReturnInfo.create(
            code=ReturnCode.FAILED, message = log_info, data={})
        return return_info
    else:
        log_info = f"User name: {user_name} is valid ."
        log_server.write_log(log=LogModel(log_info, "INFO"))
    
    user_actions_log = user_info_tools.get_user_action_log_core(user_info=user_info)
    user_actions = user_actions_log["logs"]
    user_actions.reverse()
    has_target_action = False
    action_dt = ""
    for action in user_actions:
        action_name = action.get("action_name", "")
        if action_name == target_action_name:
            action_dt = action.get("datetime", "")
            log_info = f"Find last user action: {action_name} at {action_dt}"
            log_server.write_log(log=LogModel(log_info, "INFO"))
            has_target_action = True
            break
        
    if not has_target_action:
        log_info = f"Can't find last user action: {target_action_name}"
        log_server.write_log(log=LogModel(log_info, "ERROR"))
        return_info = ReturnInfo.create(
            code=ReturnCode.FAILED, message = log_info, data={})
        return return_info
    
    log_info = f"Begin check action: {target_action_name} time ..."
    log_server.write_log(log=LogModel(log_info, "INFO"))
    action_dt = dt_tools.str_to_datetime_str(action_dt)
    validity = not dt_tools.compare_time_with_threshold(time1=now_dts, time2=action_dt, threshold_seconds=60 * 60 * 24 * 60)
    log_info = f"Action: {target_action_name} last doing datetime: {action_dt}; now datetime: {now_dts}. ststus: {str(validity)}"
    log_server.write_log(log=LogModel(log_info, "INFO"))
    
    if not validity:
        log_info = f"Action: {target_action_name} time is invalid. Please do it again."
        log_server.write_log(log=LogModel(log_info, "ERROR"))
        return_info = ReturnInfo.create(
            code=ReturnCode.FAILED, message = log_info, data={})
        return return_info
    
    user_folder_tools = UserFolderTools(user_info=user_info)
    action_dt_str = dt_tools.td2str(dt=action_dt)
    file_name = user_folder_tools.get_my_target_action_file_name(operation_name=target_action_name, time_str=action_dt_str)
    file_satatus = user_folder_tools.get_my_target_action_file_status(operation_name=target_action_name, time_str=action_dt_str)
    if file_satatus == "doing":
        log_info = f"Action: {target_action_name} is doing now. Please wait a moment."
        log_server.write_log(log=LogModel(log_info, "INFO"))
        return_info = ReturnInfo.create(
            code=ReturnCode.FAILED, message=log_info, data={})
        return return_info
    if file_satatus == "":
        log_info = f"Action: {target_action_name} ERROR. Please do it again.."
        log_server.write_log(log=LogModel(log_info, "ERROR"))
        return_info = ReturnInfo.create(
            code=ReturnCode.FAILED, message=log_info, data={})
        return return_info
    if file_satatus == "done":
        abs_file_path = user_folder_tools.get_my_target_action_file_abs_path(operation_name=target_action_name, time_str=action_dt_str)
        log_info = f"Action: {target_action_name} is done. file anme: {file_name}; file_path: {abs_file_path}"
        log_server.write_log(log=LogModel(log_info, "INFO"))
        
        target_log_info = user_folder_tools.get_my_target_action_file_content(abs_file_path=abs_file_path)
        if isinstance(target_log_info, dict):
            answers = target_log_info.get('return_value', [])
            return_info = ReturnInfo.create(
                code=ReturnCode.SUCCESS, message="", data={"answers": answers})
            return return_info
        else:
            log_info = f"Action: {target_action_name} get file content failed. Please generation it again.."
            log_server.write_log(log=LogModel(log_info, "ERROR"))
            return_info = ReturnInfo.create(
                code=ReturnCode.FAILED, message=log_info, data={})
            return return_info

    return_info = ReturnInfo.create(code=ReturnCode.SUCCESS,
                                                    message="", 
                                                    data={})
    return return_info