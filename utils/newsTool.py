import json
import os

import requests


def getNewsPic():
    response = requests.get("http://api.03c3.cn/zb/api.php")
    if response:
        try:
            response = json.loads(response.text)
            img_url = response['imageUrl']
            return saveImg(img_url)
        except:
            print("下载60s新闻出错！")
            return False

    return False


def saveImg(img_url, name = "img"):
    """
        保存图片
    """
    r = requests.get(img_url, stream=True)
    if r.status_code == 200:
        imgName = os.path.abspath(".")+ '/images/' + name+ '.png'
        open(imgName, 'wb').write(r.content)  # 将内容写入图片
        return  imgName
    return False