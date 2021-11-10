import json
import urllib
from hashlib import md5

import requests

from repository.CrossRepository import CrossRepository

myrequests = requests.Session()


def request_port(url,post_data):
    #判空
    if url or post_data:
        return False
    o = ""

    for k,v in post_data.items():
        o += k + "=" + urllib.parse.urlencode(v) + "&"

    post_data = o[0:-1]


    response = myrequests.post(url=url,data=post_data)

    if response:
        result = response.text
        return result

    return False


def push(content, cross):
    """
        推送数据
    """
    data = {
        "cid": cross.cid,
        "mid": cross.mid,
        "content": content,
        "action": "send_talk",
        "time_code": md5(str(cross.timecode).encode("utf-8")).hexdigest(),
        "msg_type": cross.msg_type,
        "token": "weixin"
    }


    response = myrequests.post(url=cross.url, data = data)


    if response:
        result = response.text
        return result

    return False

def judgeStatus(status):
    if status == "1":
        return "biubiubiu~发送成功";
    elif status == "-1":
        return "请求参数错误";
    elif status == "-2":
        return "信息缺失";
    elif status == "-3":
        return "身份验证失败";
    else:
        return status


def updateData(openid, buffer, type, msg_type, content):
    """
        更新数据列
    """
    if type == 'mixed_talk' or type == 'mixed_post':
        content = buffer + msg_type + "->" + content + "@"
    else:
        CrossRepository.updateCrossMsgTypeByOpenId(openid, type)

    CrossRepository.updateCrossContentByOpenId(openid, content)



def dataProcessing(xml_dict):
    # MsgType是消息类型 这里是提取消息类型
    msgType = xml_dict.get("MsgType")
    content = xml_dict.get("Content")


    if content == "绑定":
        cross = CrossRepository.getCrossListByOpenId(xml_dict.get("FromUserName"))
        if cross:
            return "<a href='http://sgj.520315.xyz/wxTimeMachine/getBind/" + cross.openid + "'>您已绑定，点击查看或修改</a>";
        else:
            return "<a href='http://sgj.520315.xyz/wxTimeMachine/getBind/" + xml_dict.get("FromUserName") + "'>点击绑定</a>";

    elif content == "解绑" or content ==  "解除绑定":
        # 删除绑定信息

        result = CrossRepository.deleteCrossByOpenId(xml_dict.get("FromUserName"))
        if result:
            return "已经解除绑定"
        else:
            return "操作失败，未知错误"
    elif content == "帮助":
        return """1.发送 绑定 进行绑定或修改绑定信息
2.向时光机发送消息
支持文字、图片、地理位置、链接四种消息类型。

其他消息类型等后续开发，暂不支持（如果发送了，会提示不支持该类型的，如语音消息）。
    
如果发送的是图片会自动将图片存放到typecho 的 usr/uploads/time 目录下。
    
支持发送私密说说。只需要在发送内容前加入#即可。 举例发送：#这是私密的说说，仅发送者可见。
    
连续发送多条信息
发送【开始】，开始一轮连续发送
发送【结束】，结束当前轮的发送
    
3.发送文章
输入【发文章】，开始文章发送，支持多条消息，支持多条消息图文混合
输入【结束】，结束文章发送
    
4.其他操作
发送 博客收到你的博客地址的链接
发送 发博客收到发博文的字的链接
发送 解除绑定 或 解绑 可删除掉你的绑定信息
发送 帮助 查看帮助信息

5.<a href=\'https://auth.ihewro.com/user/docs/#/wechat\'>图文教程</a>"""
    else:
        #查询是否存在记录
        cross = CrossRepository.getCrossListByOpenId(xml_dict.get("FromUserName"))
        if cross:
            if content == "文章":
                return '<a href=\''+ cross.url +'/admin/write-post.php\'>发布文章</a>';
            elif content == "博客":
                return '<a href=\'' + cross.url + '\'>打开博客</a>';
            else:
                if content == "发文章":
                    CrossRepository.updateCrossMsgTypeByOpenId(cross.openid,"mixed_post")
                    return "开启博文构造模式，请继续发送消息，下面的消息最后将组成一篇完整的文章发送到博客，发送『结束』结束本次发送，发送『取消』取消本次发送~";
                elif content == "取消":
                    CrossRepository.updateCrossMsgTypeByOpenId(cross.openid,'')
                    return "已取消发送";
                elif content == "开始":
                    CrossRepository.updateCrossMsgTypeByOpenId(cross.openid,"mixed_talk")
                    return "当前处于混合消息模式，请继续，发送『结束』结束本次发送，发送『取消』取消本次发送~";
                elif content == "结束":

                    str = cross.content
                    if not str:
                        CrossRepository.updateCrossMsgTypeByOpenId(cross.openid, '')
                        return "已结束，本次操作未发送任何信息~";
                    strList = str.split('@')

                    con = []
                    for i in strList:
                        con.append(i.split('->'))

                    result = []
                    for j in con:
                        if j[0] != '':
                            result.append({
                                'type': j[0],
                                'content': j[1]
                            })

                    content = {
                        'results': result
                    }
                    #提交
                    status = push(json.dumps(content),cross)

                    #重置
                    CrossRepository.updateCrossMsgTypeByOpenId(cross.openid, '')

                    #判断是否成功
                    return judgeStatus(status)
                else:
                    buffer = cross.content
                    type = cross.msg_type
                    if not type:
                        type = msgType

                    if msgType == "location":
                        content = xml_dict.get("Location_X") + "#" + xml_dict.get("Location_Y") \
                                  + "#" + xml_dict.get("Label") + "#http://restapi.amap.com/v3/staticmap?location=" \
                                  + xml_dict.get("Location_Y") + "," + xml_dict.get("Location_X") \
                                  + "&zoom=10&size=750*300&markers=mid,,A:" + xml_dict.get("Location_Y") \
                                  + "," + xml_dict.get("Location_X") + "&key=2a5048a9ad453654e037b6a68abd13c4"



                        updateData(cross.openid, buffer, type, "location", content)

                    elif msgType == "image":
                        content = xml_dict.get("PicUrl")
                        updateData(cross.openid, buffer, type, "image", content)

                    elif msgType == "link":
                        content = xml_dict.get("Title") + "#" + xml_dict.get("Description") + "#" + xml_dict.get("Url")
                        updateData(cross.openid, buffer, type, "link", content)

                    elif msgType == "text":
                        if xml_dict.get("Content")[0] == "#":
                            content = "[secret]" + xml_dict.get("Content")[1:] + "[/secret]"
                        else:
                            content = xml_dict.get("Content")
                        updateData(cross.openid, buffer, type, "text", content)

                    else:
                        return "不支持的消息类型";

                    # 再次查询
                    cross = CrossRepository.getCrossListByOpenId(xml_dict.get("FromUserName"))
                    type = cross.msg_type

                    if type == "mixed_post" or type == "mixed_talk":
                        # 重置
                        # CrossRepository.updateCrossMsgTypeByOpenId(cross.openid, '')
                        return "请继续，发送『结束』结束本次发送，发送『取消』取消本次发送~";
                    else:
                        status = push(cross.content, cross)
                        # 重置
                        # CrossRepository.updateCrossMsgTypeByOpenId(cross.openid, '')
                        return judgeStatus(status)

        # else:
        #     return None
        #     # return "<a href='https://www.520315.xyz/usr/wechatpy/bind.html?openid='+cross.openid>您还未绑定，点击绑定</a>";
        else:
            return "<a href='http://sgj.520315.xyz/wxTimeMachine/getBind/" + xml_dict.get("FromUserName") + "'>您还未绑定，点击绑定</a>";

        return "未知错误！"

