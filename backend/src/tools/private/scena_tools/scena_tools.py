#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import json
import os
import re
import itertools

from src.model.public.log_model import LogModel
from src.tools.public.io_tools.io_tools import IOTools
from src.tools.public.log_tools.log_tools import LogTools
from src.model.public.return_info import ReturnCode, ReturnInfo

class ScenaTools:
    
    def __init__(self, codes: list, scenarios_info: list):
        self.codes = codes
        self.scenarios_info = scenarios_info
        self.log_server = LogTools()
        self.io_tools = IOTools()
    
    def get_scena_by_code(self, code: str) -> dict:
        
        has_scena = False
        for scenario in self.scenarios_info:
            if scenario["code"] == code:
                has_scena = True
                return scenario
        if has_scena is False:
            return {}
        
    
    def gen_scena_list_by_codes(self) -> ReturnInfo:

        self.log_server.write_log(log=LogModel(f"Gen scena list by codes.", "INFO"))
        
        scena_mapping = {}
        
        for code in self.codes:
            scena = self.get_scena_by_code(code)
            group_name = scena.get("group_name", "")
            if group_name not in scena_mapping.keys():
                scena_mapping[group_name] = []
            scena_mapping[group_name].append(scena)
            
        scenas = []
        for group_name in scena_mapping.keys():
            scena = scena_mapping.get(group_name, [])
            scenas.append(scena)
            
        combinations = list(itertools.product(*scenas))
        
        scena_list = []
        for combination in combinations:
            scena_list.append(list(combination))
        print("--------------------")
        for scena in scena_list:
            print(scena)
        print("--------------------")
        self.log_server.write_log(log=LogModel(f"Gen scene list, number: {len(scena_list)}.", "INFO"))
        return ReturnInfo(code=ReturnCode.SUCCESS, data={"scena_list": scena_list}, message="Gen scene list.")
    
    def gen_simple_scena(self, scena: dict={}) -> dict:
        
        simple_scena = {}
        if "group_name" in scena.keys():
            simple_scena["group_name"] = scena["group_name"]
        if "label_name" in scena.keys():
            simple_scena["label_name"] = scena["label_name"]
        return simple_scena
    
    def gen_simple_scena_list_by_codes(self) -> ReturnInfo:

        self.log_server.write_log(log=LogModel(f"Gen scena list by codes.", "INFO"))
        
        scena_mapping = {}
        
        for code in self.codes:
            scena = self.get_scena_by_code(code)
            group_name = scena.get("group_name", "")
            if group_name not in scena_mapping.keys():
                scena_mapping[group_name] = []
            scena_mapping[group_name].append(scena)
            
        scenas = []
        for group_name in scena_mapping.keys():
            scena = scena_mapping.get(group_name, [])
            scenas.append(scena)
            
        combinations = list(itertools.product(*scenas))
        
        scena_list = []
        for combination in combinations:
            simple_scenas = []
            for scena in combination:
                simple_scenas.append(self.gen_simple_scena(scena))
            scena_list.append(simple_scenas)
            
        print("--------------------")
        for scena in scena_list:
            print(scena)
        print("--------------------")
        self.log_server.write_log(log=LogModel(f"Gen scene list, number: {len(scena_list)}.", "INFO"))
        return ReturnInfo(code=ReturnCode.SUCCESS, data={"scena_list": scena_list}, message="Gen scene list.")
    
    def gen_table_data(self, simple_scena_list: list) -> dict:
        
        title = []
        data = []
        table_data = {
            "title": [],
            "data": []
        }
        title.append("index")
        for simple_scena in simple_scena_list:
            for scena in simple_scena:
                # print(scena)
                group_name = scena["group_name"]
                if group_name not in title:
                    title.append(group_name)
        # print(title)  
            
        row_number = len(title)       
        for index, simple_scena in enumerate(simple_scena_list):
            temp_data = []
            temp_data.append(index)
            for i in range(row_number - 1):
                temp_data.append("")
            # print(temp_data)
            for scena in simple_scena:   
                label_name = scena["label_name"]
                group_name = scena["group_name"]
                group_name_index = title.index(group_name)
                temp_data[group_name_index] = label_name
            # print(temp_data)
            data.append(temp_data)
        table_data["title"] = title
        table_data["data"] = data
        return table_data

    def merge_dicts(self, dict1, dict2):
        """
        合并两个字典，校验 value 的唯一性，并按规则重新编号 key。
        :param dict1: 第一个字典
        :param dict2: 第二个字典
        :return: 合并后的新字典
        """
        merged_dict = {}
        unique_values = set()  # 用于检查 value 的唯一性
        index = 1  # 初始化新的编号

        def sanitize_key(key):
            """
            删除 key 中的所有数字字符。
            :param key: 原始 key
            :return: 去掉数字后的 key
            """
            return re.sub(r'\d', '', key)

        def add_to_merged(data):
            nonlocal index
            for key, value in data.items():
                # 如果 value 的 str 形式不在集合中，添加到结果中
                value_str = str(value)
                if value_str not in unique_values:
                    unique_values.add(value_str)
                    sanitized_key = sanitize_key(key)  # 删除 key 中的数字
                    merged_dict[f"{sanitized_key}{index}"] = value
                    index += 1

        # 合并两个字典
        add_to_merged(dict1)
        add_to_merged(dict2)

        return merged_dict

    def split_test_items(
        self, 
        input_data: str, 
        s_split: str = '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@', 
        e_split: str = '*********') -> list:
        test_items = []
        
        title_number = 0
        case_number = 0
        node_index = 0
        ss = input_data.split(s_split)
        for s in ss:
            e_s = s.split(e_split)
            for item in e_s:
                has_title = False
                title = ''
                md_text = ''
                lines = item.split('\n')
                for line in lines:
                    if '' == line:
                        continue
                    if line.startswith("## "):
                        has_title = True
                        title = line
                        title_number
                        continue
                    if line.startswith("|"):
                        md_text = md_text + line + '\n'
                if has_title:
                    info = {
                        'node_index': node_index,
                        'node_type': "title",
                        'node_info': title
                    }
                    test_items.append(info)
                    title_number = title_number + 1
                    node_index = node_index + 1
                if '' != md_text:
                    info = {
                        'node_index': node_index,
                        'node_type': "md",
                        'md_str': md_text,
                        'node_info': self.md_table_to_list(md_text)
                    }
                    test_items.append(info)
                    case_number = case_number + 1
                    node_index = node_index + 1
        log_info = f"Gen test items, title number: {title_number}, case number: {case_number}."
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        return test_items


    def md_table_to_list(self, input_data: str) -> list:
        """
        将 Markdown 表格字符串解析为二维数组。
        Args:
            input_data (str): 输入的 Markdown 表格字符串。
        Returns:
            list: 二维数组形式的表格数据。
        """
        table_info: list = []

        # 检查输入数据是否为字符串
        if not isinstance(input_data, str):
            raise ValueError("输入数据必须是字符串类型")

        # 去掉多余的换行符，确保输入的每一行是有效的表格数据
        rows = [line.strip() for line in input_data.strip().split('\n') if line.strip()]

        # 跳过标题分割线和空行
        rows = [row for row in rows if not re.match(r'^[-| ]+$', row)]

        for row in rows:
            try:
                # 去掉行首和行尾的 "|" 并分割
                cells = [cell.strip() for cell in row.strip('|').split('|')]

                # 确保每一行非空
                if cells:
                    table_info.append(cells)
                for index, _ in enumerate(cells):
                    # 如果单元格内数据长度大于100，每40个字符左右进行换行
                    if 40 < len(cells[index]):
                        cells[index] = "\n".join([cells[index][i:i + 40] for i in range(0, len(cells[index]), 40)])
            except Exception as e:
                # 捕获意外情况，记录并跳过当前行
                print(f"解析行时发生错误: {row}. 错误信息: {e}")
                continue

        # 检查表格内容是否为空
        if not table_info:
            raise ValueError("输入数据解析后为空，可能不是有效的 Markdown 表格")

        # 确保每一行列数一致（如果需要强一致性）
        max_columns = max(len(row) for row in table_info)
        for row in table_info:
            while len(row) < max_columns:  # 使用空字符串补齐缺失的列
                row.append("")

        return table_info
