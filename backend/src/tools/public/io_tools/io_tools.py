#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import os
import sys
import json

from src.model.public.log_model import LogModel
from src.model.public.return_info import ReturnCode, ReturnInfo
from src.tools.public.log_tools.log_tools import LogTools

class IOTools():

    def __init__(self):
        self.log_tools = LogTools()
        pass   

    def get_folder_names_from_path(self, target_path: str) -> list:
        try:
            # 使用 os.listdir 获取目标路径下的所有文件和文件夹
            items = os.listdir(target_path)
            
            # 过滤出仅包含文件夹的名称，并返回结果列表
            folder_names = [item for item in items if os.path.isdir(os.path.join(target_path, item))]
            
            return folder_names
        except Exception as e:
            print(f"Error occurred: {e}")
            return []

    def check_target_folder_exist(self, target_folder_path: str) -> bool:

        if not os.path.exists(target_folder_path):
            return False
        else:
            return True
        
    def create_target_folder(self, target_folder_path: str) -> ReturnInfo:
        """
        创建目标文件夹

        :param target_folder_path: 目标文件夹路径
        :return: 0: 创建成功; 1: 创建失败; -1: 目标文件夹已存在
        """
        
        return_results = ReturnInfo(code=1, message="", data=None)
        
        log_info = f"create target file path: {target_folder_path}"
        log = LogModel(log_info, "INFO")
        self.log_tools.write_log(log)
        
        # 如果目标文件夹存在,返回错误
        if self.check_target_folder_exist(target_folder_path=target_folder_path):
            return_results.set_code(-1)
            return_results.set_message(f", target file already exists!")
        else:
            os.makedirs(target_folder_path)
            if self.check_target_folder_exist(target_folder_path=target_folder_path):
                return_results.set_code(0)
                return_results.set_message(f", create success!")
            else:
                return_results.set_code(1)
                return_results.set_message(f", create failed!")
        return return_results
    

    def create_target_file(self, target_file_path: str) -> ReturnInfo:
        """
        创建目标文件

        :param target_file_path: 目标文件路径
        :return: 0: 创建成功; 1: 创建失败; -1: 目标文件已存在
        """
        
        return_results = ReturnInfo(code=1, message="", data=None)
        
        log_info = f"create target file path: {target_file_path}"
        log = LogModel(log_info, "INFO")
        self.log_tools.write_log(log)
        
        # 如果目标文件存在,返回错误
        if self.check_target_file_exist(target_file_path=target_file_path):
            return_results.set_code(-1)
            return_results.set_message(f", target file already exists!")
        else:
            try:
                with open(target_file_path, 'w') as file:
                    file.write("")
            except Exception as e:
                print(f"Error occurred: {e}")
                return_results.set_code(1)
                return_results.set_message(f", create failed!")
            if self.check_target_file_exist(target_file_path=target_file_path):
                return_results.set_code(0)
                return_results.set_message(f", create success!")    
            else:
                return_results.set_code(1)
                return_results.set_message(f", create failed!")
        return return_results


    def read_json_from_file(self, file_path: str) -> dict:
        """
        读取json文件

        :param file_path: 文件路径
        :return: 0: 读取成功; 1: 读取失败; -1: 文件不存在
        """
        
        return_results = {}
        return_code = 1
        return_value = {}
        if not os.path.exists(file_path):
            return_code = -1
        else:
            try:
                with open(file_path, 'r') as file:
                    return_code = 0
                    return_value = json.load(file)
            except Exception as e:
                print(f"Error occurred: {e}")
                return_code = 1
                return_value = {}
        return_results = {
            "return_code": return_code,
            "return_value": return_value
        }
        return return_results

    def read_list_from_file(self, file_path: str) -> dict:
        """
        读取json文件

        :param file_path: 文件路径
        :return: 0: 读取成功; 1: 读取失败; -1: 文件不存在
        """
        
        return_results = {}
        return_code = 1
        return_value = []
        if not os.path.exists(file_path):
            return_code = -1
        else:
            try:
                with open(file_path, 'r') as file:
                    return_code = ReturnCode.SUCCESS
                    return_value = file.readlines()
            except Exception as e:
                print(f"Error occurred: {e}")
                return_code = ReturnCode.FAILED
                return_value = []
        return_results = {
            "return_code": return_code,
            "return_value": return_value
        }
        return return_results
    
    def read_txt_from_file(self, file_path: str) -> dict:
        """
        读取json文件

        :param file_path: 文件路径
        :return: 0: 读取成功; 1: 读取失败; -1: 文件不存在
        """
        
        return_results = {}
        return_code = 1
        return_value = ""
        if not os.path.exists(file_path):
            return_code = -1
        else:
            with open(file_path, 'r') as file:
                return_code = ReturnCode.SUCCESS
                return_value = file.read()
        return_results = {
            "return_code": return_code,
            "return_value": return_value
        }
        return return_results
    
    def check_file_exist(self, file_path: str) -> bool:
        if not os.path.exists(file_path):
            return False
        else:
            return True
        
    def check_target_file_exist(self, target_file_path: str) -> bool:
        if not os.path.exists(target_file_path):
            return False
        else:
            return True
        
    
    def read_target_file(self, target_file_path: str) -> ReturnInfo:
        
        log_server = LogTools()
        
        log_info = f"read target file path: {target_file_path}"
        log_server.write_log(LogModel(log_info, "INFO"))
        
        return_results = ReturnInfo(code=1, message="", data=None)
        
        if not self.check_target_file_exist(target_file_path=target_file_path):
            log_info = f"target file not exist: {target_file_path}"
            log_server.write_log(LogModel(log_info, "INFO"))
            return_results.set_code(ReturnCode.FAILED)
            return_results.set_message(f", target file not exist!")
            return_results.set_data("")
            return return_results
        try:
            with open(target_file_path, 'r') as file:
                return_results.set_code(ReturnCode.SUCCESS)
                return_results.set_message(f"read success!")
                return_results.set_data(file.read())
                log_info = f"read target file success: {target_file_path}"
                log_server.write_log(LogModel(log_info, "INFO"))
        except Exception as e:
            log_info = f"read target file failed: {target_file_path}; Error occurred: {e} "
            log_server.write_log(LogModel(log_info, "INFO"))
            return_results.set_code(ReturnCode.FAILED)
            return_results.set_message(f"read failed!")
            return_results.set_data("")
        return return_results
    
        
    def write_target_file(self, target_file_path: str, content: str) -> ReturnInfo:
        
        return_results = ReturnInfo(code=1, message="", data=None)
        if not self.check_target_file_exist(target_file_path=target_file_path):
            log_info = f"target file not exist: {target_file_path}"
            self.log_tools.write_log(LogModel(log_info, "INFO"))
            return_results.set_code(ReturnCode.FAILED)
            return_results.set_message(log_info)
            return return_results
        try:
            with open(target_file_path, 'w') as file:
                file.write(content)
            log_info = f"write target file success: {target_file_path}"
            self.log_tools.write_log(LogModel(log_info, "INFO"))
            return_results.set_code(ReturnCode.SUCCESS)
            return_results.set_message(f"Write file: {target_file_path} write success!")
        except Exception as e:
            log_info = f"write target file failed: {target_file_path}; Error occurred: {e} "
            self.log_tools.write_log(LogModel(log_info, "INFO"))
            return_results.set_code(ReturnCode.FAILED)
            return_results.set_message(f"Write file: {target_file_path} write failed!")
        return return_results
    
    def create_file(self, file_path: str) -> ReturnInfo:
        
        log_info = f"create file path: {file_path}"
        self.log_tools.write_log(LogModel(log_info, "INFO"))
        
        return_results = ReturnInfo(code=1, message="", data=None)
        try:
            with open(file_path, 'w') as file:
                file.write("")
            return_results.set_code(ReturnCode.SUCCESS)
            return_results.set_message(f"Create file: {file_path} success!")
        except Exception as e:
            return_results.set_code(ReturnCode.FAILED)
            return_results.set_message(f"Create file: {file_path} failed!")
        return return_results
    
    def write_file(self, file_path: str, content: str) -> ReturnInfo:
        
        log_info = f"write file path: {file_path}"
        self.log_tools.write_log(LogModel(log_info, "INFO"))
        
        return_results = ReturnInfo(code=1, message="", data=None)
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            return_results.set_code(ReturnCode.SUCCESS)
            return_results.set_message(f"Write file: {file_path} write success!")
        except Exception as e:
            return_results.set_code(ReturnCode.FAILED)
            return_results.set_message(f"Write file: {file_path} write failed!")
        return return_results
    
    def write_json_to_file(self, file_path: str, data: dict) -> ReturnInfo:
        """
        写入json文件    

        :param file_path: 文件路径
        :param data: 写入的数据
        :return: 0: 写入成功; 1: 写入失败; -1: 文件不存在
        """
        
        return_results = ReturnInfo(code=1, message="", data=None)
        if not self.check_target_file_exist(target_file_path=file_path):
            log_info = f"target file not exist: {file_path}"
            self.log_tools.write_log(LogModel(log_info, "INFO"))
            return_results.set_code(ReturnCode.FAILED)
            return_results.set_message(f"target file not exist!")
            return return_results
        try:
            with open(file_path, 'w') as file:
                file.write(json.dumps(data, indent=4, ensure_ascii=False))
            log_info = f"write json to file success: {file_path}"
            self.log_tools.write_log(LogModel(log_info, "INFO"))
            return_results.set_code(ReturnCode.SUCCESS)
            return_results.set_message(f"Write file: {file_path} write success!")
        except Exception as e:
            log_info = f"write json to file failed: {file_path}; Error occurred: {e} "
            self.log_tools.write_log(LogModel(log_info, "INFO"))
            return_results.set_code(ReturnCode.FAILED)
            return_results.set_message(f"Write file: {file_path} write failed!")
        return return_results