#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import json
import os
import subprocess

from src.model.public.log_model import LogModel
from src.model.public.return_info import ReturnCode, ReturnInfo
from src.tools.public.log_tools.log_tools import LogTools
from src.tools.public.config_tools.config_tools import ConfigTools
from src.tools.public.user_system_tools.init_user_system_tools.Init_user_ysystem_tools import InitUserSystemTools
from src.tools.public.io_tools.io_tools import IOTools
from src.model.public.user_info import UserInfo
from src.tools.public.user_system_tools.user_folder_tools.user_folder_tools import UserFolderTools

class UserRegisteredTools():
    
    def __init__(self):
        self.log_server = LogTools()
        log_info = f"初始化用户注册系统工具"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        
        self.config_tools = ConfigTools()
        self.user_info_file_path = self.config_tools.get_user_info_file_path()
        self.user_folder_path = self.config_tools.get_user_folder_path()
        InitUserSystemTools().run()
        
    def get_user_list(self) -> list:
        
        log_info = f"get user list; from user info file: {self.user_info_file_path}"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        user_info_result = IOTools().read_json_from_file(file_path=self.user_info_file_path)
        users = []
        if 0 == user_info_result.get("return_code", 1): 
            users = user_info_result.get("return_value", {}).get("user_list", [])
        else:
            return_value = user_info_result.get("return_value", {})
            log_info = f"Get user list failed: {return_value}"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
        log_info = f"Get users info over. user number: {len(users)}"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        return users
    
    
    def registered_user(self, user_info: UserInfo) -> ReturnInfo:
        
        log_info = f"Registered user core function: {user_info}"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        user_info.user_folder_path = os.path.join(self.user_folder_path, user_info.user_name)
        
        return_result = ReturnInfo(code=ReturnCode.SUCCESS, message="User registered successfully", data={})
        users = self.get_user_list()
        
        users_names = []
        users_ids = []
        max_id = 0
        for user in users:
            if isinstance(user, dict):
                users_names.append(user.get("user_name"))
                users_ids.append(user.get("id"))
                max_id = max(max_id, int(user.get("id")))   
        user_info.id = str(max_id + 1)
        log_info = f"Setting user id: {max_id + 1}"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        
        if user_info.user_name in users_names:
            log_info = f"User {user_info.user_name} already exists"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
            return_result.code = ReturnCode.FAILED
            return_result.message = f"User {user_info.user_name} already exists"
            return_result.data = {"user_info": user_info}
            return return_result
        else:
            user_infos = {}
            users.append(user_info.to_dict())
            user_infos["user_list"] = users
            try:
                write_result = IOTools().write_json_to_file(file_path=self.user_info_file_path, data=user_infos)
                log_info = f"Write user info to file: {self.user_info_file_path}, info: {user_infos}"
                self.log_server.write_log(log=LogModel(log_info, "INFO"))
            except Exception as e:
                log_info = f"Write user info to file failed: {self.user_info_file_path},info: {user_infos}"
                self.log_server.write_log(log=LogModel(log_info, "ERROR"))
                return_result.code = ReturnCode.FAILED
                return_result.message = f"Write user info to file failed: {self.user_info_file_path},info: {user_infos}"
                return_result.data = {"user_info": user_info}
                return return_result
            
            create_user_folder_result = self.create_user_folder(user_info=user_info)
            if create_user_folder_result.code == ReturnCode.SUCCESS:
                return_result.code = ReturnCode.SUCCESS
                return_result.message = f"User {user_info.user_name} registered successfully"
                return_result.data = {"user_info": user_info}
            else:
                return_result.code = ReturnCode.FAILED
                return_result.message = f"User {user_info.user_name} registered failed"
                return_result.data = {"user_info": user_info}
                return return_result
            
        new_users = self.get_user_list()
        new_users_ids = []
        new_users_names = []
        for user in users:
            if isinstance(user, dict):
                new_users_names.append(user.get("user_name"))
                new_users_ids.append(user.get("id"))
        
        if user_info.user_name in new_users_ids:
            log_info = f"New User {user_info.user_name} registered successfully"
            self.log_server.write_log(log=LogModel(log_info, "INFO"))
            return_result.code = ReturnCode.SUCCESS
            return_result.message = f"User {user_info.user_name} registered successfully"
            return_result.data = {"user_info": user_info}
        else:
            log_info = f"User {user_info.user_name} registered failed"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
            return_result.code = ReturnCode.FAILED
            return_result.message = f"User {user_info.user_name} registered failed"
            return_result.data = {"user_info": user_info}
        return return_result
        
    
    
    def create_user_folder(self, user_info: UserInfo) -> ReturnInfo:
        
        log_info = f"Create user folder: {user_info.user_name}"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        user_folder_path = os.path.join(self.user_folder_path, user_info.user_name)
        try:
            create_user_folder_result = UserFolderTools(user_info=user_info).create_user_folder(user_info=user_info)
            if create_user_folder_result:
                log_info = f"User folder created successfully: {user_folder_path}"
                self.log_server.write_log(log=LogModel(log_info, "INFO"))
                user_info.user_folder_path = user_folder_path
                return ReturnInfo(code=ReturnCode.SUCCESS, message="User folder created successfully", data={"user_info": user_info})
            else:
                log_info = f"User folder created failed: {user_folder_path}"
                self.log_server.write_log(log=LogModel(log_info, "ERROR"))
                return ReturnInfo(code=ReturnCode.FAILED, message=f"User folder created failed: {user_folder_path}", data={})   
        except Exception as e:
            log_info = f"Create user folder failed: {e}"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
            return ReturnInfo(code=ReturnCode.FAILED, message=f"Create user folder failed: {e}", data={})
        
    
