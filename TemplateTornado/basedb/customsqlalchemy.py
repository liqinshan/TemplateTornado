# -*- coding:utf-8 -*-

import logging
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from .db_error import MissingConfError

__author__ = "lqs"

logger = logging.getLogger(__name__)


class CustomSqlalchemy:
    """Custom sqlalchemy behaves.

    """
    def __init__(self):
        """Create a declarative at initialization.

        On initialization, we do nothing but create a declarative which is
        used for defining classes mapped to relational database tables.

        Example::
            from TemplateTornado.basedb.customsqlalchemy import CustomSqlalchemy

            db = CustomSqlalchemy()

            class Test(db.base_model):
                id = Column(Integer, primary_key=true, autoincrement=true)
                name = Column(String(25), unique=true, nullable=false)
        """
        self.conf = None
        self.section = None
        self._engine = None
        self._session = None
        self.base_model = declarative_base()

    def config_db(self, conf_obj, conf_section='mysql'):
        """Get the relational db configuration.

        The configuration is read from ``conf_section`` in the ``conf_obj``
        and will be used by methods `engine` and `session` to create the
        objects engine and session.

        The ``conf_obj`` is an object created by
        `pyhocon.config_parser.ConfigFactory.parse_file()`

        The method must be called before creating engine and session.
        """
        self.conf = conf_obj
        self.section = conf_section

    @property
    def engine(self):
        if not self.conf:
            logger.error('Need to initialize db before creating engine.')
            raise MissingConfError()

        if self._engine is None:
            self._engine = create_engine(
                self.conf.get_string('{0}.url'.format(self.section)),
                **self.conf.get_config('{0}.engine_options'.format(self.section))
            )
        return self._engine

    @property
    def session(self):
        if not self.conf:
            logger.error('Need to initialize db before using session.')
            raise MissingConfError()

        if self._session is None:
            session_factory = sessionmaker(
                bind=self.engine,
                **self.conf.get_config('{0}.session_options'.format(self.section))
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
