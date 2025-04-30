import time
import requests

from PIL import Image, ImageDraw, ImageFont

from api_key import image_base_url

class TextBaseGenerator:

    def __init__(self):
        self.font_path = {
            "华文彩云": "C:/Windows/Fonts/STCAIYUN.ttf",
            "黑体": "C:/Windows/Fonts/simhei.ttf",
            "楷体": "C:/Windows/Fonts/simkai.ttf",
        }

    def DrawText(self, draw, text, x, y, font, font_size):
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
            "Accept": "application/json",
        }  

        files = {'file': (image_name, open(image_path, 'rb'), 'image/png')}

        response = requests.post(image_base_url, headers=headers, files=files)

        response.raise_for_status()
        progress = response.json()
        if progress['status'] == False:
            print(f"图片上传失败，原因：{progress['message']}")
            return None
        
        return progress['data']['links']['url']

    def GenerateTextBase(self, texts, width=1024, height=768):
        """
        Generate the text base for the image.
        """
        img = Image.new('RGB', (width, height), color=(200, 200, 200))

        draw = ImageDraw.Draw(img)

        for text in texts:
            self.DrawText(draw, text["text"], x=text["x"], y=text["y"], font=text["font"], font_size=text["font_size"])

        print(f"文字底图生成完毕")

        name = f"textbase_{int(time.time())}.png"
        name = "test.png"
        path = f"../debug/{name}"
        img.save(path)
        link = self.upload_image(name, path)
        if link is not None:
            print(f"图片上传成功，链接：{link}")
        return link

if __name__ == "__main__":
    # Example
    texts = [
        {"text": "星光E彩-2019-", "x": 200, "y": 300, "font": "华文彩云", "font_size": 100},
        {"text": "距2019年信科新年晚会 还有1天", "x": 500, "y": 500, "font": "楷体", "font_size": 30},
        {"text": "#信科新年晚会#", "x": 700, "y": 600, "font": "楷体", "font_size": 30},
    ]

    text_base = TextBaseGenerator()
    text_base_link = text_base.GenerateTextBase(texts)