import logging

from sqlalchemy.exc import InvalidRequestError

from db.DBConnect import DBConnect
from model.Cross import Cross
from model.Fund import Fund


class FundRepository:
    @classmethod
    def getFundList(cls):
        """
            获取fund列表
        """

        session = DBConnect().getSession()

        try:
            fundList = session.query(Fund).all()
            return fundList
        except InvalidRequestError:
            session.rollback()
            return False
        except Exception as e:
            logging.error(e)
            return False
        finally:
            print("关闭session")
            session.close()

    @classmethod
    def addCross(cls, fund):
        """
            添加cross信息
        """
        session = DBConnect().getSession()

        try:
            session.add(fund)
            session.commit()
            print("添加成功！")
        except Exception as e_update:
            print("e_update:", e_update)
            return None

    @classmethod
    def updateCross(cls,fund):
        """
            更新cross信息
        """
        session = DBConnect().getSession()

        try:
            proxyobj = session.query(Fund).filter(Fund.id == fund.id).first()
            if proxyobj:
                for key in fund.__dict__:
                    if key == '_sa_instance_state' or key == 'id':
                        continue
                    setattr(proxyobj, key, getattr(fund, key))
                session.commit()
                return proxyobj
            else:
                session.add(fund)
                session.commit()
                print("添加成功！")
        except Exception as e_update:
            print("e_update:", e_update)
            return None

    @classmethod
    def getFundById(cls, id):
        """
            获取fund信息
        """

        session = DBConnect().getSession()

        try:
            res = session.query(Fund).filter(Fund.id == id).first()
            return res
        except InvalidRequestError:
            session.rollback()
            return False
        except Exception as e:
            logging.error(e)
            return False
        finally:
            print("关闭session")
            session.close()

    @classmethod
    def deleteFundById(cls, id):
        """
            删除fund信息
        """

        session = DBConnect().getSession()

        try:
            res = session.query(Fund).filter(Fund.id == id).delete()
            return res
        except InvalidRequestError:
            session.rollback()
            return False
        except Exception as e:
            logging.error(e)
            return False
        finally:
            session.commit()
            print("关闭session")
            session.close()
