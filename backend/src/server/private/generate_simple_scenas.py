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
from src.model.public.user_info import UserInfo
from src.tools.public.user_system_tools.user_info_tools.user_info_tools import UserInfoTools
router = APIRouter()

class GPT_INPUT(BaseModel):
    background: str
    robot_type: str
    old_scenarios: dict
    gpt_type: str
    api_key: str
    gpt_model: str
    user_name: str
    token: str


@router.post("/gen_simplify_scenarios")
def gen_simplify_scenarios(gpt: GPT_INPUT = Body(...)):
    
    print(gpt)
    log_server = LogTools()
    config = ConfigTools()
    io_tools = IOTools()
    policy_name = "scenarios.json"
    background = gpt.background
    old_scenarios = gpt.old_scenarios
    simplify_scenarios_data = {}
    operation_name = "gen_simplify_scenarios"
    
    user_info = UserInfo(id="", user_name=gpt.user_name, user_password="", token=gpt.token, user_folder_path="")
    datetime_bot = DatetimeTools()
    now = datetime_bot.get_now_YYYY_MM_DD_HH_MM_SS()
    user_bot = UserInfoTools()
    
    do_operation_status = False
    try:
        check_user_operation_result = UserInfoTools().check_user_operation(
            user_info=user_info, 
            operation_name=operation_name)
        if check_user_operation_result.code == ReturnCode.SUCCESS:
            do_operation_status = True
            action = {"action_name": operation_name, "datetime": datetime_bot.get_now_YYYY_MM_DD_HH_MM_SS()}
            add_actions_result = UserInfoTools().add_user_action(user_info=user_info, action=action)
        else:
            log_info = f"User {user_info.user_name} operation: check get_user_actions failed."
            log_server.write_log(log=LogModel(log_info, "ERROR"))
            # user_actions_result.message = check_user_operation_result.message
    except Exception as e:
        log_info = f"User {user_info.user_name} operation: get_user_actions failed: {e}"
        log_server.write_log(log=LogModel(log_info, "ERROR"))
        # user_actions_result.message = f"User {user_info.user_name} operation: get_user_actions failed: {e}"
            
    if not do_operation_status:
        return_info = ReturnInfo.create(code=ReturnCode.SUCCESS,
                                        message="User operation isn't valid.", 
                                        data={})
        return return_info
    else:
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
                
        # background = "关注自车在低速拥挤路段与行人的交互"
        prompt = PromptTools().gen_simplify_scenarios_prompt(background=background, simplify_scenarios_data=simplify_scenarios_data)
        
        simplify_scenarios_info = gmini_agent(gpt=GPT(
            text=prompt,
            robot_type=gpt.robot_type,
            gpt_type=gpt.gpt_type,
            api_key=gpt.api_key,
            gpt_model=gpt.gpt_model))
        
        if simplify_scenarios_info.code != ReturnCode.SUCCESS:
            return_info = ReturnInfo.create(code=ReturnCode.FAILED,
                                            message=simplify_scenarios_info.message, 
                                            data={})
        else:
            gpt_api = GPTAPI(
                gpt_type=gpt.gpt_type,
                api_key=gpt.api_key,
                model=gpt.gpt_model)
            gpt_bot = gpt_api.gen_bot()
            answers = gpt_bot.extract_answers_all(simplify_scenarios_info.data)
            answers = answers.replace("```python", "").replace("\n", "").replace("```json", "").replace("```", "")
            try:
                answers = json.loads(answers)
                print(f"answers type: {str(type(answers))}")
                
                print(f"old_scenarios type: {str(type(old_scenarios))}")
                if type(old_scenarios) == dict:
                    scena_tools = ScenaTools(codes=[], scenarios_info=[])
                    print(json.dumps(old_scenarios, ensure_ascii=False, indent=4))
                    log_info = f"Merge old_scenarios and AI simple_scena_as_dicts. old_scenarios number: {len(old_scenarios)}; AI simple_scena_as_dicts number: {len(answers)}."
                    log_server.write_log(log=LogModel(log_info, "INFO"))
                    answers = scena_tools.merge_dicts(old_scenarios, answers)
                else:
                    log_info = f"Can't merge old_scenarios and rule simple_scena_as_dicts. Only return new AI simple_scena old_scenarios type: {str(type(old_scenarios))}; typy data: {old_scenarios}."
                    log_server.write_log(log=LogModel(log_info, "WARNING"))
            except Exception as e:
                print(f"answers type: {str(type(answers))}; Error: {str(e)}")
                answers = {}
            return_info = ReturnInfo.create(code=ReturnCode.SUCCESS,
                                            message=simplify_scenarios_info.message, 
                                            data={"answers": answers})

    return return_info

    # # 替换为你的 API 密钥
    # api_key = config.get_gmini_api_key()
    # model = config.get_gmini_model_name()
    # log_info = f"Begin generate scenarios. used gpt from {model}."
    # log_server.write_log(log=LogModel(log_info, "INFO"))
    # # 初始化工具类
    # gemini_api = GeminiAPI(api_key, model=model)
    # log_info = f"Create Agent success!"
    # log_server.write_log(log=LogModel(log_info, "INFO"))
    # # 调用生成内容的方法
    # contents = [f"{prompt}"]
    # try:
    #     log_info = f"Chat with GPT: {prompt.replace('\n', '')}"
    #     log_server.write_log(log=LogModel(log_info, "INFO"))
        
    #     # result = gemini_api.generate_content(contents=contents)
    #     result = {}
    # except Exception as e:
    #     result = {"error": str(e)}
    # print("Response with default model: \n", json.dumps(result, ensure_ascii=False, indent=4))
    
    # if isinstance(result, dict) and "error" not in result.keys() and "candidates" in result.keys():
    #     answers = gemini_api.extract_answers_all(data=result)
    #     log_info = f"GPT answers: {answers.replace('\n', '')}"
    #     log_server.write_log(log=LogModel(log_info, "INFO"))
    #     return_info = ReturnInfo.create(code=ReturnCode.SUCCESS, 
    #                                 message="Agent generate success!", 
    #                                 data=result)
    # else:
    #     return_info = ReturnInfo.create(code=ReturnCode.FAILED, 
    #                                 message="Agent generate failed!", 
    #                                 data={"text": "Hello world!"})
    # return return_info