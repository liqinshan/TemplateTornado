# -*- coding:utf-8 -*-

from .base import BaseHandler
from TemplateTornado.erros import MissingArgumentsError
from TemplateTornado.db.dbm import TestOperation

__author__ = "lqs"


class TestHandler(BaseHandler):
    def get(self, *args, **kwargs):
        data = self.parse_query()
        self.make_200_response(**data)

    def post(self, *args, **kwargs):
        data = self.parse_body()
        if not data.get('name'):
            raise MissingArgumentsError('missing argument name.')

        t_operation = TestOperation(self.session)
        t_operation.add_test_obj(name=data.get('name'))

        self.make_200_response()
