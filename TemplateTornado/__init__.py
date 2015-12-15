# -*- coding:utf-8 -*-

from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado import options
from TemplateTornado.utils.util import parse_cfg
from TemplateTornado.basedb.customsqlalchemy import CustomSqlalchemy

__author__ = "lqs"

# Get the config file from command line.
options.options.define('cfg', default='appconf.json', help='config file')
options.parse_command_line()

# Parse the config file to create db instance.
conf = parse_cfg(options.options.cfg)
db = CustomSqlalchemy(conf_obj=conf)


class App:
    def __init__(self, handlers=None):
        self.app = self.make_app(handlers)

    def make_app(self, handlers):
        return Application(handlers=handlers,
                           **conf.get_config('application.app_options'))

    def init_db(self):
        db.create_all()

    def startup(self):
        address = conf.get_string('application.bind')
        port = conf.get_int('application.port')

        self.app.listen(port=port, address=address)
        IOLoop.current().start()
