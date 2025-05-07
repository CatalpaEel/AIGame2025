#这个项目实现根据活动策划案生成一个媒体宣传文案，让我们能够给活动在社交媒体进行宣传

from openai import OpenAI
import json
import writer
from api_key import deepseek_api_key

deepseek_base_url = "https://api.deepseek.com"

class MediaTextDesigner:
    """
    Design media text based on ActivityDesigner using Deepseek API.
    """
    def __init__(self):
        pass # TODO
        self.client = OpenAI(api_key=deepseek_api_key, base_url=deepseek_base_url)
        self.system_prompt = """
        你是北京大学信息科学学院学生会的一名经验丰富的同学。
        你将要帮助用户解析出活动的显性信息（活动类型、主题方向、初步构想等），并通过推理补全隐性信息（隐性信息：目标受众、活动规模、时间安排、可能的合作方等）。
        系统应自主判断并补全信息缺失项，无需用户额外输入。 
        输入为之前生成的活动策划案，包含以下内容：
        {
            如果是竞赛类活动策划案，则按照以下的要求：
            {    "type": "比赛",
                "subject": "人工智能应用创新大赛",
                "schedule": {
                "competition question design": [
                    "初赛：基于公开数据集的图像分类模型优化（限时72小时）",
                    "复赛：多模态数据融合的智能客服系统设计（提交技术方案与原型演示）",
                    "决赛：现场命题开发（智慧校园场景应用开发，8小时限时编程）"
                ],
                "grading criteria": {
                    "技术创新性": 30,
                    "功能完整性": 25,
                    "代码规范性": 20,
                    "商业价值": 15,
                    "现场答辩": 10
                },
                "activity process": [
                    "09:00-09:30 开幕式（院士致辞）",
                    "09:30-12:00 初赛作品提交",
                    "14:00-17:00 复赛方案展示",
                    "次日09:00-17:00 决赛开发与评审"
                ]
                },
                "objective": "培养AI工程实践能力，推动产学研合作",
                "scale": 200,
                "time": "2023年11月15日-11月17日",
                "place": "北京大学王克桢楼智能实验室",
                "cooperation": [
                    "百度AI实验室",
                    "中国人工智能学会",
                    "北京大学学生科协"
                ],
                "resourves requriment": [
                    "GPU服务器集群",
                    "数据集存储设备",
                    "评委专家5人",
                    "学生志愿者20人"
                ],
                "propaganda strategy": {
                "online": [
                    "微信小程序报名系统",
                    "B站技术预热直播（3场）",
                    "知乎专题讨论区"
                ],
                "offline": [
                    "三角地桁架海报（主视觉：神经元网络与燕园建筑融合）",
                    "教学楼电子屏轮播（包含往届优秀作品展示）"
                ]
                },
                "visual design": {
                    "海报文案": "「智汇燕园」第三届AI创新挑战赛",
                    "流程图": "报名→线上培训→初赛→复赛→决赛→颁奖典礼",
                    "宣传视频": "30秒快剪（往届选手访谈+技术应用场景模拟）"
                }
            }

            如果是非竞赛类活动策划案: {
                "type": "学术讲座",
                "subject": "区块链技术前沿与应用实践",
                "schedule": {
                "lecture content": [
                    "14:00-14:10 主持人开场",
                    "14:10-15:30 主旨演讲（央行数字货币研究所专家）",
                    "15:30-16:00 案例工作坊（分组模拟智能合约开发）",
                    "16:00-16:30 互动问答（线上线下同步进行）"
                ]
                },
                "objective": "普及区块链核心技术，探讨数字经济新基建",
                "scale": 150,
                "time": "2023年10月25日 14:00-17:00",
                "place": "二教301智慧教室",
                "cooperation": [
                    "微众银行区块链事业部",
                    "北京大学金融科技研究院"
                ],
                "resources requriment": [
                    "区块链沙盒实验平台",
                    "多机位直播设备",
                    "同声传译系统",
                    "茶歇物资（50人份）"
                ],
                "propaganda strategy": {
                "定向邀请": [
                    "计算机学院、光华管理学院研究生",
                    "金融科技社团成员"
                ],
                "public spread": [
                    "未名BBS置顶帖（含预习资料包）",
                    "学习通平台同步直播"
                ]
                },
                "visual design": {
                    "海报主视觉": "立体化的区块链节点与未名湖倒影",
                    "互动环节": "现场生成NFT数字纪念证书",
                    "宣传亮点": "会后建立持续交流的学术社群"
                }
                }
            }
        }
        输出为解析后的活动信息，要求格式为可以推送给参加比赛的用户的邮件内容，包含以下内容：
        {
                        {
                "social_media_post": {
                    "platform": ["微信公众号", "微博话题", "B站动态"],
                    "header": "🔥【48小时AI极限挑战】北大智能实验室喊你来战！",
                    "content": [
                        "📢「#智汇燕园AI创新赛」震撼来袭！",
                        "🎯 三大硬核关卡：",
                        "   ▫️ 72H图像分类优化战（ImageNet暴风训练）",
                        "   ▫️ 多模态客服系统开发（语音+文本双模态融合）",
                        "   ▫️ 8小时智慧校园场景编程（百度真实项目对接）",
                        
                        "💎 参赛即得：",
                        "   ✅ 百度AIGC内推绿色通道",
                        "   ✅ 阿里云千元算力礼包",
                        "   ✅ 定制版《PyTorch工程化指南》",
                        
                        "🚀 技术buff加成：",
                        "   ✨ NVIDIA V100集群火力全开",
                        "   ✨ CCF论文收录快速通道",
                        "   ✨ 院士领衔导师天团",
                        
                        "📅 时间轴：",
                        "   11.10 报名截止 → 11.15-17 巅峰对决",
                        "📍 坐标：王克桢楼智能实验室（支持远程接入）",
                        
                        "🎁 隐藏福利：",
                        "   决赛现场抽签赠送【Jetson Nano开发套件】×3！",
                        
                        "👇 即刻行动：",
                        "   微信扫码 → 填写GitHub账号 → 组队开战",
                        "   （报名二维码动态嵌入）"
                    ],
                    "visual_elements": {
                        "封面图": "赛博朋克风格燕园建筑+神经网络流光特效",
                        "视频预告": "B站AV号：BV1Mz421g7E3（含往届选手炫技片段）",
                        "互动组件": [
                            "#AI工程师养成计划 话题互动",
                            "转发抽奖：华为MatePad × 2"
                        ]
                    },
                    "hashtags": [
                        "#北京大学人工智能大赛",
                        "#多模态技术实战",
                        "#产学研创新实验室",
                        "#第二课堂学分认证"
                    ],
                    "tech_features": {
                        "智能匹配": "H5页面自动组队系统",
                        "云端沙盒": "百度大脑AI Studio在线开发环境",
                        "评审追踪": "区块链技术存证评分过程"
                    }
                }
            }
     }
                
                
                """
        
    def design_media_text(self, input_text):
         response = self.client.chat.completions.create(
            model = "deepseek-chat",
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": input_text},
            ],
            stream = False
        )
         return response.choices[0].message.content

class MediaTextWriter:
    """
    Write media text based on user input and reference data using Deepseek API.
    """
    def __init__(self):
        pass # TODO


if __name__ == "__main__":
    #邮件设计的类
    input_agent = MediaTextDesigner()
    #调用活动策划案的类来生成活动策划案
    activity_result=writer.ActivityDesigner()
    input_text =activity_result.design_activity( "{'type': '比赛', 'subject': 'AI与大模型', 'schedule': '给定数据集和基本的代码，让选手调参', 'objective': '系统性解析大模型技术演进脉络，探讨自然语言处理、多模态学习等领域的最新突破；构建开放交流场域，促进学术界与产业界在算力优化、数据治理、伦理规范等关键议题上的协同创新；激发青年学子技术热忱，通过案例剖析与实战工作坊培养复合型AI人才，助力国家人工智能战略与交叉学科创新发展', 'scale': '待定', 'time': '4月下旬：大模型训练挑战赛预热推送&报名推送，5月中旬：大模型训练挑战赛总结推送', 'place': '北京大学信息科学技术学院', 'cooperation': 'Linux社'}")
    
    analysis_result = input_agent.design_media_text(input_text)
    print(analysis_result)

    # TODO

    # 数据从reference.json文件里面读，协调好格式

