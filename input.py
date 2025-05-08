from openai import OpenAI
import json
import time

from api_key import deepseek_api_key

deepseek_base_url = "https://api.deepseek.com"

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

    def analyze_input(self, input, output=None, log=None):
        start_time = time.time()
        print("输入分析开始...")
        response = self.client.chat.completions.create(
            model = "deepseek-chat",
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": input},
            ],
            response_format = { "type": "json_object" },
            stream = False
        )
        end_time = time.time()
        print(f"输入分析完成，用时：{round(end_time-start_time, 2)}s")

        if log is not None:
            with open(f"{output}/log", "w", encoding="utf-8") as f:
                print(f"输入分析：\n{response.choices[0].message.content}\n", file=f)

        if output is not None:
            with open(f"{output}/输入分析.txt", "w", encoding="utf-8") as f:
                print(response.choices[0].message.content, file=f)

        return json.loads(response.choices[0].message.content)


if __name__ == "__main__":
    input_agent = InputAnalyst()
    input_text = """
    学长您好，学生会这学期拟举行一个大模型相关的比赛，目前的想法是调参赛（给定数据集和基本的代码，让选手调参）。想请问你们Linux社是否能接下出题的任务[可怜][可怜][可怜]

    北京大学信息科学技术学院举办"AI与大模型"主题活动，旨在搭建产学研深度对话平台，通过前沿技术分享、应用场景探讨与跨学科思维碰撞，推动大模型技术的创新突破与落地实践。

    活动聚焦三大核心目标：
    一是系统性解析大模型技术演进脉络，探讨自然语言处理、多模态学习等领域的最新突破；
    二是构建开放交流场域，促进学术界与产业界在算力优化、数据治理、伦理规范等关键议题上的协同创新；
    三是激发青年学子技术热忱，通过案例剖析与实战工作坊培养复合型AI人才，助力国家人工智能战略与交叉学科创新发展。

    工作安排：4月下旬：大模型训练挑战赛预热推送&报名推送，5月中旬：大模型训练挑战赛总结推送
    """
    analysis_result = input_agent.analyze_input(input_text)
    print(analysis_result)