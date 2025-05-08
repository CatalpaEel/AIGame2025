import base64
import time
import json

from volcengine.visual.VisualService import VisualService
from openai import OpenAI

from api_key import doubao_access_key, doubao_secret_key, deepseek_api_key

class ImageGenerator:
    """
    Generate Image using Doubao Api
    """
    def __init__(self):
        self.visual_service = VisualService()
        self.visual_service.set_ak(doubao_access_key)
        self.visual_service.set_sk(doubao_secret_key)
        
    def generate_image(self, prompt, output, width=1024, height=768):
        start_time = time.time()
        print("主视觉生成开始...")
        form = {
            "req_key": "jimeng_high_aes_general_v21_L",
            "prompt": prompt,
            "width": width,
            "height": height,
        }
        response = self.visual_service.cv_process(form)
        image = base64.b64decode(response['data']['binary_data_base64'][0])
        end_time = time.time()
        print(f"主视觉生成完成，用时{round(end_time-start_time, 2)}s")
        if image is not None:
            with open(f"{output}/image.png", "wb") as f:
                f.write(image)


class ImagePrompter:
    """
    Generate prompt for ImageGenerator
    """
    def __init__(self):
        self.client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
        self.system_prompt = """
        你是一位大模型提示词生成专家。学生会将要举办一次活动，请根据用户的需求编写一个文生图模型的提示词，来指导大模型进行活动宣传海报的生成。
        用户会给出需求。不要出现“北京大学”等现实中的名称，不要输出提示词外的多余信息。
        下面是一些提示词模板，你需要仿照其风格：
        """
        
    def generate_prompt(self, input, reference, log=None):
        start_time = time.time()
        print("文生图提示词生成开始...")
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": self.system_prompt + reference},
                {"role": "user", "content": input},
            ],
            stream=False
        )
        end_time = time.time()
        print(f"文生图提示词生成完成，用时：{round(end_time-start_time, 2)}s")
        prompt = response.choices[0].message.content
        if log is not None:
            with open(log, "a", encoding='utf-8') as f:
                print(f"文生图提示词：\n{prompt}\n", file=f)
        return prompt


if __name__ == "__main__":
    # Example
    prompter = ImagePrompter()
    painter = ImageGenerator()

    input_text = "AI与大模型比赛"

    with open("../image_reference/img_ref.json", "r", encoding='utf-8') as f:
        ref_json = json.loads(f.read())
    
    reference = ""
    for ref in ref_json:
        reference += ref["name"] + ': ' + ref["prompt"] + '\n'
    
    prompt = prompter.generate_prompt(input_text, reference)

    path = f'../debug/image_{int(time.time())}.png'
    image = painter.generate_image(prompt=prompt, path=path, width=1024, height=768)
