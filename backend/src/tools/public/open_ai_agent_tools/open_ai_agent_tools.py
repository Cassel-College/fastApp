import openai

class ChatGPTAPI:
    def __init__(self, model="gpt-4", max_tokens=1000, temperature=0.7):
        """
        初始化 ChatGPTClient 类。
        
        :param model: 使用的模型名称，默认是 gpt-4。
        :param max_tokens: 每次响应的最大 token 数，默认为 1000。
        :param temperature: 控制生成的随机性，默认是 0.7。
        """
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    def chat(self, api_key, prompt):
        """
        与 OpenAI API 交互的函数。
        
        :param api_key: OpenAI API 密钥。
        :param prompt: 用户输入的提示信息。
        :return: ChatGPT 的响应。
        """
        # 动态设置 API 密钥
        openai.api_key = api_key
        
        try:
            # 发起 API 请求
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are ChatGPT, a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            # 提取并返回响应内容
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"An error occurred: {str(e)}"
