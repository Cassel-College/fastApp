#! /usr/bin/env python3

from src.tools.public.datatime_tools.datatime_tools import DatetimeTools


class LogModel:
    def __init__(self, log_info: str, level: str="INFO"):
        self.log_info = log_info
        self.level = level
        self.date_time = DatetimeTools().get_now_YYYY_MM_DD_HH_MM_SS()
        
        
    def get_log_info(self) -> str:
        return self.log_info
    
    def set_log_info(self, log_info: str):
        self.log_info = log_info
        
    def get_log_file_path(self) -> str:
        return self.log_file_path
    
    def set_log_file_path(self, log_file_path: str):
        self.log_file_path = log_file_path
    
    def get_date_time(self) -> str:
        return self.date_time
    
    def gen_log_info(self) -> str:
        return f"{self.level}: \t{self.date_time} {self.log_info}"
        
    
    