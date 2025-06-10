#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import os
import sys
import json

from src.model.public.log_model import LogModel
from src.model.public.return_info import ReturnCode, ReturnInfo
from src.tools.public.deepseek_tools.deepseek_agent_tools import DeepSeekGPTAPI
from src.tools.public.log_tools.log_tools import LogTools
from src.tools.public.gmini_tools.gmini_tools import GeminiAPI
from src.tools.public.doubao_tools.doubao_agent_tools import DoubaoGPTAPI

class GPTAPI:
    
    def __init__(self, 
                 gpt_type: str, 
                 api_key: str,
                 model="ep-20241219135516-b4clr", 
                 max_tokens=1000, 
                 temperature=0.7) -> object:
        """
        初始化 ChatGPTClient 类。
        
        :param model: 使用的模型名称，默认是 ep-20241219135516-b4clr。
        :param max_tokens: 每次响应的最大 token 数，默认为 1000。
        :param temperature: 控制生成的随机性，默认是 0.7。
        """
        
        self.gpt_type = gpt_type
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.log_server = LogTools()
    
    def gen_bot(self):
        
        log_info = f"Init GPT ..."
        self.log_server.write_log(log=LogModel(log_info, "INFO"))
        if self.gpt_type == "openai":
            pass
        elif self.gpt_type.lower() == "doubao":
            self.model="ep-20241219135516-b4clr"
            client = DoubaoGPTAPI(
                api_key=self.api_key,
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature)
            log_info = f"Create DoubaoGPTAPI success! model: {self.model}"
            self.log_server.write_log(log=LogModel(log_info, "INFO"))
            return client
        elif self.gpt_type.lower() == "deepseek":
            self.model="deepseek-chat"
            client = DeepSeekGPTAPI(
                api_key=self.api_key,
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature)
            log_info = f"Create DeepSeek GPTAPI success! model: {self.model}"
            self.log_server.write_log(log=LogModel(log_info, "INFO"))
            return client
        elif self.gpt_type.lower() == "gemini":
            self.model = "gemini-1.5-flash-latest"
            client = GeminiAPI(api_key=self.api_key, model=self.model)
            log_info = f"Create GeminiAPI success! model: {self.model}"
            self.log_server.write_log(log=LogModel(log_info, "INFO"))
            return client
        else:
            self.model="ep-20241219135516-b4clr"
            client = DoubaoGPTAPI(
                api_key=self.api_key,
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature)
            log_info = f"Create default DoubaoGPTAPI success! model: {self.model}"
            self.log_server.write_log(log=LogModel(log_info, "INFO"))
            return client

    