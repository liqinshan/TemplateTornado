# -*- coding:utf-8 -*-

from datetime import datetime
from sqlalchemy import Column
from sqlalchemy.types import String, Integer, DateTime

from TemplateTornado.basedb.customsqlalchemy import CustomSqlalchemy

__author__ = "lqs"

db = CustomSqlalchemy()

class Test(db.base_model):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(25), unique=True, nullable=False)
    date = Column(DateTime, default=lambda: datetime.now())
