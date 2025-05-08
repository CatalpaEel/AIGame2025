import threading
import time
import json

from input import InputAnalyst
from designer import ActivityDesigner
from writer import ArticleWriter, MailWriter, TextWriter, MediaWriter
from image import ImagePrompter, ImageGenerator
from reference import Retriever

# Output path
output_path = "./output"
log_path = "./output/log"

# Initialize the agents
start_time = time.time()
print("系统开始运行...")

input_agent = InputAnalyst()
design_agent = ActivityDesigner()

rag_agent = Retriever()

article_agent = ArticleWriter()
mail_agent = MailWriter()
text_agent = TextWriter()
media_agent = MediaWriter()

prompter_agent = ImagePrompter()
image_agent = ImageGenerator()


input = """
学长您好，学生会这学期拟举行一个大模型相关的比赛，目前的想法是调参赛（给定数据集和基本的代码，让选手调参）。想请问你们Linux社是否能接下出题的任务[可怜][可怜][可怜]

北京大学信息科学技术学院举办"AI与大模型"主题活动，旨在搭建产学研深度对话平台，通过前沿技术分享、应用场景探讨与跨学科思维碰撞，推动大模型技术的创新突破与落地实践。

活动聚焦三大核心目标：
一是系统性解析大模型技术演进脉络，探讨自然语言处理、多模态学习等领域的最新突破；
二是构建开放交流场域，促进学术界与产业界在算力优化、数据治理、伦理规范等关键议题上的协同创新；
三是激发青年学子技术热忱，通过案例剖析与实战工作坊培养复合型AI人才，助力国家人工智能战略与交叉学科创新发展。

工作安排：4月下旬：大模型训练挑战赛预热推送&报名推送，5月中旬：大模型训练挑战赛总结推送
"""

# Retrieve the context
context = rag_agent.retrieve(input, log_path)

# Analyze the input string
analysis = input_agent.analyze_input(input, context, output_path, log_path)

# Write part
def write():
    # Design activities
    design = design_agent.design_activity(analysis, output_path, log_path)

    # Write complete set of promotional copy through multithreading
    article_thread = threading.Thread(target=article_agent.write_article, args=(design, output_path, log_path))
    mail_thread = threading.Thread(target=mail_agent.write_mail, args=(design, output_path, log_path))
    text_thread = threading.Thread(target=text_agent.write_text, args=(design, output_path, log_path))
    media_thread = threading.Thread(target=media_agent.write_media, args=(design, output_path, log_path))

    article_thread.start()
    mail_thread.start()
    text_thread.start()
    media_thread.start()

    article_thread.join()
    mail_thread.join()
    text_thread.join()
    media_thread.join()

# Image part
def image():
    # Load reference
    with open("./ref/img_ref.json", "r", encoding='utf-8') as f:
        ref_json = json.loads(f.read())
    
    reference = ""
    for ref in ref_json:
        reference += ref["name"] + ': ' + ref["prompt"] + '\n'
    with open(log_path, "a", encoding='utf-8') as f:
        print(f"参考提示词：\n{reference}\n", file=f)
    
    # Generate prompt
    prompt = prompter_agent.generate_prompt(analysis, reference, log_path)

    # Generate image
    image = image_agent.generate_image(prompt, output_path)

write_thread = threading.Thread(target=write)
image_thread = threading.Thread(target=image)

write_thread.start()
image_thread.start()

write_thread.join()
image_thread.join()

# Complete
end_time = time.time()
print(f"系统运行完毕，输出文件保存至{output_path}，日志文件保存至{log_path}，总用时：{round(end_time-start_time, 2)}s")