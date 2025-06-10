import json
import sys

# 从标准输入读取数据
input_data = json.loads(sys.stdin.read())

data = "原先自己使用历史速度计算acc，目前感知已给出，直接使用，主要关注：1. 前车刹车不及时的问题，前车acc不对导致的点刹问题"


print(json.dumps({"key": input_data, "data": data}, ensure_ascii=False))
