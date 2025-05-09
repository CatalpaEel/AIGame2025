import threading
import time
import json
import sys
import os

from input import InputAnalyst
from designer import ActivityDesigner
from writer import ArticleWriter, MailWriter, TextWriter, MediaWriter
from image import ImagePrompter, ImageGenerator
from reference import Retriever

# Input
if len(sys.argv) != 2:
    print("Usage: python main.py <input_path>")
    sys.exit(1)
input_path = sys.argv[1]

with open(input_path, "r", encoding='utf-8') as f:
    input = f.read()

# Output path
output_path = f"./output/output_{int(time.time())}"
log_path = f"{output_path}/log"

if not os.path.exists(output_path):
    os.makedirs(output_path)

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

# Retrieve the context
context = rag_agent.retrieve(input, log_path)

# Analyze the input string
analysis = input_agent.analyze_input(input, context, output_path, log_path)

# Write part
def write():
    # Design activities
    design = design_agent.design_activity(analysis, context, output_path, log_path)

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