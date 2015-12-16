# -*- coding:utf-8 -*-

from TemplateTornado.errors import CustomException

__author__ = "lqs"


class MissingConfError(CustomException):
    def __init__(self, message='DB has not been initialized.'):
        self.code = 400
        self.message = message
