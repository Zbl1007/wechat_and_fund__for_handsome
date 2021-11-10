#!/usr/bin/python3
# -*- coding: utf-8 -*-
## author:zbl
import threading

import pymysql
import json
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBConnect(object):
    _instance_lock = threading.Lock()
    def __init__(cls):
        pass

    #单例
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with DBConnect._instance_lock:
                if not hasattr(cls, '_instance'):
                    cls.__creatSession(cls)
                    cls._instance = object.__new__(cls, *args, **kwargs)

        return cls._instance

    def __creatSession(cls):
        """
            创建数据库Session
        """
        root_dir = os.path.abspath('.')
        # root_dir = os.path.dirname(os.path.abspath('.'))
        f = open(root_dir + "/conf/Config.json", 'r', encoding='utf8')
        dbInfo = json.load(f)
        str = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(dbInfo['username'], dbInfo['passwd'], dbInfo['host'],
                                                       dbInfo['datebase'])

        cls._engine = create_engine(str)
        # self._db = pymysql.connect(host = dbInfo['host'], port = dbInfo['port'], user = dbInfo['username'], passwd = dbInfo['passwd'], database = dbInfo['datebase'])
        cls._DBSession = scoped_session(sessionmaker(bind=cls._engine))
        f.close()


    # 获取session
    def getSession(cls):
        session = cls._DBSession
        return session()

    
    # 获取engine
    def getEngine(cls):
        return cls._engine


#此处留下了sql注入的风险
def queryData(obj,sql):
    db = DBConnect().getSession()
    cursor = db.cursor()
    #获取类名
    tableName = obj.__class__.__name__
    sql = 'SELECT * FROM '+ tableName + 'WHERE %s'
    cursor.execute(sql, sql)
    db_data = cursor.fetchall()
    db.close()
    return db_data

def insertData(obj):
    db = DBConnect().getSession()
    cursor = db.cursor()

    try:
        # 获取类名
        tableName = obj.__class__.__name__
        # 获取成员
        attr = list(obj.__dict__.values())

        sql = "INSERT INTO " + tableName + " VALUES(null, %s)" % (str(attr.remove(attr[0]))[1:-1])
        cursor.execute(sql)
        db.commit()
        # 关闭数据库连接
        db.close()
    except:
        db.close()
        return False
    return True

def deleteData(obj,id):
    db = DBConnect().getSession()
    cursor = db.cursor()

    try:
        # 获取类名
        tableName = obj.__class__.__name__
        sql = "DELETE FROM %s WHERE id='%s' " % (tableName, id)
        cursor.execute(sql)
        db.commit()
        # 关闭数据库连接
        db.close()
    except:
        db.close()
        return False
    return True

def execute(sql):
    db = DBConnect().getSession()

    cursor = db.cursor()

    try:
        cursor.execute(sql)
        db.commit()
        db.close()
    except:
        db.close()
        return False
    return True

# app = Flask(__name__)
# #设置编码
# app.config['JSON_AS_ASCII'] = False


# @app.route('/getFavor', methods=['POST', 'GET'])  # 关于route（）里面可以写url，提交的方式
# def get_data():
#     user = request.args['user']
#     if user == '':
#         return jsonify({'response_code': '404', 'response_body': []})
#     udata = queryData(user)
#     tmp = {'response_code': 200, 'response_body': []}
#     for i in udata:
#         favor_id = i[1]
#         favor_name = i[3]
#         tmp['response_body'].append({'id': favor_id, 'name': favor_name})
#     return jsonify(tmp)

# @app.route('/addFavor', methods=['POST', 'GET'])  # 关于route（）里面可以写url，提交的方式
# def add_data():
#     user = request.args['user']
#     id = request.args['jjid']
#     name = request.args['jjname']
#     r = insertData(id, user, name)
#     if r == False:
#         return jsonify({'response_code': '400', 'response_body': []})
#     else:
#         return jsonify({'response_code': '200'})
#
# @app.route('/delFavor', methods=['POST', 'GET'])  # 关于route（）里面可以写url，提交的方式
# def del_data():
#     user = request.args['user']
#     id = request.args['jjid']
#     r = deleteData(user, id)
#     if r == False:
#         return jsonify({'response_code': '400', 'response_body': []})
#     else:
#         return jsonify({'response_code': '200'})
#
#
# if __name__ == '__main__':
#     # insertData("000002", "wz", "xxx")
#     app.debug = True
#     # 跨域支持
#     def after_request(resp):
#         resp.headers['Access-Control-Allow-Origin'] = '*'
#         return resp
#     app.after_request(after_request)
#     app.run(host='0.0.0.0', port=50005)
#     a = DBConnect().getSession()
#     print(a)
#     b = DBConnect().getSession()
#     print(b)