# -*- coding:utf-8 -*-

import traceback
import logging
import json

from tornado import web
from TemplateTornado.customerrors import CustomException, MissingArgumentsError
from TemplateTornado.util import to_str

__author__ = "lqs"

logger = logging.getLogger(__name__)


class Base(web.RequestHandler):
    def options(self, *args, **kwargs):
        """Rewrite the method to support CORS.

        Refer to: http://newhtml.net/using-cors/
        Refer to: https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Access_control_CORS
        """
        headers = self.request.headers.get('Access-Control-Request-Headers')
        origin = self.request.headers.get('Origin', '*')
        methods = 'OPTIONS, GET, POST, PUT, DELETE'

        if headers:
            self.set_header('Access-Control-Allow-Headers', headers)

        if origin == 'null':
            origin = '*'
        self.set_header('Access-Control-Allow-Origin', origin)
        self.set_header('Access-Control-Allow-Methods', methods)

        self.set_status(204)
        self.finish()

    def write_error(self, status_code, message=None, **kwargs):
        """Rewrite the method to accept the error message of the custom error.

        """
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            self.finish({'code': status_code, 'message': message or self._reason})

    def _handle_request_exception(self, e):
        """Rewrite the method to enable the ability to handle the custom
        errors.

        """
        if isinstance(e, CustomException):
            self.set_status(e.code)
            self.write_error(e.code, message=str(e.message))
        else:
            super()._handle_request_exception(e)

    def make_200_response(self, **kwargs):
        kwargs.update(code=200)
        self.write(kwargs)
        self.finish()

    def parse_body(self):
        """Handle the body argument in the request.

        Body argument is a bytes string.
        """
        if not self.request.body:
            logger.warning('The request body is empty.')
            raise MissingArgumentsError('Missing body arguments.')

        content_type = self.request.headers.get('Content-Type')
        if content_type and content_type.startswith('application/json'):
            data = json.loads(to_str(self.request.body))
            return {k: v for k, v in data.items()}

    def parse_query(self):
        """Handle the query arguments in the request.

        Query arguments are dicts that keys are str, while values are lists of
        bytes string.
        """
        if not self.request.arguments:
            logger.warning('The are no arguments coming with the request.')
            raise MissingArgumentsError('Missing query arguments.')
        return {k: to_str(v[0]) for k, v in self.request.arguments.items()}
