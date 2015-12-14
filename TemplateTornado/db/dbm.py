# -*- coding:utf-8 -*-

from TemplateTornado.db.models import Test

__author__ = "lqs"


class Base:
    def __init__(self, session):
        self.session = session

    def create(self, obj):
        if isinstance(obj, list):
            self.session.add_all(obj)
        else:
            self.session.add(obj)

        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise


class TestOperation(Base):
    def query_test_obj(self, name):
        return self.session.query(Test).filter_by(name=name).first()

    def add_test_obj(self, name):
        if not self.query_test_obj(name=name):
            t = Test(name=name)
            self.create(t)
