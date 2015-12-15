# -*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

__author__ = "lqs"


class CustomSqlalchemy:
    """Custom sqlalchemy behaves.

    """
    def __init__(self, conf_obj=None):
        """Do two things in the constructor:
        1) create a declarative to define classes mapped to relational
        database tables.
        2) Receive an conf_obj to create objects engine and session.

        conf_obj is an object created by
        `pyhocon.config_parser.ConfigFactory.parse_file()`
        """
        self.conf = conf_obj
        self._engine = None
        self._session = None
        self.base_model = declarative_base()

    @property
    def engine(self):
        if not self.conf:
            raise IOError('No conf object exists.')

        if self._engine is None:
            self._engine = create_engine(
                self.conf.get_string('mysql.url'),
                **self.conf.get_config('mysql.engine_options')
            )
        return self._engine

    @property
    def session(self):
        if not self.conf:
            raise AttributeError('No conf object exists.')

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
