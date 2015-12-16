# -*- coding:utf-8 -*-

from TemplateTornado.base import CustomBase
from ExampleProject.models import db

__author__ = "lqs"


class BaseHandler(CustomBase):
    @property
    def session(self):
        return db.session

    def on_finish(self):
        db.close()
