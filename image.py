import hmac
from hashlib import sha1
import base64
import time
import uuid

import requests

from openai import OpenAI

from api_key import  liblibai_access_key, liblibai_secret_key, deepseek_api_key


class ImageGenerator:

    def __init__(self):

        self.timestamp = str(int(time.time() * 1000))
        self.signature_nonce = str(uuid.uuid4())

        text2img_url = "/api/generate/webui/text2img"
        self.text2img_url = f"https://openapi.liblibai.cloud{text2img_url}?AccessKey={liblibai_access_key}&Signature={self.make_sign(text2img_url)}&Timestamp={self.timestamp}&SignatureNonce={self.signature_nonce}"

        status_url = "/api/generate/webui/status"
        self.status_url = f"https://openapi.liblibai.cloud{status_url}?AccessKey={liblibai_access_key}&Signature={self.make_sign(status_url)}&Timestamp={self.timestamp}&SignatureNonce={self.signature_nonce}"
    

    def make_sign(self, uri):
        """
        Make the sign for the request.
        """

        timestamp = self.timestamp
        signature_nonce = self.signature_nonce
        content = '&'.join((uri, timestamp, signature_nonce))
        
        digest = hmac.new(liblibai_secret_key.encode(), content.encode(), sha1).digest()
        sign = base64.urlsafe_b64encode(digest).rstrip(b'=').decode()

        return sign


    def make_request(self, prompt, text_base, width, height):
        """
        Make the request to the API.
        """

        self.headers = {
            "Content-Type": "application/json",
        }

        self.body = {
            "templateUuid": "6f7c4652458d4802969f8d089cf5b91f",
            "generateParams": {
                "checkPointId": "412b427ddb674b4dbab9e5abd5ae6057", # F.1-dev-fp8
                "prompt": prompt, 
                "negativePrompt": "ng_deepnegative_v1_75t,(badhandv4:1.2),EasyNegative,(worst quality:2),",
                "clipSkip": 2,
                "sampler": 15, # DPM++ 2M Karras
                "steps": 20, 
                "cfgScale": 7, 
                "width": width, 
                "height": height, 
                "imgCount": 1, 
                "randnSource": 0,  
                "seed": -1, 
                "restoreFaces": 0,  
                "controlNet": [
                    {
                        "unitOrder": 1,
                        "sourceImage": text_base,
                        "width": width,
                        "height": height,
                        "preprocessor": 1,
                        "annotationParameters": {
                            "canny": {
                                "preprocessorResolution": 512,
                                "lowThreshold": 100,
                                "highThreshold": 200
                            }
                        },
                        "model": "13c1e1b96ba64f9cbb2b54f89b5fe873", # InstantX-FLUX.1-dev-Controlnet-Union-Pro
                        "controlWeight": 0.7,
                        "startingControlStep": 0,
                        "endingControlStep": 1,
                        "pixelPerfect": 1,
                        "controlMode": 1,
                        "resizeMode": 1,
                    },
                ],
            }
            
        }


    def run(self, prompt, text_base, width, height, timeout=60, interval=5):
        """
        Generate the image
        """
        start_time = time.time()

        self.make_request(prompt=prompt, text_base=text_base, width=width, height=height)

        response = requests.post(url=self.text2img_url, headers=self.headers, json=self.body)
        response.raise_for_status()

        progress = response.json()
        if progress['code'] == 0:
            while True:
                current_time = time.time()
                if (current_time - start_time) > timeout:
                    print(f"任务超时：{current_time - start_time}s")
                    return None

                generate_uuid = progress["data"]['generateUuid']
                data = {"generateUuid": generate_uuid}
                response = requests.post(url=self.status_url, headers=self.headers, json=data)
                response.raise_for_status()
                progress = response.json()
                print("debug:", progress)
                print("图片生成中：",progress['data']['percentCompleted'] * 100, "%") # [BUG] 50-0-0-0-0-90-100

                if progress['data'].get('images') and any(
                        image for image in progress['data']['images'] if image is not None):
                    link = progress['data']['images'][0]['imageUrl']
                    print("图片生成完成，链接为：", link)
                    return link
                
                time.sleep(interval)
        else:
            print(f'任务失败，原因：{progress["msg"]}')
            return None


    def generate_image(self, prompt, text_base, width=1024, height=768):

        image = self.run(prompt=prompt, text_base=text_base, width=width, height=height)

        if image is None:
            return None
        
        response = requests.get(image)

        if response.status_code != 200:
            print(f"图片下载失败，原因：{response.status_code}")
            return None

        return response.content


class ImagePrompter:
    """
    Generate prompt for ImageGenerator
    """
    def __init__(self):
        self.client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
        self.system_prompt = """
        你是一位大模型提示词生成专家。学生会将要举办一次活动，请根据用户的需求编写一个文生图模型的英文提示词，来指导大模型进行活动宣传海报的生成。
        用户会给出需求。除提示词外不要添加任何其他内容，不要擅自增加信息。输出包括：主题、背景、配色、排版等等。
        
        例子：
        Create a promotional graphic for a New Year's Eve event.
        The design should incorporate a circular motif with a dashed border, featuring abstract geometric shapes and splashes of warm colors like orange, yellow, and pink in the background.
        The text "星光E彩-2019-" should be prominently displayed within the circle, using a bold, modern font with a 3D effect.
        The overall style should be festive and contemporary, with a focus on geometric shapes and a watercolor-like splash effect in the background.
        """
        
    def generate_prompt(self, input):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": input},
            ],
            stream=False
        )
        prompt = response.choices[0].message.content
        print(f"文生图提示词已生成: \n{prompt}")
        return prompt


if __name__ == "__main__":
    # Example

    text_base_link = "https://img.picui.cn/free/2025/04/30/681243c98befb.png"
    # prompt = """
    #     Create a promotional graphic for a New Year's Eve event titled "星光E彩-2019-" in Chinese.
    #     The design should incorporate a circular motif with a dashed border, featuring abstract geometric shapes and splashes of warm colors like orange, yellow, and pink in the background.
    #     The text "星光E彩-2019-" in Chinese should be prominently displayed within the circle, using a bold, modern font with a 3D effect.
    #     Include additional text on the right side of the circle that reads "距2019年信科新年晚会 还有1天" in Chinese in a clean, sans-serif font, with the number "1" highlighted in red.
    #     Add a hashtag "#信科新年晚会#" in Chinese at the bottom left of the circle.
    #     The overall style should be festive and contemporary, with a focus on geometric shapes and a watercolor-like splash effect in the background.
    #     """
    # img_prompt_agent = ImagePrompter()
    # input = "{'type': '比赛', 'subject': 'AI与大模型', 'schedule': '给定数据集和基本的代码，让选手调参', 'objective': '系统性解析大模型技术演进脉络，探讨自然语言处理、多模态学习等领域的最新突破；构建开放交流场域，促进学术界与产业界在算力优化、数据治理、伦理规范等关键议题上的协同创新；激发青年学子技术热忱，通过案例剖析与实战工作坊培养复合型AI人才，助力国家人工智能战略与交叉学科创新发展', 'scale': '待定', 'time': '4月下旬：大模型训练挑战赛预热推送&报名推送，5月中旬：大模型训练挑战赛总结推送', 'place': '北京大学信息科学技术学院', 'cooperation': 'Linux社'}"
    # prompt = img_prompt_agent.generate_prompt(input)

    prompt = """
        Create a promotional graphic for an AI and Large Model competition.
        The design should feature a futuristic and tech-inspired theme with elements like neural networks, data streams, and coding syntax in the background. Use a cool color palette dominated by blues, purples, and metallic accents to emphasize innovation and technology.

        The text "AI与大模型训练挑战赛" should be prominently displayed in a bold, modern font with a sleek 3D or holographic effect. Incorporate dynamic elements like glowing circuit lines or abstract digital particles to enhance the technological vibe.

        Include secondary text blocks for key details:
        - "北京大学信息科学技术学院 | 合作: Linux社"
        - "4月下旬: 预热推送 | 5月中旬: 总结推送"

        The layout should be clean and organized, balancing visual tech elements with readable typography. The overall style should be professional yet engaging, appealing to students and tech enthusiasts.
    """

    painter = ImageGenerator()
    image = painter.generate_image(prompt=prompt, text_base=text_base_link, width=1024, height=768)

    if image is not None:
        with open(f'../debug/image_{int(time.time())}.png', 'wb') as file:
            file.write(image)