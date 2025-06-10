#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import json
from pydantic import BaseModel


class UserInfo(BaseModel):
    id: str
    user_name: str
    user_password: str
    token: str
    user_folder_path: str
        
    def __str__(self):
        return f"UserInfo(id={self.id}, user_name={self.user_name}, user_password={self.user_password}, token={self.token}, user_folder_path={self.user_folder_path})"
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
    def to_dict(self) -> dict:
        return self.__dict__
        
        