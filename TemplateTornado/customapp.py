# -*- coding:utf-8 -*-

import logging
from tornado import options
from tornado.ioloop import IOLoop
from tornado.web import Application
from pyhocon.config_parser import ConfigFactory

__author__ = "lqs"

# Set the config file
options.options.define('cfg', help='Specify a config file')
options.parse_command_line()

# Set the logger using default logging configuration set by ``tornado.log``
logger = logging.getLogger(__name__)


class App:
    """Custom a tornado application

    Example::
    # Create an application, meanwhile create a conf object for this application
    app = App()
    # Create db
    from ExampleProject.models import db
    app.init_db(db)
    # Create handlers for this application, meanwhile set extra arguments for this handler
    handlers = [(r'/test', TestHandler, dict(db=db)), ]
    app.handlers = handlers
    # Startup application
    app.startup()
    """
    def __init__(self):
        self.app = None
        self.handlers = None
        self.conf = None

        # gen conf object while creating app
        self.parse_conf()

    def parse_conf(self):
        if options.options.cfg is None:
            raise ValueError('config file is not set using ``--cfg``')
        self.conf = ConfigFactory.parse_file(options.options.cfg)

    def init_db(self, db, **kwargs):
        db.config(**kwargs)
        db.create_all()

    def make_app(self):
        self.app = Application(handlers=self.handlers, **self.conf.get_config())

    def startup(self):
        logger.info('Starting applicaiton')
        self.make_app()
        self.app.listen(port=self.conf.get_int('', 8000),
                        address=self.conf.get_string('', '0.0.0.0'))
        IOLoop.current().start()
