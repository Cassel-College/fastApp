#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import json
import os
import subprocess

from src.model.public.log_model import LogModel
from src.tools.public.log_tools.log_tools import LogTools


class ScriptTools():
    
    def __init__(self):
        pass
    
    def run_script(self, script_path: str, input_data: str) -> str:
        
        log_server = LogTools()
        log_info = f"执行第三方脚本: {script_path}; 输入数据: {input_data}"
        log_server.write_log(log=LogModel(log_info, "INFO"))
        output = ""
        try:
            result = subprocess.run(
                ["python3", script_path],
                input=json.dumps(input_data),  # 发送数据到标准输入
                capture_output=True,
                text=True,
                check=True
            )
            output = str(result.stdout)
            log_info = f"第三方脚本返回数据: {output}"
            log_server.write_log(log=LogModel(log_info, "INFO"))
        except subprocess.CalledProcessError as e:
            log_info = f"执行第三方脚本失败: {e}"
            log_server.write_log(log=LogModel(log_info, "ERROR"))
        return output
    
    def update_script(self, script_path: str, input_data: str) -> bool:
        
        log_server = LogTools()
        log_info = f"更新第三方脚本: {script_path}; 输入数据: {input_data}"
        log_server.write_log(log=LogModel(log_info, "INFO"))
        update_status = False
        try:
            # Open the script file in write mode to clear and update it
            with open(script_path, 'w', encoding='utf-8') as script_file:
                script_file.write(input_data)
            update_status = True
            log_info = f"第三方脚本更新成功: {script_path}"
            log_server.write_log(log=LogModel(log_info, "INFO"))
        except Exception as e:
            log_info = f"更新第三方脚本失败: {e}"
            log_server.write_log(log=LogModel(log_info, "ERROR"))
        return update_status
    
    def get_script(self, script_path: str) -> str:
        
        log_server = LogTools()
        log_info = f"获取第三方脚本: {script_path}"
        log_server.write_log(log=LogModel(log_info, "INFO"))
        output = ""
        try:
            with open(script_path, 'r', encoding='utf-8') as script_file:
                output = script_file.read()
            log_info = f"获取第三方脚本成功: {script_path}"
            log_server.write_log(log=LogModel(log_info, "INFO"))
        except Exception as e:
            log_info = f"获取第三方脚本失败: {e}"
            log_server.write_log(log=LogModel(log_info, "ERROR"))
        return output

# Example usage
# input_data = {"command": "process", "values": [1, 2, 3]}
# run_script("script.py", input_data)
