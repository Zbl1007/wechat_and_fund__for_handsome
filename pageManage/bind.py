import json

from flask import render_template, request

from model.Cross import Cross
from utils.tool import getJiJinInfo
from . import pageManage
from repository.CrossRepository import CrossRepository


@pageManage.route("/bind",methods = ["POST", "GET"])
def bind():
    data = request.get_data()
    try:
        cross = Cross()

        cross.url = request.form.get("url")
        cross.openid = request.form.get("openid")
        cross.timecode = request.form.get("timecode")
        cross.cid = request.form.get("cid")
        cross.mid = request.form.get("mid")


        if CrossRepository.getCrossListByOpenId(cross.openid):
            # 更新
            result = CrossRepository.updateCross(cross)
            return "2"
        else:
            # 添加
            result = CrossRepository.addCross(cross)
            return "1"
    except Exception as e:
        print("Exception:", e)
        return "参数错误！"


@pageManage.route("/getBind/<openid>",methods = ["POST", "GET"])
def getBind(openid):

    cross = CrossRepository.getCrossListByOpenId(openid)

    return render_template('bind.html',cross = cross, openid = openid)


@pageManage.route("/getFund/<openid>",methods = ["POST", "GET"])
def getFund(openid):
    tb_dapan,tb_jj = getJiJinInfo(openid,True)

    print(tb_dapan)
    print(tb_jj)
    dpList = []

    # 查看基金值
    for i in tb_dapan:
        i.border = False
        i.header = False
        # print(i)
        dpList.append({
            "code": i.get_string(fields=["大盘"]).strip(),
            "name": i.get_string(fields=["上证指数"]).strip(),
            "guzhi": i.get_string(fields=["深证成指"]).strip(),
            "gutime": i.get_string(fields=["创业板指"]).strip()
        })

    fundList = []
    # 查看基金值
    for i in tb_jj:
        i.border = False
        i.header = False
        # print(i)
        fundList.append({
            "code" : i.get_string(fields=["基金代码"]).strip(),
            "name" : i.get_string(fields=["基金名称"]).strip(),
            "guzhi" : i.get_string(fields=["估值涨幅"]).strip(),
            "gutime" : i.get_string(fields=["估值更新"]).strip(),
            "num" : i.get_string(fields=["份额"]).strip(),
            "profitStr" : i.get_string(fields=["收益"]).strip()
        })


    result_dict = {
        "dpList" : dpList,
        "fundList" : fundList
    }


    return result_dict
