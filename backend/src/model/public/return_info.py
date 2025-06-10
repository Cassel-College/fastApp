#!/usr/bin/env python3
#! -* coding: utf-8 -*-

from pydantic import BaseModel
from typing import Any


class ReturnCode:
    SUCCESS = 0
    FAILED = 1

class ReturnInfo(BaseModel):
    code: int
    message: str
    data: Any

    @classmethod
    def create(cls, code: int, message: str, data: dict = {}) -> 'ReturnInfo':
        return cls(code=code, message=message, data=data)

    def get_code(self) -> int:
        return self.code
    
    def get_message(self) -> str:
        return self.message
    
    def get_data(self):
        return self.data
    
    def set_code(self, code: int):
        self.code = code
    
    def set_message(self, message: str):
        self.message = message
    
    def set_data(self, data: dict = {}):  
        self.data = data
        
    def add_data(self, key: str, value: Any):
        self.data[key] = value
    
    def get_return_info(self) -> dict:
        return self.dict()