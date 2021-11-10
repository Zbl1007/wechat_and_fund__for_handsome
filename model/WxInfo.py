#!/usr/bin/python3
# -*- coding: utf-8 -*-
## author:zbl

from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class WxInfo(Base):
    __tablename__ = 'wx_info'
    __table_args__ = {'comment': '微信信息表'}

    id = Column(INTEGER(11), primary_key=True, comment='主键')
    wx_id = Column(String(50), comment='微信id')
    wx_name = Column(String(50), comment='微信名')
    is_del = Column(String(1), comment="是否删除")
