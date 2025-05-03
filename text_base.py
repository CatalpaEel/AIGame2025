import time
import requests
import json

from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont

from api_key import picui_token, deepseek_api_key

class TextBaseGenerator:

    def __init__(self):
        self.font_path = {
            "华文彩云": "C:/Windows/Fonts/STCAIYUN.ttf",
            "黑体": "C:/Windows/Fonts/simhei.ttf",
            "楷体": "C:/Windows/Fonts/simkai.ttf",
        }

    def draw_text(self, draw, text, x, y, font, font_size):
        """
        Draw the text on the image.
        """
        font_path = self.font_path.get(font)
        
        if not font_path:
            print(f"文字生成失败：未找到字体{font}")
            return

        font = ImageFont.truetype(font_path, font_size)

        # [TODO] now the (x, y) is the left-top corner of the text, but it may be better to be the center of the text

        draw.text((x, y), text, fill=(100, 100, 100), font=font)

    def upload_image(self, image_name, image_path):
        """
        Upload the image to Gitee.
        """

        headers = {
            "Authorization": "Bearer " + picui_token,
            "Accept": "application/json",
        }  

        files = {'file': (image_name, open(image_path, 'rb'), 'image/png')}

        response = requests.post("https://picui.cn/api/v1/upload", headers=headers, files=files)

        response.raise_for_status()
        progress = response.json()
        if progress['status'] == False:
            print(f"图片上传失败，原因：{progress['message']}")
            return None
        
        return progress['data']['links']['url'], progress['data']['links']['delete_url']

    def generate_text_base(self, texts, width=1024, height=768):
        """
        Generate the text base for the image.
        """
        img = Image.new('RGB', (width, height), color=(200, 200, 200))

        draw = ImageDraw.Draw(img)

        for text in texts:
            self.draw_text(draw, text["text"], x=text["x"], y=text["y"], font=text["font"], font_size=text["font_size"])

        print(f"文字底图生成完毕")

        name = f"textbase_{int(time.time())}.png"
        path = f"../debug/{name}"
        img.save(path)
        link, delete_link = self.upload_image(name, path)
        if link is not None:
            print(f"图片上传图床成功，链接：{link}，删除链接：{delete_link}")
        return link, delete_link


class TextComposer:
    """
    Generate and compose the text on the image
    """
    def __init__(self):
        self.client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
        self.system_prompt = """
        你是一个设计师，你将要根据用户给出的活动需求以及主视觉的宽度，设计活动主视觉上面的文字，你需要精准排版。
        你不得推断、猜测输入没有给出的任何信息，例如时间地点。
        定义文字块为一个json字符串，代表了相同格式与大小的一道横排文字，包含以下字段：
        - text:文字内容
        - x:文字左上角的x坐标
        - y:文字左上角的y坐标
        - font:字体，从黑体、楷体、华文彩云中选择
        - font_size:字体大小
        总体输出格式为JSON：
        - header：一个文字块的数组，代表了主视觉主标题的文字。主标题文字较大，夺人眼目，且可能有大小高低的错落。
        - text：其他补充信息，字体较小。
        """

    def compose(self, input_text):
        response = self.client.chat.completions.create(
            model = "deepseek-chat",
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": input_text},
            ],
            response_format = { "type": "json_object" },
            stream = False
        )
        return json.loads(response.choices[0].message.content)


if __name__ == "__main__":
    # Example
    # input = "2019年新年晚会，画面宽度：1024，高度：768"
    # compose_agent = TextComposer()
    # composition = compose_agent.compose(input)
    # print(composition)
    # texts = composition['header'] + composition['text']
    # print(texts)
    texts = [
        {
            "text": "距2019年信科新年晚会",
            "x": 615,
            "y": 350,
            "font": "黑体",
            "font_size": 20
        },
        {
            "text": "还有 1 天",
            "x": 615,
            "y": 500,
            "font": "黑体",
            "font_size": 20
        },
        {
            "text": "#信科新年晚会#",
            "x": 60,
            "y": 650,
            "font": "黑体",
            "font_size": 18
        }
    ]

    text_base = TextBaseGenerator()
    text_base_link, delete_link = text_base.generate_text_base(texts)