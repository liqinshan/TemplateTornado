# -*- coding:utf-8 -*-

import os
from pyhocon import ConfigFactory
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

__author__ = "lqs"


class CustomSqlalchemy:
    """Custom sqlalchemy behaves.

    """
    def __init__(self, cfg=None):
        self.cfg = cfg
        self._engine = None
        self._session = None
        self.base_model = declarative_base()

    def parse_cfg(self):
        if self.cfg is None:
            self.cfg = self.default_cfg

        if not os.path.exists(self.cfg):
            raise IOError('cfg file {0} does not exist.'.format(self.cfg))

        return ConfigFactory.parse_file(self.cfg)

    @property
    def conf(self):
        return self.parse_cfg()

    @property
    def default_cfg(self):
        return 'default.json'

    @property
    def engine(self):
        if self._engine is None:
            self._engine = create_engine(
                self.conf.get_string('mysql.url'),
                **self.conf.get_config('mysql.engine_options')
            )
        return self._engine

    @property
    def session(self):
        if self._session is None:
            session_factory = sessionmaker(
                bind=self.engine,
                **self.conf.get_config('mysql.session_options')
            )
            self._session = scoped_session(session_factory)
        return self._session

    def create_all(self):
        self.base_model.metadata.create_all(bind=self.engine)

    def drop_all(self):
        self.base_model.metadata.drop_all(bind=self.engine)

    def close(self):
        self.session.remove()
