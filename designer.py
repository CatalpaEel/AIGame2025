from openai import OpenAI
import time

from api_key import deepseek_api_key

deepseek_base_url = "https://api.deepseek.com"

class ActivityDesigner:
    """
    Design activities based on user input using Deepseek API.
    """
    def __init__(self):
        self.client = OpenAI(api_key=deepseek_api_key, base_url=deepseek_base_url)
        self.system_prompt = """
        你是一名活动设计师。
        你需要根据用户提供的活动信息，设计详细的活动策划案，包括活动流程和时间安排建议等。不要输出多余信息。
        如果是竞赛类活动请深度思考并详细设计合理的赛题、规则与评分标准。
        """
        
    def design_activity(self, input, output=None, log=None):
        start_time = time.time()
        print("活动策划开始...")
        response = self.client.chat.completions.create(
            model = "deepseek-reasoner",
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": input},
            ],
            stream = False
        )
        end_time = time.time()
        print(f"活动策划完成，用时：{round(end_time-start_time, 2)}s")

        if log is not None:
            with open(f"{output}/log", "w", encoding="utf-8") as f:
                print(f"活动策划案思考过程：\n{response.choices[0].message.reasoning_content}\n", file=f)
                print(f"生成活动策划案：\n{response.choices[0].message.content}\n", file=f)

        if output is not None:
            with open(f"{output}/活动策划案.txt", "w", encoding="utf-8") as f:
                print(response.choices[0].message.content, file=f)

        return response.choices[0].message.content


if __name__ == "__main__":
    input_agent = ActivityDesigner()
    input_text = "{'type': '比赛', 'subject': 'AI与大模型', 'schedule': '给定数据集和基本的代码，让选手调参', 'objective': '系统性解析大模型技术演进脉络，探讨自然语言处理、多模态学习等领域的最新突破；构建开放交流场域，促进学术界与产业界在算力优化、数据治理、伦理规范等关键议题上的协同创新；激发青年学子技术热忱，通过案例剖析与实战工作坊培养复合型AI人才，助力国家人工智能战略与交叉学科创新发展', 'scale': '待定', 'time': '4月下旬：大模型训练挑战赛预热推送&报名推送，5月中旬：大模型训练挑战赛总结推送', 'place': '北京大学信息科学技术学院', 'cooperation': 'Linux社'}"
    design = input_agent.design_activity(input_text)
    print(design)