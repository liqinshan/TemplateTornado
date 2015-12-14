# -*- coding:utf-8 -*-

from pyhocon.config_parser import ConfigFactory
from tornado.web import Application
from tornado.ioloop import IOLoop

from TemplateTornado.handlers.handler import TestHandler
from TemplateTornado.db.models import db

__author__ = "lqs"

application = Application(
    handlers = [
    (r'/test', TestHandler),
    ]
)

if __name__ == '__main__':
    db.create_all()

    application.listen(8888)
    IOLoop.current().start()
