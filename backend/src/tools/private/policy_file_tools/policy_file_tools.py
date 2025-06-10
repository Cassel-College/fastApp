#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import json
import os

from src.model.public.log_model import LogModel
from src.tools.public.io_tools.io_tools import IOTools
from src.tools.public.log_tools.log_tools import LogTools
from src.model.public.return_info import ReturnCode, ReturnInfo


class PolicyFileTools:
    
    def __init__(self, policy_file_abs_path: str=None):
        
        self.policy_file_abs_path = policy_file_abs_path
        self.log_server = LogTools()
        self.io_tools = IOTools()
    
    def get_policy_info(self) -> ReturnInfo:
        
        if not self.io_tools.check_target_file_exist(self.policy_file_abs_path):
            return_info = ReturnInfo.create(
                code=ReturnCode.FAILED,
                message=f"Target policy not exist! file path: {self.policy_file_abs_path}.", 
                data={})
            self.log_server.write_log(
                log=LogModel(f"Target policy not exist! policy_file_abs_path: {self.policy_file_abs_path}.", "ERROR"))
        else:
            if self.policy_file_abs_path.endswith(".json"):
                data = self.io_tools.read_json_from_file(self.policy_file_abs_path)
                policy_file_data = data.get("return_value", {})
            else:
                data = self.io_tools.read_list_from_file(self.policy_file_abs_path)
                policy_file_data = data.get("return_value", [])
            if isinstance(data, dict) and "return_code" in data.keys() and data["return_code"] == 0:
                return_info = ReturnInfo.create(
                    code=ReturnCode.SUCCESS, 
                    message=f"Read target policy success! file path: {self.policy_file_abs_path}.", 
                    data=policy_file_data)
                self.log_server.write_log(
                    log=LogModel(f"Read target policy success! policy_file_abs_path: {self.policy_file_abs_path}.", "INFO"))
            else:
                return_info = ReturnInfo.create(
                    code=ReturnCode.FAILED, 
                    message=f"Read target policy failed! file path: {self.policy_file_abs_path}.", 
                    data={})
                self.log_server.write_log(
                    log=LogModel(f"Read target policy failed! policy_file_abs_path: {self.policy_file_abs_path}.", "ERROR"))
        return return_info
        
    def get_policy_info_as_json(self) -> ReturnInfo:
        
        self.log_server.write_log(log=LogModel(f"get policy info as json:", "INFO"))
        return self.get_policy_info()
    
    def get_policy_info_as_list(self) -> ReturnInfo:
        
        self.log_server.write_log(log=LogModel(f"get policy info as list:", "INFO"))
        return self.get_policy_info()
    
    def get_scenarios_info_as_list(self) -> ReturnInfo:

        policy_data = self.get_policy_info_as_json()
        
        if policy_data.code != ReturnCode.SUCCESS and isinstance(policy_data.data, dict):
            log_info = f"Get scenarios info failed! and return empty list."
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
            return_info = ReturnInfo.create(code=ReturnCode.FAILED, message=log_info, data=[])
        else:
            if "scenarios" in policy_data.data.keys():
                log_info = f"Get scenarios info success!"
                self.log_server.write_log(log=LogModel(log_info, "INFO"))
                scenarios_info = policy_data.data.get("scenarios", [])
                return_info = ReturnInfo.create(code=ReturnCode.SUCCESS, message=log_info, data=scenarios_info)
            else:
                log_info = f"Get scenarios info failed! and return empty list."
                self.log_server.write_log(log=LogModel(log_info, "ERROR"))
                return_info = ReturnInfo.create(code=ReturnCode.FAILED, message=log_info, data=[])
        return return_info
    
    

    def simplify_scenarios(self, data: dict) -> dict:
        """
        将复杂的场景数据转化为分组简化的格式。
        
        :param data: 包含场景数据的 JSON 对象
        :return: 转化后的字典
        """
        result = {}

        # 遍历所有场景
        for scenario in data.get('scenarios', []):
            group_name = scenario['group_name']
            label_name = scenario['label_name']
            
            # 按组名分类收集 label_name
            if group_name not in result:
                result[group_name] = []
            result[group_name].append(label_name)

        # 返回简化的字典
        return result
