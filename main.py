from openai import OpenAI
import json

from api_key import deepseek_api_key, deepseek_base_url

class InputAnalyst:
    """
    Analyze user input and extract event information using Deepseek API.
    """

    def __init__(self):
        self.client = OpenAI(api_key=deepseek_api_key, base_url=deepseek_base_url)
        self.system_prompt = """
        你是北京大学信息科学学院学生会的一名经验丰富的同学。
        你将要帮助用户解析出活动的显性信息（活动类型、主题方向、初步构想等），并通过推理补全隐性信息（隐性信息：目标受众、活动规模、时间安排、可能的合作方等）。
        系统应自主判断并补全信息缺失项，无需用户额外输入。
        输出格式为json字符串，包含以下字段：
        - type: 活动类型（如：讲座、比赛、展览等）
        - subject: 主题方向（如：人工智能、区块链等）
        - schedule: 初步构想（如：详细的比赛规则等）
        - objective: 活动目的（如：提高学生的专业技能、促进学术交流等）
        - scale: 活动规模（如：50人、200人等）
        - time: 时间安排（如：2023年10月1日、2023年10月1日至2023年10月5日等）
        - place: 活动地点（如：信息科学技术学院、某某教室等）
        - cooperation: 可能的合作方（如：某某公司、某某学校、其他学院、社团等）
        """

    def analyze_input(self, input_text):
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


class ActivityDesigner:
    """
    Design activities based on user input using Deepseek API.
    """
    def __init__(self):
        pass # TODO


class ArticleWriter:
    """
    Write articles based on user input and reference data using Deepseek API.
    """
    def __init__(self):
        pass # TODO


if __name__ == "__main__":
    input_agent = InputAnalyst()
    # activity_agent = ActivityDesigner()
    # article_agent = ArticleWriter()
    input_text = ""
    input_text = input("Enter your input (or 'exit' to quit): ")
    analysis_result = input_agent.analyze_input(input_text)
    print(analysis_result)

    # TODO

    # 数据从reference.json文件里面读，协调好格式

