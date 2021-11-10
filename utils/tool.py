#!/usr/bin/python3
# -*- coding: utf-8 -*-
## author:zbl

# 基金查询

from colorama import init, Fore, Back, Style
import prettytable as pt
import time
import platform
import os
import logging

# 定义颜色类

from utils.create_table_img import create_table_img
from utils.getInfo import getGegu, getJijin
from utils.readTxt import GetData

init(autoreset=False)


class Colored(object):
    #  前景色:红色  背景色:默认
    def red(self, s):
        return Fore.LIGHTRED_EX + s + Fore.RESET

    #  前景色:绿色  背景色:默认
    def green(self, s):
        return Fore.LIGHTGREEN_EX + s + Fore.RESET

    def yellow(self, s):
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET

    def white(self, s):
        return Fore.LIGHTWHITE_EX + s + Fore.RESET

    def blue(self, s):
        return Fore.LIGHTBLUE_EX + s + Fore.RESET


def getJiJinInfo(wxId,flag=False):
    d = GetData()


    def compareDapanNum(s1, s2):
        color = Colored()
        if float(str(s1)[:-1]) > 0.00:
            return color.red('+' + s1), color.red(s2)
        elif float(str(s1)[:-1]) < 0.00:
            return color.green(s1), color.green(s2)
        else:
            return color.white(s1), color.white(s2)


    shangz_jg, shangz_zd, shenz_jg, shenz_zd, chuangyb_jg, chuangyb_zd = 0, 0, 0, 0, 0, 0

    sh = getGegu('sh000001')
    sz = getGegu('sz399001')
    cyb = getGegu('sz399006')
    if sh != False:
        shangz_zuoshou = float(sh['gegu_zuoshou'])
        shangz_jg = float(sh['gegu_xianjia'])
        cha = shangz_jg - shangz_zuoshou
        if cha > 0:
            shangz_zd = cha / shangz_zuoshou
        else:
            shangz_zd = -(-cha / shangz_zuoshou)
        shangz_zd = str(round(shangz_zd * 100, 2)) + '%'
    if sz != False:
        shenz_zuoshou = float(sz['gegu_zuoshou'])
        shenz_jg = float(sz['gegu_xianjia'])
        cha = shenz_jg - shenz_zuoshou
        zhangfu = 0
        if cha > 0:
            shenz_zd = cha / shenz_zuoshou
        else:
            shenz_zd = -(-cha / shenz_zuoshou)
        shenz_zd = str(round(shenz_zd * 100, 2)) + '%'
    if cyb != False:
        chuangyb_zuoshou = float(cyb['gegu_zuoshou'])
        chuangyb_jg = float(cyb['gegu_xianjia'])
        cha = chuangyb_jg - chuangyb_zuoshou
        if cha > 0:
            chuangyb_zd = cha / chuangyb_zuoshou
        else:
            chuangyb_zd = -(-cha / chuangyb_zuoshou)
        chuangyb_zd = str(round(chuangyb_zd * 100, 2)) + '%'
    # shangz_zd, shangz_jg = compareDapanNum(str(shangz_zd), str(shangz_jg))
    shangz_zd, shangz_jg = str(shangz_zd), str(shangz_jg)
    # shenz_zd, shenz_jg = compareDapanNum(str(shenz_zd), str(shenz_jg))
    shenz_zd, shenz_jg = str(shenz_zd), str(shenz_jg)
    # chuangyb_zd, chuangyb_jg = compareDapanNum(str(chuangyb_zd), str(chuangyb_jg))
    chuangyb_zd, chuangyb_jg = str(chuangyb_zd), str(chuangyb_jg)
    # 绘表
    tb_dapan = pt.PrettyTable(['大盘', '上证指数', '深证成指', '创业板指'])
    tb_dapan.add_row(['价格', shangz_jg, shenz_jg, chuangyb_jg])
    tb_dapan.add_row(['涨幅', shangz_zd, shenz_zd, chuangyb_zd])

    jjc = d.getJjCodeByWxId(wxId)  # 修改为 [代码，份额] 数组

    def compareNum(s, flag=0):  # 返回 color 包装的 s 对象
        color = Colored()
        if s != '--':
            if float(str(s)[:-1]) > 0.00:
                return color.red('+' + s)
            elif float(str(s)[:-1]) < 0.00:
                return color.green(s)
            else:
                return color.white(s)
        else:
            return color.white(s)


    tb_jj = pt.PrettyTable()
    # tb_jj.field_names = ["基金代码", "基金名称", "估值涨幅", "估值更新", "净值涨幅", "净值更新", "份额", "收益"]
    tb_jj.field_names = ["基金代码", "基金名称", "估值涨幅", "估值更新", "份额", "收益"]
    totalProfitNum = 0
    for code, num in jjc:
        num = float(num)
        jj, jj_jin = getJijin(code)
        if jj != False:
            jjcode = code
            name, guzhi, gutime = jj['name'][:4], jj['gszzl'] + '%', jj['gztime'].split(" ")[1]
            jingzhi = float(str(jj_jin).split('"')[1].split(',')[1])
            profitNum = round(num * float(guzhi.split('%')[0]) / 100 * jingzhi, 2)
            jingzhip = float(str(jj_jin).split('"')[1].split(',')[3])
            jingzhitime = str(jj_jin).split('"')[1].split(',')[4]
            jingzhizd = 0
            cha = jingzhi - jingzhip
            if cha > 0:
                jingzhizd = cha / jingzhip
            else:
                jingzhizd = -(-cha / jingzhip)
            jingzhizd = str(round(jingzhizd * 100, 2)) + '%'
            # jingzhizd = compareNum(jingzhizd, flag=1)

            # profitStr = compareNum(str(profitNum))
            profitStr = str(profitNum)
            totalProfitNum += profitNum
            # guzhi = compareNum(guzhi, flag=0)

            # tb_jj.add_row([code, name, guzhi, gutime, jingzhizd, jingzhitime, num, profitStr])
            tb_jj.add_row([code, name, guzhi, gutime, num, profitStr])

    # totalProfit = compareNum(str(totalProfitNum))
    totalProfit = str(totalProfitNum)
    # tb_jj.add_row(['合计', '--', '--', '--', '--', '--', '--', totalProfit])
    tb_jj.add_row(['合计', '--', '--', '--', '--', totalProfit])
    # if platform.system().lower() == 'windows':
    #     os.system("cls")
    # elif platform.system().lower() == 'linux':
    #     os.system("clear")
    # elif platform.system().lower() == 'darwin':
    #     os.system("clear")

    if flag:
        return tb_dapan,tb_jj

    result = create_table_img([tb_dapan,tb_jj],wxId+'jjInfo.jpg',font = os.path.abspath('.')+'/utils/fonts/simkai.ttf')
    if result:
        logging.info(wxId+'基金图表生成成功')

    # result = create_table_img(tb_jj, wxId+'tb_jj.jpg',font = 'C:\\Windows\\Fonts\\simkai.ttf')
    # if result:
    #     print(wxId+'基金图表生成成功')
    return True



def getEarning(wxId):
    d = GetData()
    jjc = d.getJjCodeByWxId(wxId)  # 修改为 [代码，份额] 数组

    tb_jj = pt.PrettyTable()
    tb_jj.field_names = ["基金代码", "基金名称", "估值涨幅", "估值更新", "净值涨幅", "净值更新", "份额", "收益"]
    #tb_jj.field_names = ["基金代码", "基金名称", "估值涨幅", "估值更新", "份额", "收益"]
    totalProfitNum = 0
    for code, num in jjc:
        num = float(num)
        jj, jj_jin = getJijin(code)
        if jj != False:
            jjcode = code
            name, guzhi, gutime = jj['name'][:4], jj['gszzl'] + '%', jj['gztime'].split(" ")[1]
            jingzhi = float(str(jj_jin).split('"')[1].split(',')[1])
            profitNum = round(num * float(guzhi.split('%')[0]) / 100 * jingzhi, 2)
            jingzhip = float(str(jj_jin).split('"')[1].split(',')[3])
            jingzhitime = str(jj_jin).split('"')[1].split(',')[4]
            jingzhizd = 0
            cha = jingzhi - jingzhip
            if cha > 0:
                jingzhizd = cha / jingzhip
            else:
                jingzhizd = -(-cha / jingzhip)
            jingzhizd = str(round(jingzhizd * 100, 2)) + '%'
            # jingzhizd = compareNum(jingzhizd, flag=1)

            # profitStr = compareNum(str(profitNum))
            profitStr = str(profitNum)
            totalProfitNum += profitNum
            # guzhi = compareNum(guzhi, flag=0)

            tb_jj.add_row([code, name, guzhi, gutime, jingzhizd, jingzhitime, num, profitStr])
            # tb_jj.add_row([code, name, guzhi, gutime, num, profitStr])

    # totalProfit = compareNum(str(totalProfitNum))
    totalProfit = str(totalProfitNum)
    tb_jj.add_row(['合计', '--', '--', '--', '--', '--', '--', totalProfit])
    # tb_jj.add_row(['合计', '--', '--', '--', '--', totalProfit])
    # if platform.system().lower() == 'windows':
    #     os.system("cls")
    # elif platform.system().lower() == 'linux':
    #     os.system("clear")
    # elif platform.system().lower() == 'darwin':
    #     os.system("clear")
    result = create_table_img([tb_jj],wxId+'jjInfo.jpg',font = os.path.abspath('.')+'/utils/fonts/simkai.ttf')
    if result:
        logging.info(wxId+'基金图表生成成功')

    # result = create_table_img(tb_jj, wxId+'tb_jj.jpg',font = 'C:\\Windows\\Fonts\\simkai.ttf')
    # if result:
    #     print(wxId+'基金图表生成成功')
    return True

