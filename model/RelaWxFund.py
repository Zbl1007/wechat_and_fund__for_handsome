#!/usr/bin/python3
# -*- coding: utf-8 -*-
## author:zbl

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class RelaWxFund(Base):
    __tablename__ = 'rela_wx_fund'
    __table_args__ = {'comment': '微信-基金关联表'}

    id = Column(INTEGER(11), primary_key=True, comment='主键')
    wx_info_id = Column(INTEGER(11), comment='微信信息表主键id')
    fund_id = Column(INTEGER(11), comment='基金表主键id')
