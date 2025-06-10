#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import json
import requests


class GeminiAPI:
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash-latest"):
        """
        初始化 GeminiAPI 工具类
        :param api_key: API 密钥
        :param model: 默认使用的模型名称
        """
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = model  # 初始化时设定模型名称
    
    def set_model(self, model: str):
        """
        修改当前使用的模型名称
        :param model: 新的模型名称
        """
        self.model = model
    
    def generate_content(self, contents: list) -> dict:
        """
        发送请求到 Gemini API 并获取生成内容
        :param contents: 请求内容的列表
        :return: 返回解析的 JSON 数据
        """
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": text} for text in contents]}]}
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        
    def chat_old(self, contents: list) -> dict:
        """
        发送请求到 Gemini API 并获取生成内容
        :param contents: 请求内容的列表
        :return: 返回解析的 JSON 数据
        """
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": text} for text in contents]}]}
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        
    def chat(self, prompt: str) -> dict:
        """
        发送请求到 Gemini API 并获取生成内容
        :param contents: 请求内容的列表
        :return: 返回解析的 JSON 数据
        """
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        

    def extract_answers_all(self, data):
        results = []
        if "candidates" in data:
            for candidate in data["candidates"]:
                content = candidate.get("content", {})
                parts = content.get("parts", [])
                for part in parts:
                    text = part.get("text", "")
                    results.append(text)
        return "".join(results)
    
    def extract_answers_frist(self, data):
        results = []
        if "candidates" in data:
            for candidate in data["candidates"]:
                content = candidate.get("content", {})
                parts = content.get("parts", [])
                for part in parts:
                    text = part.get("text", "")
                    results.append(text)
                    break
                break
        return "".join(results)

# # 示例用法
# if __name__ == "__main__":
    
#     # 替换为你的 API 密钥
#     api_key = "AIzaSyDJFCqAxeu3hxvZatchxPrSwQmmtg1BZqo"
#     model="gemini-1.5-flash-latest"
#     # 初始化工具类
#     gemini_api = GeminiAPI(api_key, model=model)
    
#     # 调用生成内容的方法
#     contents = [
#         "你好！你了解自动驾驶的知识吗？我给你一些场景；你可以帮我生产一个自动驾驶测试方案吗？用表格的形式返回给我，只返回一个纵向的表格就好，不需要其他内容。这是场景元素：白天，停车场，5-10 km/h，跟车行驶，行人在人行道，減速礼让，掉头。"
#     ]
#     result = gemini_api.generate_content(contents=contents)
#     print("Response with default model: \n", json.dumps(result, ensure_ascii=False, indent=4))
    
#     # 修改模型名称
#     # gemini_api.set_model("another-model-name")
    
#     # 使用新的模型发送请求
#     result_with_new_model = gemini_api.generate_content(contents=contents)
#     print("Response with new model:", result_with_new_model)
