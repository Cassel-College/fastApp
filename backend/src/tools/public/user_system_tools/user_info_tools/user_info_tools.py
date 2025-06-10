#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import json
import os
import subprocess

from src.model.public.log_model import LogModel
from src.tools.public.datatime_tools.datatime_tools import DatetimeTools
from src.tools.public.io_tools.io_tools import IOTools
from src.tools.public.log_tools.log_tools import LogTools
from src.tools.public.config_tools.config_tools import ConfigTools
from src.model.public.user_info import UserInfo
from src.tools.public.user_system_tools.user_folder_tools.user_folder_tools import UserFolderTools
from src.tools.public.user_system_tools.user_loading_tools.user_loading_tools import UserLoadingTools
from src.model.public.return_info import ReturnCode, ReturnInfo

class UserInfoTools():
    
    def __init__(self):
        
        self.log_server = LogTools()
        log_info = f"初始化用户系统工具"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        
        self.config_tools = ConfigTools()
        self.user_info_file_path = self.config_tools.get_user_info_file_path()
        self.user_folder_path = self.config_tools.get_user_folder_path()
    
    
    def check_user_info(self, user_info: UserInfo) -> bool:
        """
        检查用户信息
        :param user_info:
        :return:
        """
        return True
    
    def get_user_action_log_core(self, user_info: UserInfo) -> list:
        
        log_info = f"Get user: {user_info.user_name} action log ..."
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        
        my_folder_path = UserFolderTools(user_info).get_my_folder_path()
        log_info = f"Get user action log: {my_folder_path}"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        
        my_action_log_path = UserFolderTools(user_info).get_my_action_log_path()
        log_info = f"Get user action log: {my_action_log_path}"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))

        action_log = {"logs": []}
        try:
            read_result = IOTools().read_json_from_file(file_path=my_action_log_path)
            if read_result.get("return_code", 1) == 0:
                action_log = read_result.get("return_value", {})
        except Exception as e:
            log_info = f"Get user action log failed: {e}"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
        return action_log
    
    def get_user_action(self, user_info: UserInfo) -> ReturnInfo:
        
        log_info = f"Get user: {user_info.user_name} action ..."
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        
        return_result = ReturnInfo(code=ReturnCode.FAILED, message="Get user action failed", data={})
        try:
            action_log_result = self.get_user_action_log_core(user_info=user_info)
            return_result.code = ReturnCode.SUCCESS
            return_result.message = "Get user action successfully"
            return_result.data['action'] = action_log_result
        except Exception as e:
            log_info = f"Get user action failed: {e}"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
            return_result.message = f"Get user action failed: {e}"
            
        return return_result
    
    def add_user_action(self, user_info: UserInfo, action: dict) -> ReturnInfo:
        
        log_info = f"Add user: {user_info.user_name} action ..."
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        # now_datetime = DatetimeTools().get_now_YYYY_MM_DD_HH_MM_SS()
        # action["datetime"] = now_datetime
        # action["action_name"] = "test"
        return_result = ReturnInfo(code=ReturnCode.FAILED, message="Add user action failed", data={})
        try:
            action_log_result = self.get_user_action_log_core(user_info=user_info)
            # print(json.dumps(action_log_result, indent=4))
            # print(type(action_log_result))
            action_log_result["logs"].append(action)
            # print(json.dumps(action_log_result, indent=4))
            my_action_log_path = UserFolderTools(user_info).get_my_action_log_path()
            log_info = f"Get user action log: {my_action_log_path}"
            self.log_server.write_log(log=LogModel(log_info, "INFO"))
            IOTools().write_json_to_file(file_path=my_action_log_path, data=action_log_result)
            return_result.code = ReturnCode.SUCCESS
            return_result.message = "Add user action successfully"
        except Exception as e:
            log_info = f"Add user action failed: {e}"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
            return_result.message = f"Add user action failed: {e}"
        return return_result
    
    def check_user_operation(self, user_info: UserInfo, operation_name: str) -> ReturnInfo:
        
        td_bots = DatetimeTools()
        check_result = ReturnInfo(code=ReturnCode.FAILED, message="User operation isn't valid.", data={})
        token = user_info.token
        user_name, is_valid = UserLoadingTools().verify_token(token)
        if not is_valid:
            log_info = f"Token is invalid"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
        if user_name != user_info.user_name:
            log_info = f"User name is invalid"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
        
        log_info = f"get user: {user_info.user_name} action log"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        action_log_result = self.get_user_action_log_core(user_info=user_info)
        action_logs = action_log_result.get("logs", [])
        now_datetime = td_bots.get_now_YYYY_MM_DD_HH_MM_SS()
        
        # 获取上一次操作记录
        last_action_log = {}
        action_logs = action_logs[::-1]
        for action_log in action_logs:
            action_name = action_log.get("action_name", "")
            if action_name == operation_name:
                last_action_log = action_log
                log_info = f"Get user: {user_info.user_name} last action log: {last_action_log}"
                self.log_server.write_log(log=LogModel(log_info, "INFO"))
                break
            
        if {} == last_action_log :
            log_info = f"User {user_info.user_name} not exist last action of {operation_name}."
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
            check_result.code = ReturnCode.SUCCESS
            check_result.message = log_info
        else:
            last_action_date = last_action_log.get("datetime", "")
            action_time = self.config_tools.get_maximum_operating_time_interval()
            time_key = td_bots.compare_time_with_threshold(time1=now_datetime, time2=last_action_date, threshold_seconds=action_time)
            if time_key:
                log_info = f"User {user_info.user_name} last do [{operation_name}] at: {last_action_date}. " + \
                        f"Now is {now_datetime}, time interval is {action_time} seconds."
                self.log_server.write_log(log=LogModel(log_info, "INFO"))
                check_result.code = ReturnCode.SUCCESS
                check_result.message = log_info
            else:
                log_info = f"operation is invalid, time interval is {action_time} seconds."
                self.log_server.write_log(log=LogModel(log_info, "WARNING"))
                check_result.code = ReturnCode.FAILED
                check_result.message = log_info
        return check_result