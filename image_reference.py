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
            请根据图片反推详细的中文文生图提示词，不要输出提示词外的多余信息
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
                    ],
                }
            ],
            response_format = { "type": "text" },
            stream = False
        )
        return response.choices[0].message.content


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python script.py <image_path_pattern>")
        sys.exit(1)

    image_path_pattern = sys.argv[1]
    image_paths = glob.glob(image_path_pattern)

    image_analyst_agent = ImageAnalyst()
    
    results = []

    for image_path in image_paths:
        name = os.path.splitext(os.path.basename(image_path))[0]
        result = image_analyst_agent.analyze_image(image_path)
        results.append({"name":name, "prompt":result})
        print(f"{name}分析完毕：\n{result}\n")

    with open(f"../image_reference/img_ref.json", "w", encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
