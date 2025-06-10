#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import json
import os
import subprocess

from src.model.public.log_model import LogModel
from src.tools.public.log_tools.log_tools import LogTools
from src.tools.public.config_tools.config_tools import ConfigTools
from src.model.public.user_info import UserInfo
from src.tools.public.io_tools.io_tools import IOTools

class UserFolderTools():
    
    def __init__(self, user_info: UserInfo):
        self.log_server = LogTools()
        self.config_tools = ConfigTools()
        self.user_info_file_path = self.config_tools.get_user_info_file_path()
        self.user_folder_path = self.config_tools.get_user_folder_path()
        self.my_folder_path = os.path.join(self.user_folder_path, user_info.user_name)
        self.my_action_log_path = os.path.join(self.my_folder_path, "action_log.json")
        
    def mkdir_my_folder_path(self) -> bool:
        
        log_info = f"初始化用户文件夹工具"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        log_info = f"创建用户文件夹: {self.my_folder_path}"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        
        if not os.path.exists(self.my_folder_path): 
            os.makedirs(self.my_folder_path)
        if os.path.exists(self.my_folder_path):
            log_info = f"创建用户文件夹成功: {self.my_folder_path}"
            self.log_server.write_log(log=LogModel(log_info, "INFO"))
            return True
        else:
            log_info = f"创建用户文件夹失败: {self.my_folder_path}"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
            return False
    
    def check_user_folder_exist(self) -> bool:
        
        return os.path.exists(self.my_folder_path)
    
    def get_my_folder_path(self) -> str:
        
        if not self.check_user_folder_exist():
            self.mkdir_my_folder_path()
        return self.my_folder_path
    
    def check_my_action_log_exist(self) -> bool:
        
        return os.path.exists(self.my_action_log_path)
    
    def get_my_action_log_path(self) -> str:
        """获取我的操作日志路径。
        如果用户文件夹不存在，则创建用户文件夹。
        如果操作日志文件不存在，则创建一个空的操作日志文件。
        返回:
            str: 操作日志文件的路径。
        """
        
        if not self.check_user_folder_exist():
            self.mkdir_my_folder_path()
        if not os.path.exists(self.my_action_log_path):
            with open(self.my_action_log_path, 'w') as f:
                f.write('{"logs": []}')
        return self.my_action_log_path
    
    def create_action_file(self, operation_name: str, time_str: str, status: str) -> tuple:
        
        file_name = f"{operation_name}_{time_str}_{status}.txt"
        abs_file_path = os.path.join(self.my_folder_path, file_name)
        log_info = f"创建用户操作文件: {abs_file_path}"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        if not os.path.exists(abs_file_path):
            with open(abs_file_path, 'w') as f:
                f.write('')
        create_result = os.path.exists(abs_file_path)
        if create_result:
            log_info = f"创建用户操作文件成功: {abs_file_path}"
            self.log_server.write_log(log=LogModel(log_info, "INFO"))
        else:
            log_info = f"创建用户操作文件失败: {abs_file_path}"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
        return create_result, abs_file_path
    
    def update_action_file(self, operation_name: str, time_str: str, old_status: str, new_status: str) -> tuple:
        
        old_file_name = f"{operation_name}_{time_str}_{old_status}.txt"
        new_file_name = f"{operation_name}_{time_str}_{new_status}.txt"
        abs_old_file_path = os.path.join(self.my_folder_path, old_file_name)
        abs_new_file_path = os.path.join(self.my_folder_path, new_file_name)
        if os.path.exists(abs_old_file_path):
            os.rename(abs_old_file_path, abs_new_file_path)
        return os.path.exists(abs_new_file_path), abs_new_file_path
    
    def get_my_file_list(self) -> list:
        
        log_info = f"获取用户文件列表: {self.my_folder_path}"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        directory_path = self.my_folder_path
        files = []
        try:
            files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
            log_info = f"获取用户文件列表成功: {files}"
            self.log_server.write_log(log=LogModel(log_info, "INFO"))
        except Exception as e:
            log_info = f"获取用户文件列表失败: {e}"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
        return files
    
    def get_my_target_action_file_name(self, operation_name: str, time_str: str) -> str:
        
        log_info = f"获取用户操作文件名: {operation_name}_{time_str}"
        target_file_name = f"{operation_name}_{time_str}"
        last_file_name = ""
        has_last_file = False
        for file_name in self.get_my_file_list():
            if file_name.startswith(target_file_name):
                last_file_name = file_name
                has_last_file = True
                log_info = f"获取用户操作文件名成功: {file_name}"
                self.log_server.write_log(log=LogModel(log_info, "INFO"))
                break
        if not has_last_file:
            log_info = f"获取用户操作文件名失败: {target_file_name}"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
        return last_file_name
    
    def get_my_target_action_file_abs_path(self, operation_name: str, time_str: str) -> str:
        
        file_name = self.get_my_target_action_file_name(operation_name=operation_name, time_str=time_str)
        abs_file_path = os.path.join(self.my_folder_path, file_name)
        return abs_file_path
    
    def get_my_target_action_file_status(self, operation_name: str, time_str: str) -> str:
        
        file_name = self.get_my_target_action_file_name(operation_name=operation_name, time_str=time_str)
        file_status = ""
        try:
            file_status = file_name.split('_')[-1].split('.')[0]
        except Exception as e:
            log_info = f"获取用户操作文件状态失败: {e}"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
        return file_status
    
    def get_my_target_action_file_content(self, abs_file_path: str):
        
        file_content = []
        try:
            if IOTools().check_target_file_exist(abs_file_path):
                file_content = IOTools().read_json_from_file(abs_file_path)
        except Exception as e:
            log_info = f"获取用户操作文件内容失败: {e}"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
        return file_content
    
    
        
        
    
    