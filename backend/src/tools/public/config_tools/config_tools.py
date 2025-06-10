#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import os
import sys
import json  # 添加这个导入


class ConfigTools(object):

    def __init__(self):

        self.exec_root_path = os.getcwd()
        self.config_file_path = os.path.join(self.exec_root_path, "src/config.json")
        self.config_dict = None

    def get_config(self) -> dict:
        
        config = {}

        if not os.path.exists(self.config_file_path):
            raise FileNotFoundError(f"config file: {self.config_file_path} not found!")

        with open(self.config_file_path, "r") as f:
            config = json.load(f)  # 使用 json.load 代替 eval

        return config
    
    def get_log_folder_path(self) -> str:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        log_folder_path = os.path.join(self.exec_root_path, self.config_dict.get("log_folder_path", ""))
        return log_folder_path
    
    def get_source_folder_path(self) -> str:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        source_folder_path = os.path.join(self.exec_root_path, self.config_dict.get("source_folder_path", ""))
        return source_folder_path
    
    def get_input_file_name(self) -> str:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        return self.config_dict.get("input_file_name", "")
    
    def get_output_file_name(self) -> str:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        return self.config_dict.get("output_file_name", "")

    def get_step_log_file_name(self) -> str:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        return self.config_dict.get("step_log_file_name", "")
    
    def get_script_engine(self) -> str:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        return self.config_dict.get("script_engine", "")
    
    def get_environment(self) -> str:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        return self.config_dict.get("environment", "")

    def get_dev_mode(self) -> dict:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        return self.config_dict.get("dev_mode", {})

    def get_dev_mode_open(self) -> bool:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        return self.config_dict.get("dev_mode", {}).get("open", False)
    
    def get_dev_mode_print_log_in_terminal(self) -> bool:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        return self.config_dict.get("dev_mode", {}).get("print_log_in_terminal", False)
    
    def get_gmini_api_key(self) -> str:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        return self.config_dict.get("gmini_setting", {}).get("gmini_api_key", "")
    
    def get_gmini_model_name(self) -> str:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        return self.config_dict.get("gmini_setting", {}).get("model", "")
    
    def get_open_ai_api_key(self) -> str:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        return self.config_dict.get("open_ai_setting", {}).get("open_ai_api_key", "")
    
    def get_open_ai_model_name(self) -> str:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        return self.config_dict.get("open_ai_setting", {}).get("model", "")
    
    def get_root_username(self) -> str:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        return self.config_dict.get("root_setting", {}).get("username", "")
    
    def check_root_passwork(self) -> str:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        password_key = self.config_dict.get("root_setting", {}).get("password_key", "")
        return password_key
    
    def get_user_folder_name(self) -> str:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        user_folder_name = self.config_dict.get("user_folder_name", "")
        return user_folder_name
    
    def get_user_info_file_name(self) -> str:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        return self.config_dict.get("user_info_file_name", "")
    
    
    def get_user_info_file_path(self) -> str:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        user_info_file_path = os.path.join(self.get_source_folder_path(), self.get_user_info_file_name())
        return user_info_file_path
    
    def get_user_folder_path(self) -> str:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        user_folder_path = os.path.join(self.get_source_folder_path(), self.get_user_folder_name())
        return user_folder_path
    
    def get_maximum_operating_time_interval(self) -> int:

        if self.config_dict is None:
            self.config_dict = self.get_config()
        
        return self.config_dict.get("maximum_operating_time_interval", 60)
