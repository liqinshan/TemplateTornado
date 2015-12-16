# -*- coding:utf-8 -*-

from TemplateTornado.basedb.customdb import CustomDB
from .models import Test

__author__ = "lqs"


class TestOperation(CustomDB):
    def query_test_obj(self, name):
        return self.session.query(Test).filter_by(name=name).first()

    def add_test_obj(self, name):
        if not self.query_test_obj(name=name):
            t = Test(name=name)
            self.create(t)
