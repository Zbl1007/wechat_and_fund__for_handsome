#!/usr/bin/python3
# -*- coding: utf-8 -*-
## author:zbl

import os
# 读取my.txt内容
from sqlalchemy.exc import InvalidRequestError
import logging

from db.DBConnect import DBConnect
from model.Fund import Fund
from model.RelaWxFund import RelaWxFund
from model.WxInfo import WxInfo


class GetData():
    def __init__(self):
        self.db = DBConnect()

    def getJjCode(self):
        root_dir = os.path.abspath('.')
        f = open(root_dir + '/utils/my_jijin.txt', 'r', encoding='utf-8')
        line = f.readline()  # 调用文件的 readline()方法

        jjs = []
        while line:
            jjs.append(line.strip().split(','))
            line = f.readline()
        f.close()
        return jjs

    def getJjCodeByWxId(self,wxId):
        """
            根据wxId获取用户持有基金信息
        """
        session = self.db.getSession()
        #根据wxId获取
        try:
            wxInfo = session.query(WxInfo).filter(WxInfo.wx_id == wxId).first()

            fundList = []
            if wxInfo:
                # 获取关联信息
                # relaWxFundList = session.query(RelaWxFund.fund_id).filter(RelaWxFund.wx_info_id == wxInfo.id).all()
                ss = session.query(RelaWxFund.fund_id).filter(RelaWxFund.wx_info_id == wxInfo.id)
                fundList = session.query(Fund).filter(Fund.id.in_(ss)).all()

            jjList = []
            # 获取基金信息
            for i in fundList:
                jjList.append([i.code,i.share])

            return jjList
        except InvalidRequestError:
            session.rollback()
            return False
        except Exception as e:
            logging.error(e)
            return False
        finally:
            session.close()


#     def getGgCode(self):
#         f = open('my_gegu.txt', 'r', encoding='utf-8')
#         gg_codes = f.readlines()
#         return gg_codes


# if __name__ == "__main__":
#     a = DBConnect()
    # engine = a.getEngine()
    #
    # Fund.metadata.create_all(engine)
    # WxInfo.metadata.create_all(engine)
    # RelaWxFund.metadata.create_all(engine)
    # fundList = session.query(Fund).all()
    # for i in fundList:
    #     print(i.code)
