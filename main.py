#!/usr/bin/python3
# -*- coding: utf-8 -*-
## author:zbl
import json
import logging

from flask import Flask, request, abort, render_template
import hashlib
import xmltodict
import time,os
from wechatpy.replies import ImageReply
from wechatpy import parse_message

# 微信的token令牌
from db.DBConnect import DBConnect
from model.WxInfo import WxInfo
from repository.CrossRepository import CrossRepository
from repository.WxInfoRepository import WxInfoRepository
from utils.MyWeChatpy.MyWeChatClient import uploadImage, sendImage, sendMessage
from utils.handsome import dataProcessing
from utils.newsTool import getNewsPic
from utils.readTxt import GetData
from utils.tool import getJiJinInfo

WECHAT_TOKEN = 'bailiang125'
app = Flask(__name__)


@app.route("/wx", methods=["POST","GET"])
def wechat():
    """验证服务器地址的有效性"""
    # 开发者提交信息后，微信服务器将发送GET请求到填写的服务器地址URL上，GET请求携带四个参数:
    # signature:微信加密, signature结合了开发者填写的token参数和请求中的timestamp参数 nonce参数
    # timestamp:时间戳(chuo这是拼音)
    # nonce: 随机数
    # echostr: 随机字符串
    # 接收微信服务器发送参数
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")

    # 校验参数
    # 校验流程：
    # 将token、timestamp、nonce三个参数进行字典序排序
    # 将三个参数字符串拼接成一个字符串进行sha1加密
    # 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
    if not all([signature, timestamp, nonce]):
        # 抛出400错误
        abort(400)

    # 按照微信的流程计算签名
    li = [WECHAT_TOKEN, timestamp, nonce]
    # 排序
    li.sort()
    # 拼接字符串
    tmp_str = "".join(li)
    tmp_str = tmp_str.encode('utf-8')

    # 进行sha1加密, 得到正确的签名值
    sign = hashlib.sha1(tmp_str).hexdigest()

    # 将自己计算的签名值, 与请求的签名参数进行对比, 如果相同, 则证明请求来自微信
    if signature != sign:
        # 代表请求不是来自微信
        # 弹出报错信息, 身份有问题
        abort(403)
    else:
        # 表示是微信发送的请求
        if request.method == "GET":
            # 表示第一次接入微信服务器的验证
            echostr = request.args.get("echostr")
            # 校验echostr
            if not echostr:
                abort(400)
            return echostr

        elif request.method == "POST":
            # 表示微信服务器转发消息过来
            # 拿去xml的请求数据
            xml_str = request.data

            # 当xml_str为空时
            if not xml_str:
                abort(400)

            # 对xml字符串进行解析成字典
            xml_dict = xmltodict.parse(xml_str)

            xml_dict = xml_dict.get("xml")
            # print(xml_dict)
            # MsgType是消息类型 这里是提取消息类型
            msg_type = xml_dict.get("MsgType")
            # logging.info(xml_dict)

            # 标志位
            flag = False

            if xml_dict.get("Content") == "openid":
                resp_dict = {
                    "xml": {
                        "ToUserName": xml_dict.get("FromUserName"),
                        "FromUserName": xml_dict.get("ToUserName"),
                        "CreateTime": int(time.time()),
                        "MsgType": "text",
                        "Content": xml_dict.get("FromUserName")
                    }
                }
                return resp_dict

            elif xml_dict.get("Content") == "基金" or xml_dict.get("Content") == "新闻":
                # 读取值返回
                if xml_dict.get("Content") == "基金":
                    result = getJiJinInfo(xml_dict.get("FromUserName"))
                else:
                    imgName = getNewsPic()
                    if imgName:
                        result = uploadImage(imgName)

                if result:
                    if xml_dict.get("Content") == "基金":
                        response = uploadImage(
                            os.path.abspath(".") + "/images/" + xml_dict.get("FromUserName") + "jjInfo.jpg")
                    else:
                        response = result

                    if response:
                        msg = parse_message(xml_str)
                        reply = ImageReply(media_id=response, message=msg)
                        # print(reply)
                        # print(reply.render())
                        xml = reply.render()
                        return xml


                    else:
                        resp_dict = {
                            "xml": {
                                "ToUserName": xml_dict.get("FromUserName"),
                                "FromUserName": xml_dict.get("ToUserName"),
                                "CreateTime": int(time.time()),
                                "MsgType": "text",
                                "Content": "上传出错！"
                            }
                        }

            else:
                result = dataProcessing(xml_dict)
                resp_dict = {
                    "xml": {
                        "ToUserName": xml_dict.get("FromUserName"),
                        "FromUserName": xml_dict.get("ToUserName"),
                        "CreateTime": int(time.time()),
                        "MsgType": "text",
                        "Content": result
                    }
                }
            resp_xml_str = xmltodict.unparse(resp_dict)
            # 返回消息数据给微信服务器
            return resp_xml_str

            # if msg_type == "text":
            #     # 表示发送文本消息
            #     # 够造返回值, 经由微信服务器回复给用户的消息内容
            #     # 回复消息
            #     # ToUsername: (必须传) 接收方账号(收到的OpenID)
            #     # FromUserName: (必须传) 开发者微信号
            #     # CreateTime: (必须传) 消息创建时间(整形)
            #     # MsgType: (必须传) 消息类型
            #     # Content: (必须传) 回复消息的内容(换行:在Content中能够换行, 微信客户端就支持换行显示)
            #
            #     # 我们自己的消息处理逻辑
            #     # user_name = xml_dict.get("FromUserName")
            #
            #     if flag:
            #         if xml_dict.get("Content") == "openid":
            #             resp_dict = {
            #                 "xml": {
            #                     "ToUserName": xml_dict.get("FromUserName"),
            #                     "FromUserName": xml_dict.get("ToUserName"),
            #                     "CreateTime": int(time.time()),
            #                     "MsgType": "text",
            #                     "Content": xml_dict.get("FromUserName")
            #                 }
            #             }
            #             return resp_dict
            #
            #
            #         #基金判断
            #         if xml_dict.get("Content") == "jj":
            #             #读取值返回
            #             result = getJiJinInfo(xml_dict.get("FromUserName"))
            #
            #             if result:
            #
            #                 response = uploadImage(
            #                     os.path.abspath(".") + "/images/" + xml_dict.get("FromUserName") + "jjInfo.jpg")
            #
            #
            #                 if response:
            #                     msg = parse_message(xml_str)
            #                     reply = ImageReply(media_id=response, message=msg)
            #                     # print(reply)
            #                     # print(reply.render())
            #                     xml = reply.render()
            #                     return xml
            #
            #
            #                 else:
            #                     resp_dict = {
            #                         "xml": {
            #                             "ToUserName": xml_dict.get("FromUserName"),
            #                             "FromUserName": xml_dict.get("ToUserName"),
            #                             "CreateTime": int(time.time()),
            #                             "MsgType": "text",
            #                             "Content": "上传出错！"
            #                         }
            #                     }
            #
            #     else:
            #         resp_dict = {
            #             "xml": {
            #                 "ToUserName": xml_dict.get("FromUserName"),
            #                 "FromUserName": xml_dict.get("ToUserName"),
            #                 "CreateTime": int(time.time()),
            #                 "MsgType": "text",
            #                 "Content": xml_dict.get("Content")
            #             }
            #         }
            #
            #
            #
            # else:
            #     if msg_type == 'image':
            #         msg = parse_message(xml_str)
            #         media_id = xml_dict.get('MediaId')
            #         reply = ImageReply(media_id=media_id, message=msg)
            #         xml = reply.render()
            #         return xml
            #
            #     resp_dict = {
            #         "xml": {
            #             "ToUserName": xml_dict.get("FromUserName"),
            #             "FromUserName": xml_dict.get("ToUserName"),
            #             "CreateTime": int(time.time()),
            #             "MsgType": "text",
            #             "Content": "对不起，不能识别您发的内容！"
            #         }
            #     }
            # 将字典转换为xml字符串
            # resp_xml_str = xmltodict.unparse(resp_dict)
            # # 返回消息数据给微信服务器
            # return resp_xml_str


@app.route("/pushTask",methods = ["POST", "GET"])
def pushTask():
    """
        主动推送当日基金涨跌情况给用户
    """
    token = request.args.get("token")
    if token == "right":
        #获取目前用户

        wxInfoList = WxInfoRepository.getWxInfoList()
        msg = ""
        if wxInfoList:
            for i in wxInfoList:
                # 读取值返回
                result = getJiJinInfo(i[0])
                # xml_str = """<xml>
                #                     <ToUserName><![CDATA[gh_a6026c9fc172]]></ToUserName>\n
                #                     <FromUserName><![CDATA[{0}]]></FromUserName>\n
                #                     <CreateTime>{1}</CreateTime>\n
                #                     <MsgType><![CDATA[text]]></MsgType>\n
                #                     <Content><![CDATA[jj]]></Content>\n
                #                     <MsgId>23055705217771921</MsgId>\n
                #                 </xml>""".format(i[0], int(time.time()))
                # msg = parse_message(xml_str)
                if result:
                    # 上传临时素材，基金信息图片
                    response = uploadImage(
                        os.path.abspath(".") + "/images/" + i[0] + "jjInfo.jpg")

                    if response:
                        # 主动发送图片
                        sendImage(response,i[0])
                        msg += "获取成功：" + i[0]
                    else:
                        # 发送消息，提示失败
                        sendMessage("获取基金信息失败！", i[0])
                        msg += "获取基金信息失败！" + i[0]
            return msg
        return "查询失败！"
    else:
        return "非法访问!"



@app.route("/pushNewsTask",methods = ["POST", "GET"])
def pushNewsTask():
    """
        主动推送每日60s看世界新闻
    """
    token = request.args.get("token")
    if token == "right":
        #获取目前用户

        wxInfoList = WxInfoRepository.getWxInfoList()
        msg = ""
        if wxInfoList:
            for i in wxInfoList:
                # 读取值返回
                result = getJiJinInfo(i[0])
                
                if result:
                    # 上传临时素材，新闻图片
                    # 获取新闻信息并保存
                    imgName = getNewsPic()
                    if imgName:
                        response = uploadImage(imgName)

                        if response:
                            # 主动发送图片
                            sendImage(response,i[0])
                            msg += "获取成功：" + i[0]
                        else:
                            # 发送消息，提示失败
                            sendMessage("获取60s新闻失败！", i[0])
                            msg += "获取60s新闻失败！" + i[0]
            return msg
        return "查询失败！"
    else:
        return "非法访问!"


@app.route("/fund/list",methods = ["POST", "GET"])
def list():
    """
        查询基金
    """
    return None


@app.route("/fund/add",methods = ["POST", "GET"])
def add():
    """
        添加基金
    """
    return None


@app.route("/fund/edit",methods = ["POST", "GET"])
def edit():
    """
        修改基金
    """
    return None


@app.route("/fund/delete",methods = ["POST", "GET"])
def delete():
    """
        删除基金
    """
    return None



from pageManage import pageManage
app.register_blueprint(pageManage)

if __name__ == '__main__':
    app.run(port=39080, host='0.0.0.0', debug=True)