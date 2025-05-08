from openai import OpenAI
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
        你是一名需求解析专家。
        你将要帮助用户解析出活动的显性信息（活动类型、主题方向、初步构想等），并通过推理补全隐性信息（隐性信息：目标受众、活动规模、时间安排、可能的合作方等）。
        如有信息缺失，请自行补充，尽量具体。
        输出包含以下内容，请不要输出多余提示信息。
        活动类型：讲座、比赛、展览等
        主题方向：人工智能、区块链等）
        初步构想：详细的比赛规则等
        活动目的：提高学生的专业技能、促进学术交流等
        活动规模：50人、200人等
        时间安排：2025年10月1日、2025年10月1日至2025年10月5日等（当前年份为2025年）
        活动地点：信息科学技术学院、某某教室等
        主办方与合作方：某某公司、某某学校、其他学院、社团等
        """

    def analyze_input(self, input, context, output=None, log=None):
        start_time = time.time()
        print("输入分析开始...")
        response = self.client.chat.completions.create(
            model = "deepseek-chat",
            messages = [
                {"role": "system", "content": self.system_prompt + f"下面是一些过去活动的context片段：{context}"},
                {"role": "user", "content": input},
            ],
            stream = False
        )
        end_time = time.time()
        print(f"输入分析完成，用时：{round(end_time-start_time, 2)}s")

        if log is not None:
            with open(f"{log}", "a", encoding="utf-8") as f:
                print(f"输入分析：\n{response.choices[0].message.content}\n", file=f)

        return response.choices[0].message.content


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

    context = """
    2025信息科学技术学院新年晚会将于12月21日晚7点在中关新园群英厅举行，节目包括歌曲、魔术、配音、舞蹈等，到场观众可领取新年限定礼品。
北京大学第二十三届“九坤杯”程序设计竞赛报名开启，比赛时间为5月18日，采用ACM赛制，面向全体在校学生。获奖选手有机会获得课程加分和实习机会，报名截止时间为5月13日晚23:59。
信科青协“信”心行动学业辅导项目招募讲师和学生报名，提供高数、线代、电磁学等课程辅导。讲师需满足相关条件，劳务300元/小时。学生报名截止时间为4月3日晚23:59，辅导形式以 线下串讲为主。
华为北京研究所参访活动于3月15日举行，面向全体北大本科生和研究生，活动包括技术展厅参观、座谈交流和餐厅就餐。报名需扫描二维码，名额有限。
颁奖典礼将于2025年春季学期开学后在北京大学线下举行。主办单位为北京大学计算中心，联合主办包括北京大学计算机学院、北京大学信息科学技术学院和北京大学长沙计算与数字经济研究院。承办单位为北京大学学生Linux俱乐部和北京大学未名超算队。协办组织包括上科大GeekPie_HPC、东南大学Linux俱乐部、南昌大学NCUSCC俱乐部等。
赛程安排如下：赛题将于4月26日发布。入门讲座计划在5月1日左右举行，适合零基础参与者，提供回放和文字版教程。结果提交截止时间为5月7日（高级赛道）和5月9日（初级赛道）。 颁奖仪式定于5月10日举行。
比赛设有两个赛道：初级赛道主题为大信科活动规划与宣传智能系统，高级赛道主题为文生图模型微调。报名后可在题库查看赛题，高级赛道需先完成第一题并创建算力账号。
    """
    analysis_result = input_agent.analyze_input(input_text, context)
    print(analysis_result)