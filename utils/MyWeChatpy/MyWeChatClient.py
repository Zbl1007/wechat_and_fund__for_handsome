import json
import logging
import os
import threading

from wechatpy import WeChatClient


class MyWeChatClient(object):
    """
    自用操作微信API
    """
    _instance_lock = threading.Lock()
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with MyWeChatClient._instance_lock:
                if not hasattr(cls, '_instance'):
                    # root_dir = os.path.dirname(os.path.abspath('.'))
                    f = open("./conf/Config.json", 'r', encoding='utf8')
                    info = json.load(f)
                    appid = info["appid"]
                    secret = info["secret"]
                    f.close()
                    cls._myWeChatClient = WeChatClient(appid, secret)
                    MyWeChatClient._instance = super().__new__(cls)

            return MyWeChatClient._instance

    def getWeChatClient(cls):
        """
        获取连接
        :return: WeChatClient
        """
        return cls._myWeChatClient


wx = MyWeChatClient()


def uploadImage(filePath):
    """
    上传图片
    :param filePath:
    :return:
    """
    try:
        # 上传文件
        result = wx.getWeChatClient().media.upload("image",open(filePath,'rb'))
        # 返回media_id值
        return result['media_id']
    except Exception as e:
        print(e)
        return False

def downloadImage(mediaId):
    """
    下载图片
    :param mediaId:
    :return:
    """
    try:
        result = wx.getWeChatClient().media.download(mediaId)

    except:
        return False


def sendImage(media_id,wxId,url=None):
    """
        发送图片
    :return:
    """
    try:
        # if url:
        #     result = wx.getWeChatClient().message.send
        # else:
        result = wx.getWeChatClient().message.send_image(wxId,media_id)
        print(wxId + media_id + result)

        return result

    except Exception as e:
        logging.error(e)
        return False

def sendMessage(content,wxId,url=None):
    """
        发送信息
    :return:
    """
    try:
        # if url:
        #     result = wx.getWeChatClient().message.send
        # else:
        result = wx.getWeChatClient().message.send_text(wxId,content)

        return result

    except Exception as e:
        logging.error(e)
        return False
