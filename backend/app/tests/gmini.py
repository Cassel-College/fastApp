import requests

api_key = "AIzaSyDJFCqAxeu3hxvZatchxPrSwQmmtg1BZqo" 
# 设置请求的 URL 和 API 密钥
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

# 定义请求头
headers = {
    "Content-Type": "application/json"
}

# 定义请求体
data = {
    "contents": [
        {
            "parts": [
                {"text": "你好！你了解自动驾驶的知识吗？我给你一些场景；你可以帮我生产一个自动驾驶测试方案吗？用表格的形式返回给我，只返回一个纵向的表格就好，不需要其他内容。，这是场景元素：白天，停车场，5-10 km/h，跟车行驶，行人在人行道，減速礼让，掉头。"}
            ]
        }
    ]
}

# 发起 POST 请求
response = requests.post(url, headers=headers, json=data)

# 解析和打印响应结果
if response.status_code == 200:
    print("Response:", response.json())
else:
    print(f"Error: {response.status_code}")
    print("Details:", response.text)
