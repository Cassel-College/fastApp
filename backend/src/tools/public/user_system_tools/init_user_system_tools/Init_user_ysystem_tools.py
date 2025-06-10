#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import json
import os
import subprocess

from src.model.public.log_model import LogModel
from src.tools.public.log_tools.log_tools import LogTools
from src.tools.public.config_tools.config_tools import ConfigTools


class InitUserSystemTools():
    
    def __init__(self):
        
        self.log_server = LogTools()
        log_info = f"初始化用户系统工具"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        
        self.config_tools = ConfigTools()
        self.user_info_file_path = self.config_tools.get_user_info_file_path()
        self.user_folder_path = self.config_tools.get_user_folder_path()
        
        
    def check_user_folder(self) -> bool:        
        user_folder_existed = os.path.exists(self.user_folder_path)
        if not user_folder_existed:
            log_info = f"用户文件夹不存在: {self.user_folder_path}"
            self.log_server.write_log(log=LogModel(log_info, "INFO"))
        else:
            log_info = f"用户文件夹存在: {self.user_folder_path}"
            self.log_server.write_log(log=LogModel(log_info, "WARNING"))
        return user_folder_existed
    
    def check_user_info_file(self) -> bool:        
        user_info_file_existed = os.path.exists(self.user_info_file_path)
        if not user_info_file_existed:
            log_info = f"用户信息文件不存在: {self.user_info_file_path}"
            self.log_server.write_log(log=LogModel(log_info, "INFO"))
        else:
            log_info = f"用户信息文件存在: {self.user_info_file_path}"
            self.log_server.write_log(log=LogModel(log_info, "WARNING"))
        return user_info_file_existed
    
    def create_user_folder(self) -> bool:   
        log_info = f"创建用户文件夹: {self.user_folder_path}"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))     
        try:
            os.makedirs(self.user_folder_path)
            log_info = f"用户文件夹创建成功: {self.user_folder_path}"
            self.log_server.write_log(log=LogModel(log_info, "INFO"))
            return True
        except Exception as e:
            log_info = f"创建用户文件夹失败: {e}"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
            return False
    
    def create_user_info_file(self) -> bool: 
        log_info = f"创建用户信息文件: {self.user_info_file_path}"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))     
        try:
            default_user_info = {
                "user_list": [
                    {
                        "id": 1,
                        "user_name": "root",
                        "user_password": "root",
                        "token": "string",
                        "user_folder_path": "string"
                    }
                ]
            }

            with open(self.user_info_file_path, 'w') as file:
                # file.write("{\n}")
                file.write(json.dumps(default_user_info, indent=4))
            log_info = f"用户信息文件创建成功: {self.user_info_file_path}"
            self.log_server.write_log(log=LogModel(log_info, "INFO"))
            return True
        except Exception as e:
            log_info = f"创建用户信息文件失败: {e}"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
            return False
    
      
    def run(self):
        
        if not self.check_user_folder():
            self.create_user_folder()
        if not self.check_user_info_file():
            self.create_user_info_file()