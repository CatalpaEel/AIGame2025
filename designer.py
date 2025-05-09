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
        
    def design_activity(self, input, context, output=None, log=None):
        start_time = time.time()
        print("活动策划开始...")
        response = self.client.chat.completions.create(
            model = "deepseek-reasoner",
            messages = [
                {"role": "system", "content": self.system_prompt + f"下面是一些过去活动的context片段：{context}"},
                {"role": "user", "content": input},
            ],
            stream = False
        )
        end_time = time.time()
        print(f"活动策划完成，用时：{round(end_time-start_time, 2)}s")

        if log is not None:
            with open(f"{log}", "a", encoding="utf-8") as f:
                print(f"活动策划案思考过程：\n{response.choices[0].message.reasoning_content}\n", file=f)
                print(f"生成活动策划案：\n{response.choices[0].message.content}\n", file=f)

        if output is not None:
            with open(f"{output}/活动策划案.txt", "w", encoding="utf-8") as f:
                print(response.choices[0].message.content, file=f)

        return response.choices[0].message.content


if __name__ == "__main__":
    input_agent = ActivityDesigner()
    input_text = """
    活动类型：比赛  
    主题方向：大模型训练与调参  
    初步构想：参赛选手将获得给定的数据集和基础代码框架，主要任务是通过调整模型参数、优化训练策略等方式提升模型性能。比赛将设置多个评估指标（如准确率、F1分数等），最终根据模型在测试集上的表现进行排名。比赛分为初级和高级两个赛道，初级赛道提供更详细的指导文档和基线模型，高级赛道则更具挑战性，鼓励创新性调参方法。  
    活动目的：提高学生的大模型实践能力，促进学术交流，激发对AI技术的兴趣  
    活动规模：100人  
    时间安排：2025年5月10日至2025年5月20日  
    活动地点：信息科学技术学院机房  
    主办方与合作方：北京大学信息科学技术学院学生会（主办方）、北京大学学生Linux俱乐部（合作方，负责出题和技术支持）
    """

    context = """
    2025信息科学技术学院新年晚会将于12月21日晚7点在中关新园群英厅举行，节目包括歌曲、魔术、配音、舞蹈等，到场观众可领取新年限定礼品。
    北京大学第二十三届“九坤杯”程序设计竞赛报名开启，比赛时间为5月18日，采用ACM赛制，面向全体在校学生。获奖选手有机会获得课程加分和实习机会，报名截止时间为5月13日晚23:59。
    信科青协“信”心行动学业辅导项目招募讲师和学生报名，提供高数、线代、电磁学等课程辅导。讲师需满足相关条件，劳务300元/小时。学生报名截止时间为4月3日晚23:59，辅导形式以 线下串讲为主。
    华为北京研究所参访活动于3月15日举行，面向全体北大本科生和研究生，活动包括技术展厅参观、座谈交流和餐厅就餐。报名需扫描二维码，名额有限。
    颁奖典礼将于2025年春季学期开学后在北京大学线下举行。主办单位为北京大学计算中心，联合主办包括北京大学计算机学院、北京大学信息科学技术学院和北京大学长沙计算与数字经济研究院。承办单位为北京大学学生Linux俱乐部和北京大学未名超算队。协办组织包括上科大GeekPie_HPC、东南大学Linux俱乐部、南昌大学NCUSCC俱乐部等。
    赛程安排如下：赛题将于4月26日发布。入门讲座计划在5月1日左右举行，适合零基础参与者，提供回放和文字版教程。结果提交截止时间为5月7日（高级赛道）和5月9日（初级赛道）。 颁奖仪式定于5月10日举行。
    比赛设有两个赛道：初级赛道主题为大信科活动规划与宣传智能系统，高级赛道主题为文生图模型微调。报名后可在题库查看赛题，高级赛道需先完成第一题并创建算力账号。
    """
    design = input_agent.design_activity(input_text, context)
    print(design)