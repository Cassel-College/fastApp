#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import json
import os
import jwt
import datetime

from src.model.public.log_model import LogModel
from src.model.public.return_info import ReturnCode, ReturnInfo
from src.tools.public.log_tools.log_tools import LogTools
from src.tools.public.config_tools.config_tools import ConfigTools
from src.tools.public.user_system_tools.init_user_system_tools.Init_user_ysystem_tools import InitUserSystemTools
from src.tools.public.io_tools.io_tools import IOTools
from src.model.public.user_info import UserInfo

# 秘密密钥，必须保密
SECRET_KEY = 'your_secret_key_here'

class UserLoadingTools():
    
    def __init__(self):
        self.log_server = LogTools()
        log_info = f"初始化用户注册系统工具"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        
        self.config_tools = ConfigTools()
        self.user_info_file_path = self.config_tools.get_user_info_file_path()
        self.user_folder_path = self.config_tools.get_user_folder_path()
        InitUserSystemTools().run()

    # 生成token的函数
    def generate_token(self, user_name):
        # 设置token的有效期为24小时
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        # 定义payload（有效载荷），包含user_name和过期时间
        payload = {
            'user_name': user_name,
            'exp': expiration_time
        }
        # 使用HS256算法生成token
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    # 校验token的函数
    def verify_token(self, token):
        try:
            # 解码token，校验过期时间及其它信息
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return decoded['user_name'], True
        except jwt.ExpiredSignatureError:
            # 如果token过期
            return None, False
        except jwt.InvalidTokenError:
            # 如果token无效
            return None, False
    
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
    
    def loading_user(self, user_info: UserInfo) -> ReturnInfo:
        
        log_info = f"Loading user core function: {user_info}"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        user_info.user_folder_path = os.path.join(self.user_folder_path, user_info.user_name)
        
        return_result = ReturnInfo(code=ReturnCode.FAILED, message="User loading failed", data={"user_info": user_info})
        users = self.get_user_list()
        users_names = []
        for user in users:
            if isinstance(user, dict):
                users_names.append(user.get("user_name"))
                if user_info.user_name == user.get("user_name", ""):
                    if user_info.user_password == user.get("user_password", ""):
                        user_info.token = self.generate_token(user_name=user_info.user_name)
                        log_info = f"User loading successfully: {user_info}"
                        self.log_server.write_log(log=LogModel(log_info, "INFO"))
                        return_result.code = ReturnCode.SUCCESS
                        return_result.message = "User loading successfully"
                        return_result.data = {"user_info": user_info}
                        return return_result
                    else:
                        log_info = f"User password error: {user_info}"
                        self.log_server.write_log(log=LogModel(log_info, "ERROR"))
                        return_result.message = f"User password error."
                        return return_result
        if user_info.user_name not in users_names:
            log_info = f"User {user_info.user_name} not exist"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
            return_result.message = f"User {user_info.user_name} not exist"
            return return_result
        return return_result
    
    def get_user_name_as_list(self) -> list:
        
        log_info = f"Get all user name as list."
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        users = self.get_user_list()
        users_names = []
        for user in users:
            if isinstance(user, dict):
                users_names.append(user.get("user_name"))
        return users_names
    
    def check_user_loading_verify_core(self, user_info: UserInfo) -> bool:
        
        log_info = f"Check user core function core: {user_info}"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        is_valid = False
        users_names = self.get_user_name_as_list()
        if user_info.user_name not in users_names:
            log_info = f"User {user_info.user_name} not exist"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
            is_valid = False
        else:
            user_token = user_info.token
            print(f"user_token: {user_token}")
            user_name, is_valid = self.verify_token(user_token)
            if is_valid:
                log_info = f"User {user_name} token verify successfully"
                self.log_server.write_log(log=LogModel(log_info, "INFO"))
                is_valid = True
            else:
                log_info = f"User {user_info.user_name} token error"
                self.log_server.write_log(log=LogModel(log_info, "ERROR"))
                is_valid = False
        return is_valid
    
    def check_user_loading_verify(self, user_info: UserInfo) -> ReturnInfo:
        
        log_info = f"Check user core function: {user_info}"
        self.log_server.write_log(log=LogModel(log_info, "INFO"))

        return_result = ReturnInfo(code=ReturnCode.FAILED, message="User loading failed", data={"user_info": user_info})
        is_valid = False
        
        try:
            is_valid = self.check_user_loading_verify_core(user_info=user_info)
        except Exception as e:
            log_info = f"Check user core function failed: {e}"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
            return_result.message = f"Check user core function failed: {e}"
            return return_result
        
        if is_valid:
            log_info = f"User {user_info.user_name} token verify successfully"
            self.log_server.write_log(log=LogModel(log_info, "INFO"))
            return_result.code = ReturnCode.SUCCESS
            return_result.message = "User token verify successfully"
            return_result.data = {"user_info": user_info}
        else:
            log_info = f"User {user_info.user_name} token error"
            self.log_server.write_log(log=LogModel(log_info, "ERROR"))
            return_result.message = f"User {user_info.user_name} token error"
        return return_result
        
    
