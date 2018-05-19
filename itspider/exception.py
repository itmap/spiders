#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from scrapy.utils.response import response_status_message

logger = logging.getLogger('exception')

class ExceptionMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_response(self, request, response, spider):
        if response.status >= 400:
            reason = response_status_message(response.status)
            self._faillog(request, u'HTTPERROR',reason, spider)
        return response

    def process_exception(self, request, exception, spider):
        self._faillog(request, u'EXCEPTION', exception, spider)
        return request

    def _faillog(self, request, errorType, reason, spider):
        logger.info("%(now)s <%(spider)s> (%(error)s) %(url)s reason: %(reason)s" %
                         {'now':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          'error': errorType,
                          'url': request.url,
                          'reason': reason,
                          'spider': spider.name})
