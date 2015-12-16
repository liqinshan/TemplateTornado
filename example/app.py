# -*- coding:utf-8 -*-

from TemplateTornado import App
from ExampleProject.handlers import TestHandler
from ExampleProject.models import db

__author__ = "lqs"

# Add handlers.
app = App([
    (r'/test', TestHandler),
])

# Initialize db.
app.init_db(db_ins=db, config_section='mysql')

if __name__ == '__main__':
    app.startup()

