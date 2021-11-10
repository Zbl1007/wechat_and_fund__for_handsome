#!/usr/bin/python3
# -*- coding: utf-8 -*-
## author:zbl

from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Fund(Base):
    __tablename__ = 'fund'
    __table_args__ = {'comment': '基金信息表'}

    id = Column(INTEGER(11), primary_key=True, comment='主键')
    code = Column(String(8), comment='基金代码')
    name = Column(String(50), comment='基金名称')
    share = Column(DECIMAL(20, 3), comment='份额')


    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.id)