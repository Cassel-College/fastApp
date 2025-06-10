#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import openai


class DeepSeekGPTAPI:
    
    def __init__(self, api_key: str, model="deepseek-chat", max_tokens=1000, temperature=0.7):
        """
        初始化 ChatGPTClient 类。
        
        :param model: 使用的模型名称，默认是 ep-20241219135516-b4clr。
        :param max_tokens: 每次响应的最大 token 数，默认为 1000。
        :param temperature: 控制生成的随机性，默认是 0.7。
        """
        
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        self.client = openai.OpenAI(
            api_key = self.api_key,
            base_url = "https://api.deepseek.com",
        )
        
    def chat(self, prompt: str):
        """
        与 OpenAI API 交互的函数。

        :param prompt: 用户输入的提示信息。
        :return: ChatGPT 的响应。
        """
        
        try:
            # 发起 API 请求
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            # print(response)
            # import json
            # print(json.dumps(response, indent=4, ensure_ascii=False))
            # 提取并返回响应内容
            # return response.dict()['choices'][0]['message']['content']
            return response.dict()
        except Exception as e:
            return {"error": str(e)}

    
    def chat_old(self, api_key, prompt):
        """
        与 OpenAI API 交互的函数。
        
        :param api_key: OpenAI API 密钥。
        :param prompt: 用户输入的提示信息。
        :return: ChatGPT 的响应。
        """
        # 动态设置 API 密钥
        openai.api_key = api_key
        
        try:
            # 发起 API 请求
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are ChatGPT, a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            # 提取并返回响应内容
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    def extract_answers_all(self, data: dict):
        results = []
        if "choices" in data.keys():
            for choice in data["choices"]:
                message = choice.get("message", {})
                content = message.get("content", "")
                results.append(content)
        return "".join(results)
    
    def extract_answers_frist(self, data: dict):
        results = []
        if "choices" in data.keys():
            for choice in data["choices"]:
                message = choice.get("message", {})
                content = message.get("content", "")
                results.append(content)
                break
        return "".join(results)
        
# ARK_API_KEY = "99263ff7-c198-4aec-8bf5-720fb1a38a62"
# model="ep-20241219135516-b4clr"
# prompt = "你好,你是一个有多年驾驶经验和有丰富经验的自动驾驶测试工程师.              我给你一个测试背景描述和一些简要的测试场景要素，你可以帮我生产一个自动驾驶测试方案吗？只包含多组测试项目用例             测试背景是这样的：“原先自己使用历史速度计算acc，目前感知已给出，直接使用，主要关注：1. 前车刹车不及时的问题，前车acc不对导致的点刹问题”;             简要的测试场景要素数据如下：{'自车行驶时间段': '白天', '自车行驶环境': '高速公路', '自车行驶速度': '100 km/h以上', '与其他车辆的交互': '跟车行驶', '与行人的交互': '无行人', '自车行为': '正常行驶', '导航需求': '直行', '路口': '无', '前车行为': '紧急变道并制动'};            你所生成的测试方案场景从我给出的测试场景要素数中给出，你来进行合理的扩展的完善，一定要合理，不要排列组合，整个测试方案中的测试项目，测试场景，测试目标，预期结果，测试方法，通过标准，额外条件一定要合理，紧扣测试背景，使用你多年的自动驾驶从业经验和丰富的驾驶经验给出良好的测试方案；            返回数据的模板是：“| **测试项**   | **详细内容** |             | ------------ | ------------ |            | **测试项目** |              |            | **测试场景** |              |            | **测试目标** |              |            | **预期结果** |              |            | **测试方法** |              |            | **通过标准** |              |            | **额外条件** |              |”;            模板可以酌情修改和新增数据行处理。            我的附加要求是：;            每组测试用例需要用分割符: **********分开，方便我单独查看，            只需要返回markdown格式的表格就好。"

# gpt = DoubaoGPTAPI(api_key=ARK_API_KEY, model="ep-20241219135516-b4clr", max_tokens=1000, temperature=0.7)
# info = gpt.chat(prompt=prompt)
# print(info)