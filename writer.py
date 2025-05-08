import time

from openai import OpenAI

from api_key import deepseek_api_key

deepseek_base_url = "https://api.deepseek.com"

class ArticleWriter:
    """
    Write articles based on user input and reference data using Deepseek API.
    """
    def __init__(self):
        self.client = OpenAI(api_key=deepseek_api_key, base_url=deepseek_base_url)
        self.system_prompt = """
        你是一名微信公众号写作者，你需要根据活动策划案，提取关键内容，为活动通知和宣传的微信公众号撰写文案。请输出纯文本格式，不要加粗、列表等。
        例子：
        活动 | 2025年“信科杯”师生院友羽毛球比赛火热来袭！
        2025年“信科杯”师生院友羽毛球比赛
        拼搏
        热爱
        青春
        活力
        春风徐徐，春景熙熙
        恰逢期中周告一段落
        经历了半学期的忙碌学习
        是时候卸下行囊
        在羽毛球场上挥洒热忱
        在切磋较量中书写热爱
        是的，没错，它来了！
        2025年“信科杯”师生院友羽毛球比赛
        重磅来
        2025年“信科杯”羽毛球比赛
        即将到来，
        你还在犹豫什么？
        只要你热爱羽毛球，
        只要你喜欢同对手在场上激战，
        就赶紧来报名参赛吧！
        有丰厚的奖品在等着大家～
        活动简介
        比赛时间：
        4月29日（周二）
        13：00 - 17：00
        （根据具体比赛情况会有所调整）
        比赛地点：
        五四体育馆-羽毛球场
        面向对象：
        信息科学技术学院全体师生(含毕业院友)
        （主办方将对报名人员进行审核）
        比赛形式：
        1）比赛分为男单、男双、女单、女双、混双五大项目，参赛队员可根据意愿报名一个或多个项目
        2）比赛将根据报名情况采用小组赛和淘汰赛相结合的形式（具体赛制和赛程将在报名结束后通知各位运动员）
        注意事项：
        请同学和老师们自备球拍！
        比赛奖品：
        单打奖品
        一等奖:
        尤尼克斯羽毛球包
        二等奖:
        尤尼克斯AS-9羽毛球
        三等奖:
        小黄鸭颈椎按摩器
        双打奖品
        一等奖:
        尤尼克斯AS-9羽毛球
        二等奖:
        米小舒午睡枕
        三等奖:
        尤尼克斯运动毛巾
        报名方式
        请有意愿报名参加比赛的
        老师，院友，同学们
        扫描下方二维码填写问卷并加入选手群
        （问卷中附有选手群二维码）
        若报名双打需要填写搭档信息
        （双打队伍一人填写即可）
        请于4月27日(周日)晚23:59前
        扫描下方二维码填写问卷
        只要热爱，永远都是当打之年
        只要向前，何处都是风光无限
        只要专注，输赢都是一场历练
        在这里
        探索
        追寻
        较量
        欣赏
        欢迎大家报名！
        一起拥抱金色汗水的春天和夏天！
        主办方 | 信科团委文体中心
        """

    def write_article(self, input, output=None, log=None):
        start_time = time.time()
        print("微信公众号文案写作开始...")
        response = self.client.chat.completions.create(
            model = "deepseek-chat",
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": input},
            ],
            stream = False
        )
        end_time = time.time()
        print(f"微信公众号文案写作完成，用时：{round(end_time-start_time, 2)}s")

        if log is not None:
            with open(f"{log}", "a", encoding="utf-8") as f:
                print(f"生成微信公众号文案：\n{response.choices[0].message.content}\n", file=f)

        if output is not None:
            with open(f"{output}/微信公众号文案.txt", "w", encoding="utf-8") as f:
                print(response.choices[0].message.content, file=f)

        return response.choices[0].message.content


class MailWriter:
    def __init__(self):
        self.client = OpenAI(api_key=deepseek_api_key, base_url=deepseek_base_url)
        self.system_prompt = """
        你是一名公文写作者，你需要根据活动策划案，提取关键内容，写一封邮件格式的文案，作为活动的通知和宣传。请输出纯文本格式，不要加粗、列表等。

        下面是一个例子：
        标题：“信谈1024”| 活动报名：信科党政班子师生面对面活动【2025年第六期（总第36期）】
        正文：
        “信谈1024”信科党政班子师生面对面是信息科学技术学院师生交流品牌活动。“1024”是2的10次方，这个和二进制相关的数字为信息学科师生所熟悉，首期活动于2023年3月10日举办，并固定在每月的10日及24日开展。通常每月10日为个人单独面谈，每月24日为多人团体座谈。活动提供不同形式，旨在围绕学院人才培养中心工作，通过搭建学院党政班子和全院师生的日常面对面交流平台，广泛听取意见建议，破解学院发展难题，力求解决师生中长期存在的困惑或问题，凝聚共识，勠力同心，推进学院更好更快发展。
        一、 活动主题：
        “信谈1024”信科党政班子师生面对面
        【2025年第六期（总第36期）】
        二、 活动时间：
        2025年4月24日（周四）12：00
        三、 活动地点：
        报名成功后具体通知
        四、 活动形式：
        多人团体座谈
        五、 报名方式：
        请有意参加活动的同学填写以下问卷，问卷将于4月22日23点停止。学院学工办会以填写问卷的顺序原则上分别邀请各年级前3位同学参加活动，报名成功的同学会在活动开始前一天收到确认通知。如有同学因故无法参加，将以问卷填写顺序依次顺延邀请。
        六、 特别说明
        期待学院师生在问卷中提交自己感兴趣的话题或对学院发展的意见建议，学工办会收集并分类整理，在活动中讨论和交流，现场回复参加活动的师生代表。期待大家的参与！
        北京大学信息科学技术学院
        学生工作办公室
        附：报名问卷 
        https://www.wjx.cn/vm/meL420e.aspx#

        --
        2025年4月21日
        北京大学信息科学技术学院（本科生学院）
        学生工作办公室
        """

    def write_mail(self, input, output=None, log=None):
        start_time = time.time()
        print("邮件通知写作开始...")
        response = self.client.chat.completions.create(
            model = "deepseek-chat",
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": input},
            ],
            stream = False
        )
        end_time = time.time()
        print(f"邮件通知写作完成，用时：{round(end_time-start_time, 2)}s")

        if log is not None:
            with open(f"{log}", "a", encoding="utf-8") as f:
                print(f"生成邮件通知：\n{response.choices[0].message.content}\n", file=f)

        if output is not None:
            with open(f"{output}/邮件通知.txt", "w", encoding="utf-8") as f:
                print(response.choices[0].message.content, file=f)

        return response.choices[0].message.content


class TextWriter:
    def __init__(self):
        self.client = OpenAI(api_key=deepseek_api_key, base_url=deepseek_base_url)
        self.system_prompt = """
        你是一个宣传语写作者，你需要根据用户给出的活动策划案，写一个短文本宣传语。不要输出多余信息。
        例子：
        钟声敲响，灯火可亲！新年晚会邀你共赴团圆盛宴，用歌舞点亮夜空，让欢笑填满岁末时光！
        """
    
    def write_text(self, input, output=None, log=None):
        start_time = time.time()
        print("短文本宣传语写作开始...")
        response = self.client.chat.completions.create(
            model = "deepseek-chat",
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": input},
            ],
            stream = False
        )
        end_time = time.time()
        print(f"短文本宣传语写作完成，用时：{round(end_time-start_time, 2)}s")

        if log is not None:
            with open(f"{log}", "a", encoding="utf-8") as f:
                print(f"生成短文本宣传语：\n{response.choices[0].message.content}\n", file=f)

        if output is not None:
            with open(f"{output}/短文本宣传语.txt", "w", encoding="utf-8") as f:
                print(response.choices[0].message.content, file=f)

        return response.choices[0].message.content


class MediaWriter:
    def __init__(self):
        self.client = OpenAI(api_key=deepseek_api_key, base_url=deepseek_base_url)
        self.system_prompt = """
        你是一名社交媒体写作者，你需要根据活动策划案，撰写社交媒体宣传文案。
        例子：
        🎆同学们！新年的钟声越来越近啦！属于我们的新年狂欢夜也即将闪亮登场✨！​
        这里有超燃歌舞秀💃🕺，热辣舞台点燃全场；趣味游戏大挑战🎮，惊喜礼品拿到手软；更有神秘嘉宾空降，带来意想不到的惊喜环节🎉！​
        无论你是想在舞台上绽放光芒，还是想沉浸在欢乐海洋，这里都有你的专属位置！12 月 31 日晚 7 点，北京大学第一体育场，让我们一起倒数跨年，把烦恼留在旧年，把快乐和期待带进崭新的 2024！​
        🌟快 @你的搭子，组团来嗨！评论区留言 “想去”，说不定还能解锁隐藏福利哦～​
        #新年晚会 #跨年狂欢 #一起迎接 2024
        """

    def write_media(self, input, output=None, log=None):
        start_time = time.time()
        print("社交媒体宣传文案写作开始...")
        response = self.client.chat.completions.create(
            model = "deepseek-chat",
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": input},
            ],
            stream = False
        )
        end_time = time.time()
        print(f"社交媒体宣传文案写作完成，用时：{round(end_time-start_time, 2)}s")

        if log is not None:
            with open(f"{log}", "a", encoding="utf-8") as f:
                print(f"生成社交媒体宣传文案：\n{response.choices[0].message.content}\n", file=f)

        if output is not None:
            with open(f"{output}/社交媒体宣传文案.txt", "w", encoding="utf-8") as f:
                print(response.choices[0].message.content, file=f)

        return response.choices[0].message.content


if __name__ == "__main__":
    design = """
    一、活动背景
    响应国家人工智能发展战略，依托北京大学学术资源与Linux社技术优势，搭建产学研协同创新平台。聚焦大模型核心技术突破，培养兼具理论深度与实践能力的复合型人才。

    二、赛制设计
    1. 双阶段赛程：
    - 初赛：单模态模型调优（自然语言处理）
    - 决赛：多模态联合训练（图文跨模态理解）

    2. 竞赛形式：
    - 48小时封闭式开发 + 模型迭代
    - 基于统一Pytorch框架与预训练基座模型（提供BERT、ViT等可选）

    三、时间安排
    | 阶段          | 时间节点       | 主要内容                                 |
    |---------------|----------------|------------------------------------------|
    | 预热期        | 4.20-4.25      | 官网/公众号技术解析推文                  |
    | 报名期        | 4.26-5.5       | 线上报名+组队审核                        |
    | 技术讲座      | 5.6-5.7        | Transformer架构/参数优化专题工作坊       |
    | 初赛阶段      | 5.8-5.14       | 开放训练数据集，提交模型权重文件         |
    | 决赛入围公示  | 5.15           | 公布TOP20团队                            |
    | 决赛冲刺      | 5.16-5.20      | 多模态任务挑战+技术报告撰写               |
    | 线下答辩      | 5.21           | 北京大学英杰交流中心                     |

    四、赛题设计
    1. 初赛任务：
    - 数据集：中文医疗问答文本（脱敏处理）
    - 要求：在给定计算资源内（32G VRAM）完成模型微调
    - 评估指标：F1值/推理速度/显存利用率

    2. 决赛任务：
    - 多模态数据集：医学影像+诊断报告（授权使用）
    - 挑战目标：构建跨模态检索系统
    - 创新要求：提出至少1项模型改进策略

    五、评分体系
    1. 初赛评分（100分）：
    - 模型性能（60%）：准确率、推理时延
    - 代码质量（20%）：可读性、可复现性
    - 资源效率（20%）：显存占用、训练耗时

    2. 决赛评分（120分）：
    - 技术报告（40%）：创新性、理论深度
    - 系统表现（50%）：多模态对齐能力、检索精度
    - 答辩表现（10%）：逻辑表达、技术洞察

    六、奖项设置
    - 特等奖（1队）：3万元+顶级会议推荐名额
    - 一等奖（2队）：1.5万元/队
    - 二等奖（5队）：大模型算力卡（价值5000元）
    - 最佳创新奖：定制化模型优化方案指导

    七、技术保障
    1. 计算资源：
    - 初赛：提供AWS EC2 P3实例（8节点）
    - 决赛：部署NVIDIA DGX Station集群

    2. 数据安全：
    - 联邦学习框架保障数据隐私
    - 沙箱环境运行参赛代码

    八、产学研联动
    1. 产业导师制：配备来自华为云、商汤科技等企业的技术导师
    2. 成果转化通道：优秀方案推荐至《中国人工智能学会通讯》
    3. 人才对接会：决赛期间同步举办头部AI企业招聘专场

    九、宣传矩阵
    1. 线上渠道：
    - B站技术直播：大模型前沿技术解析
    - GitHub开源社区：建立竞赛专属讨论区

    2. 线下推广：
    - 全国重点高校巡回宣讲会
    - IEEE学生分会联合推广

    十、组委会架构
    - 学术指导：北京大学人工智能研究院
    - 技术委员会：Linux社核心开发者团队
    - 运营支持：北大创新创业中心

    本方案深度融合技术挑战与人才培养，通过参数优化、多模态学习等实战环节，系统性提升参赛者的工程实践能力，同时建立产学研长效对话机制。建议后续细化计算资源分配方案与伦理审查流程，确保竞赛的公平性与安全性。
    """
    
    article_agent = ArticleWriter()
    article = article_agent.write_article(design)
    print(f"微信公众号推送稿：\n{article}\n")

    mail_agent = MailWriter()
    mail = mail_agent.write_mail(design)
    print(f"邮件通知版本：\n{mail}\n")

    text_agent = TextWriter()
    text = text_agent.write_text(design)
    print(f"短文本宣传语：\n{text}\n")

    media_agent = MediaWriter()
    media = media_agent.write_media(design)
    print(f"社交媒体分享版本：\n{media}\n")