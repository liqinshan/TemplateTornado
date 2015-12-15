# -*- coding:utf-8 -*-

__author__ = "lqs"


class CustomDB:
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
