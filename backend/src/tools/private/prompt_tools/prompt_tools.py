#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import json
import os

class PromptTools():
    def __init__(self):
        
        pass
    
    def gen_simplify_scenarios_prompt(self, background: str, simplify_scenarios_data: str) -> str:
        """
        生成一个用于自动驾驶测试方案的提示字符串。
        
        参数:
        background (str): 测试背景描述。
        simplify_scenarios_data (str): 场景库数据。

        返回:
        str: 生成的提示字符串，包含测试背景和场景库信息。
        """
        
        prompt = f"你好,你是一个有多年驾驶经验和有丰富经验的自动驾驶测试工程师. \n我给你一个测试背景描述和一些场景库，你可以帮我生产一些自动驾驶测试方案吗？\n测试背景是这样的：“{background}”\n场景库的数据如下：{str(simplify_scenarios_data)}\n你所搭建的测试方案的场景中场景元素都从我给的场景库里给出来,用dict嵌套dict的格式\n返回json格式给我, 第一层dict中的key是场景的名字加序号，第二层dict中的key是场景元素的名字, 我会直接把你返回的信息loads成dict，所以不需要其他内容\n不需要```python,```json,```这样的格式，只需要返回纯文本就好。"
        return prompt
    
    
    def gen_full_scenarios_prompt(self, 
                                  background: str, 
                                  simplify_scenarios_data: str, 
                                  replenish: str) -> str:
        """
        生成一个用于自动驾驶测试方案的提示字符串。
        
        参数:
        background (str): 测试背景描述。
        simplify_scenarios_data (str): 场景库数据。

        返回:
        str: 生成的提示字符串，包含测试背景和场景库信息。
        """
        
        prompt = f"你好,你是一个有多年驾驶经验和有丰富经验的自动驾驶测试工程师. \n \
            我给你一个测试背景描述和一些简要的测试场景要素，你可以帮我生产一个自动驾驶测试方案吗？只包含多组测试项目用例\n \
            测试背景是这样的：“{background}”;\n \
            简要的测试场景要素数据如下：{str(simplify_scenarios_data)}\n;\
            你所生成的测试方案场景从我给出的测试场景要素数中给出，你来进行合理的扩展的完善，一定要合理，不要排列组合，整个测试方案中的测试项目，测试场景，测试目标，预期结果，测试方法，通过标准，额外条件一定要合理，紧扣测试背景，使用你多年的自动驾驶从业经验和丰富的驾驶经验给出良好的测试方案；\
            返回数据的模板是：“| **测试项**   | **详细内容** | \
            | ------------ | ------------ |\
            | **测试项目** |              |\
            | **测试场景** |              |\
            | **测试目标** |              |\
            | **预期结果** |              |\
            | **测试方法** |              |\
            | **通过标准** |              |\
            | **额外条件** |              |”;\
            模板可以酌情修改和新增数据行处理。\
            一定要返回多行俩列的样式的表格。\
            我的附加要求是：{replenish};\
            每组测试用例需要用分割符: **********分开，方便我单独查看，\
            只需要返回markdown格式的表格就好。"
        return prompt
    
    
    def update_full_scenarios_prompt(self, 
                                     background: str, 
                                     scenarios_data: str, 
                                     replenish: str) -> str:
        """
        生成一个用于自动驾驶测试方案的提示字符串。
        
        参数:
        background (str): 测试背景描述。
        simplify_scenarios_data (str): 场景库数据。

        返回:
        str: 生成的提示字符串，包含测试背景和场景库信息。
        """
        
        prompt = f"你好,你是一个有多年驾驶经验和有丰富经验的自动驾驶测试工程师. \n \
            我给你一个测试背景描述和一些简要的测试场景要素，你可以帮我修改一个自动驾驶测试方案吗？\n \
            测试背景是这样的：“{background}”;\n \
            当前的测试场景数据如下：{str(scenarios_data)}\n;\
            我感觉数据不满足我的需求，需要稍微调整一下，我的要求是：{replenish};\
            一切修改在在原表格内进行，只修改表格内元素，不要新增表格; 只需要返回markdown格式的表格就好。"
        return prompt
    
# 只需要返回一个测试项目用例