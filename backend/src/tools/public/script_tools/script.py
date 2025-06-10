import json
import sys

# 从标准输入读取数据
input_data = json.loads(sys.stdin.read())
print(json.dumps({"status": "received", "data": input_data}))
