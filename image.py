import hmac
from hashlib import sha1
import base64
import time
import uuid

import requests

from api_key import  liblibai_access_key, liblibai_secret_key

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


    def make_request(self, prompt, width, height):
        """
        Make the request to the API.
        """

        self.headers = {
            "Content-Type": "application/json",
        }

        self.body = {
            "templateUuid": "6f7c4652458d4802969f8d089cf5b91f",
            "generateParams": {
                "checkPointId": "0ea388c7eb854be3ba3c6f65aac6bfd3", 
                "prompt": prompt, 
                "negativePrompt": "ng_deepnegative_v1_75t,(badhandv4:1.2),EasyNegative,(worst quality:2),",
                "clipSkip": 2,
                "sampler": 15, 
                "steps": 20, 
                "cfgScale": 7, 
                "width": width, 
                "height": height, 
                "imgCount": 1, 
                "randnSource": 0,  
                "seed": -1, 
                "restoreFaces": 0,  
            } # [TODO] Add lora
            
        }


    def run(self, prompt, width=1024, height=768, timeout=60, interval=5):
        """
        Generate the image
        """
        start_time = time.time()

        self.make_request(prompt=prompt, width=width, height=height)

        response = requests.post(url=self.text2img_url, headers=self.headers, json=self.body)
        response.raise_for_status()

        progress = response.json()
        if progress['code'] == 0:
            # Get the task ID
            while True:
                current_time = time.time()
                if (current_time - start_time) > timeout:
                    print(f"任务超时：{timeout}s")
                    return None

                generate_uuid = progress["data"]['generateUuid']
                data = {"generateUuid": generate_uuid}
                response = requests.post(url=self.status_url, headers=self.headers, json=data)
                response.raise_for_status()
                progress = response.json()
                print("图片生成中：",progress['data']['percentCompleted'] * 100, "%") # [BUG] 50-0-0-0-0-90-100

                if progress['data'].get('images') and any(
                        image for image in progress['data']['images'] if image is not None):
                    link = progress['data']['images'][0]['imageUrl']
                    print("图片生成完成，链接为：", link)
                    return link
                
                time.sleep(interval)
        else:
            print(f'任务失败，原因：code {progress["msg"]}')
            return None


    def generate_image(self):

        prompt = """
        Create a promotional graphic for a New Year's Eve event titled "星光E彩-2019-".
        The design should incorporate a circular motif with a dashed border, featuring abstract geometric shapes and splashes of warm colors like orange, yellow, and pink in the background.
        The text "星光E彩-2019-" should be prominently displayed within the circle, using a bold, modern font with a 3D effect.
        Include additional text on the right side of the circle that reads "距2019年信科新年晚会 还有1天" in a clean, sans-serif font, with the number "1" highlighted in red.
        Add a hashtag "#信科新年晚会#" at the bottom left of the circle.
        The overall style should be festive and contemporary, with a focus on geometric shapes and a watercolor-like splash effect in the background.
        """
        # [TODO] This prompt is terribly bad

        image = self.run(prompt=prompt)

        response = requests.get(image)

        return response


if __name__ == "__main__":
    # Example
    painter = ImageGenerator()
    image = painter.generate_image()

    if image is not None:
        with open(f'../debug/image.{time.time()}.png', 'wb') as file:
            file.write(image.content)