# -*- coding:utf-8 -*-

import logging
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado import options
from TemplateTornado.utils.util import parse_cfg
from TemplateTornado.basedb.customsqlalchemy import CustomSqlalchemy

__author__ = "lqs"

# Get the config file from command line.
options.options.define('cfg', default='appconf.json', help='config file')
options.parse_command_line()

logger = logging.getLogger(__name__)


class App:
    def __init__(self, handlers=None):
        self.conf = parse_cfg(options.options.cfg)
        self.app = self.make_app(handlers)

    def make_app(self, handlers):
        return Application(handlers=handlers,
                           **self.conf.get_config('application.app_options'))

    def init_db(self, db_ins=None, config_section='mysql'):
        db_ins.config_db(self.conf, conf_section=config_section)
        db_ins.create_all()

    def startup(self):
        logging.info('Starting application...')

        self.app.listen(port=self.conf.get_int('application.port'),
                        address=self.conf.get_string('application.bind'))
        IOLoop.current().start()
