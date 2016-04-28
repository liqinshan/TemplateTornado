# -*- coding:utf-8 -*-

import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

__author__ = "lqs"

logger = logging.getLogger(__name__)


class CustomSqlalchemy:
    def __init__(self):
        self._engine = None
        self._session = None
        self._configuration = None
        self.base_model = declarative_base()

    def config(self, **kwargs):
        self._configuration = kwargs

    @property
    def engine(self):
        if self._engine is None:
            self._engine = create_engine(
                self._configuration.get('url'),
                **self._configuration.get('engine_options')
            )
        return self._engine

    @property
    def session(self):
        if self._session is None:
            session_factory = sessionmaker(
                bind=self.engine,
                **self._configuration.get('session_options')
            )
            self._session = scoped_session(session_factory)
        return self._session

    def create_all(self):
        self.base_model.metadata.create_all(bind=self.engine)

    def drop_all(self):
        self.base_model.metadata.drop_all(bind=self.engine)

    def close(self):
        if self._session:
            self._session.remove()
