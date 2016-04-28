# -*- coding:utf-8 -*-

__author__ = "lqs"


class CustomException(Exception):
    pass


class MissingArgumentsError(CustomException):
    def __init__(self, message='Missing arguments'):
        self.code = 400
        self.message = message
