import base64
import os
import glob
import sys
import json

from openai import OpenAI
from api_key import doubao_api_key

class ImageAnalyst:
    """
    Analyse the reference image
    """
    def __init__(self):
        self.client = OpenAI(api_key=doubao_api_key, base_url="https://ark.cn-beijing.volces.com/api/v3")
        self.system_prompt = """
            你是一个图片分析专家，你需要根据用户给出的图片以及图片的标题，分析给出的图片的风格、排版等特征，输出格式为json字符串，包含以下字段：
            - image: 图片主题；可能有多块文字；图片背景的配色、元素、组合；图片艺术风格；图片排版；图片配色
            - text: 一个数组，描述了若干个文字块。定义文字块为一个json字符串，代表了相同格式与大小的一道横排文字，包含以下字段：
                - text:文字内容
                - x:文字左上角的x坐标
                - y:文字左上角的y坐标
                - font:字体，从黑体、楷体、华文彩云中选择
                - font_size:字体大小
        """

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_image(self, image_path):
        response = self.client.chat.completions.create(
            model = "doubao-1-5-vision-pro-32k-250115",
            messages = [
                { "role": "system", "content": self.system_prompt },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": { "url":  f"data:image/png;base64,{self.encode_image(image_path)}" },
                        },
                        {
                            "type": "text",
                            "text": os.path.basename(image_path),
                        }
                    ],
                }
            ],
            response_format = { "type": "json_object" },
            stream = False
        )
        return response.choices[0].message.content


class ImageSummarizer:
    """
    Summarize the feature of the image
    """
    def __init__(self):
        self.client = OpenAI(api_key=doubao_api_key, base_url="https://ark.cn-beijing.volces.com/api/v3")
        self.system_prompt = """
            你是一个图片特征分析专家，你需要总结用户给出的信息，分析这些图片的共性特征，比如艺术风格、排版形式等等。
            直接罗列共性特征，不要输出多余信息。
        """

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def summarize_image(self, input):
        response = self.client.chat.completions.create(
            model = "doubao-1-5-vision-pro-32k-250115",
            messages = [
                { "role": "system", "content": self.system_prompt },
                { "role": "user", "content": input }
            ],
            response_format = { "type": "text" },
            stream = False
        )
        return json.loads(response.choices[0].message.content)
        


if __name__ == "__main__":

    # if len(sys.argv) != 2:
    #     print("Usage: python script.py <image_path_pattern>")
    #     sys.exit(1)

    # image_path_pattern = sys.argv[1]
    # image_paths = glob.glob(image_path_pattern)

    image_analyst_agent = ImageAnalyst()
    image_path = "../image_png/2019 新年晚会.png"
    result = image_analyst_agent.analyze_image(image_path)
    print(result)
    # results = ""

    # for image_path in image_paths:
    #     name = os.path.basename(image_path)
    #     name = os.path.splitext(name)[0]
    #     result = image_analyst_agent.analyze_image(image_path)
    #     results += result
    #     print(f"{name}分析完毕：\n{result}\n")
    #     with open(f'../image_reference/{name}', 'w', encoding='utf-8') as f:
    #         print(result, file=f)

    # summarize_agent = ImageSummarizer()
    # result = summarize_agent.summarize_image(results)
    # with open(f'../image_reference/summarize', 'w', encoding='utf-8') as f:
    #     print("总结：\n" + result, file=f)