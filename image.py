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
        
    def generate_image(self, prompt, path, width=1024, height=768):
        # target = [(512,512), (384,512), (512,341), (341,512), (512,288), (288,512)] # 1:1, 4:3, 3:4, 3:2, 2:3, 16:9, 9:16
        # s_width, s_height = min(target, key=lambda x: abs(width/height - x[0]/x[1])) # Find the closest preset size to make the model happy
        form = {
            "req_key": "jimeng_high_aes_general_v21_L",
            "prompt": prompt,
            "width": width,
            "height": height,
        }
        response = self.visual_service.cv_process(form)
        image = base64.b64decode(response['data']['binary_data_base64'][0])
        print(f"主视觉已生成，保存路径: {path}")
        if image is not None:
                with open(path, "wb") as file:
                    file.write(image)


class ImagePrompter:
    """
    Generate prompt for ImageGenerator
    """
    def __init__(self):
        self.client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
        self.system_prompt = """
        你是一位大模型提示词生成专家。学生会将要举办一次活动，请根据用户的需求编写一个文生图模型的提示词，来指导大模型进行活动宣传海报的生成。
        用户会给出需求。不要出现“北京大学”等现实中的名称。
        下面是一些提示词模板，你需要仿照其风格：
        """
        
    def generate_prompt(self, input, reference):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": self.system_prompt + reference},
                {"role": "user", "content": input},
            ],
            stream=False
        )
        prompt = response.choices[0].message.content
        print(f"文生图提示词已生成: \n{prompt}")
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
