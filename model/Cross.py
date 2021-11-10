#!/usr/bin/python3
# -*- coding: utf-8 -*-
## author:zbl
from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import INTEGER, TEXT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Cross(Base):
    __tablename__ = 'cross'

    id = Column(INTEGER(11), primary_key=True)
    openid = Column(VARCHAR(255), nullable=False, server_default=text("''"))
    url = Column(VARCHAR(255))
    timecode = Column(VARCHAR(255))
    cid = Column(INTEGER(11))
    mid = Column(INTEGER(11))
    msg_type = Column(VARCHAR(16))
    content = Column(TEXT)
