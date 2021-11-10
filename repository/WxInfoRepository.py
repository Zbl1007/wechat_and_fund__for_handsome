import logging

from sqlalchemy.exc import InvalidRequestError

from db.DBConnect import DBConnect
from model.WxInfo import WxInfo

class WxInfoRepository:

    @classmethod
    def getWxInfoList(self):
        """
            获取微信用户列表
        """

        session = DBConnect().getSession()
        try:
            wxInfoList = session.query(WxInfo.wx_id).filter(WxInfo.is_del == "0").all()

            return wxInfoList
        except InvalidRequestError:
            session.rollback()
            return False
        except Exception as e:
            logging.error(e)
            return False
        finally:
            print("关闭session")
            session.close()


if __name__ == "__main__":
    infoList = WxInfoRepository.getWxInfoList()
    print(infoList)