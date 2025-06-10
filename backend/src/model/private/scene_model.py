#!/usr/bin/env python3
#! -* coding: utf-8 -*-

import json
from pydantic import BaseModel

class Scene(BaseModel):
    code: str
    label_name: str
    group_name: str
    selected: bool = False
    disabled: bool = False

    def __repr__(self):
        return f"Scene(code={self.code}, label_name={self.label_name}, group_name={self.group_name}, selected={self.selected}, disabled={self.disabled})"

    def to_dict(self):
        return {
            "code": self.code,
            "label_name": self.label_name,
            "group_name": self.group_name,
            "selected": self.selected,
            "disabled": self.disabled
        }
        
    def to_json(self):
        return json.dumps(self.to_dict())
    
    