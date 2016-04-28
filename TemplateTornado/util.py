# -*- coding:utf-8 -*-

__author__ = "lqs"

def to_str(obj):
    if isinstance(obj, bytes):
        return obj.decode()
    return obj
