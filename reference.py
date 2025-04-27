from openai import OpenAI
import json

from api_key import deepseek_api_key, deepseek_base_url

class ReferenceAnalyst:
    
    def __init__(self):
        self.client = OpenAI(api_key=deepseek_api_key, base_url=deepseek_base_url)
        self.system_prompt = """
        ???
        """

    def analyze_reference(self, input_text):
        response = self.client.chat.completions.create(
            model = "deepseek-chat",
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": input_text},
            ],
            response_format = { "type": "json_object" },
            stream = False
        )
        return json.loads(response.choices[0].message.content)


class ReferenceSummarizer:

    def __init__(self):
        self.client = OpenAI(api_key=deepseek_api_key, base_url=deepseek_base_url)
        self.system_prompt = """
        ???
        """

    def summarize_reference(self, input_text):
        response = self.client.chat.completions.create(
            model = "deepseek-chat",
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": input_text},
            ],
            response_format = { "type": "json_object" },
            stream = False
        )
        return json.loads(response.choices[0].message.content)
        
    
if __name__ == "__main__":
    reference_analyst = ReferenceAnalyst()
    reference_summarizer = ReferenceSummarizer()
    
    # TODO
    # 数据在datatvss_txt目录里面
    # 保存到reference.json文件，协调好格式