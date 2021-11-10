import logging

from sqlalchemy.exc import InvalidRequestError

from db.DBConnect import DBConnect
from model.Cross import Cross


class CrossRepository:

    @classmethod
    def getCrossList(cls):
        """
            获取cross列表
        """

        session = DBConnect().getSession()

        try:
            crossList = session.query(Cross).all()
            return crossList
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
    def addCross(cls, cross):
        """
            添加cross信息
        """
        session = DBConnect().getSession()

        try:
            session.add(cross)
            session.commit()
            print("添加成功！")
        except Exception as e_update:
            print("e_update:", e_update)
            return None

    @classmethod
    def updateCross(cls,cross):
        """
            更新cross信息
        """
        session = DBConnect().getSession()

        try:
            proxyobj = session.query(Cross).filter(Cross.openid == cross.openid).first()
            if proxyobj:
                for key in cross.__dict__:
                    if key == '_sa_instance_state' or key == 'id':
                        continue
                    setattr(proxyobj, key, getattr(cross, key))
                session.commit()
                return proxyobj
            else:
                session.add(cross)
                session.commit()
                print("添加成功！")
        except Exception as e_update:
            print("e_update:", e_update)
            return None


    @classmethod
    def getCrossListByOpenId(cls,openId):
        """
            获取cross列表
        """

        session = DBConnect().getSession()

        try:
            cross = session.query(Cross).filter(Cross.openid == openId).first()
            return cross
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
    def updateCrossMsgTypeByOpenId(cls, openId, msg_type):
        """
            获取cross列表
        """

        session = DBConnect().getSession()

        try:
            res = session.query(Cross).filter(Cross.openid == openId).update({'msg_type':msg_type,'content':''})
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

    @classmethod
    def updateCrossContentByOpenId(cls, openId, content):
        """
            获取cross列表
        """

        session = DBConnect().getSession()

        try:
            res = session.query(Cross).filter(Cross.openid == openId).update({'content': content})
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

    @classmethod
    def deleteCrossByOpenId(cls, openId):
        """
            获取cross列表
        """

        session = DBConnect().getSession()

        try:
            res = session.query(Cross).filter(Cross.openid == openId).delete()
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
