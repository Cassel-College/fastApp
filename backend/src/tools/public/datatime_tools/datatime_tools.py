#! /usr/bin/env python3

from datetime import datetime, timedelta

class DatetimeTools:
    def __init__(self):
        pass
    
    def get_now_YYYY_MM_DD_HH_MM_SS(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_now_YYYY_MM_DD(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")
    
    def get_now_HH_MM_SS(self) -> str:
        return datetime.now().strftime("%H:%M:%S")
    
    def get_td_str(self) -> str:
        
        return self.get_now_YYYY_MM_DD_HH_MM_SS().replace(" ", "_").replace(":", "_")
    
    def td2str(self, dt: timedelta) -> str:
        
        return str(dt).replace(" ", "_").replace(":", "_")
    
    def str_to_datetime_str(self, time_str: str) -> str:
        
        parts = time_str.split("_")
        if len(parts) == 4:
            return f"{parts[0]} {parts[1]}:{parts[2]}:{parts[3]}"
        else:
            return time_str
    
    def compare_time_with_threshold(self, time1: str, time2: str, threshold_seconds: int) -> bool:
        """
        比较两个时间字符串是否第一个时间超过第二个时间指定的秒数。

        Args:
            time1 (str): 第一个时间，格式为 "YYYY-MM-DD HH:MM:SS"
            time2 (str): 第二个时间，格式为 "YYYY-MM-DD HH:MM:SS"
            threshold_seconds (int): 秒数阈值

        Returns:
            bool: 如果第一个时间比第二个时间晚超过阈值，返回 True；否则返回 False。
        """
        try:
            # 转换时间字符串为 datetime 对象
            datetime1 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
            datetime2 = datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")

            # 计算时间差
            time_difference = (datetime1 - datetime2).total_seconds()

            # 判断是否超过阈值
            return time_difference > threshold_seconds
        except ValueError as e:
            print(f"时间格式错误: {e}")
            return False
    