#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import datetime
import json
import traceback as tb
import sys

from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding('utf8')

log_path = os.path.join(os.path.dirname(__file__), "..")
LOGPATH = os.environ.get("LOGPATH", log_path)
if not os.path.exists(LOGPATH):
    os.makedirs(LOGPATH)


def _default_json_default(obj):
    """
    Coerce everything to strings.
    All objects representing time get output as ISO8601.
    """
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()
    else:
        return str(obj)


class ConsoleFormatter(logging.Formatter):

    def format(self, record):
        args = record.args
        a = []
        for arg in args:
            a.append(arg)
        record.args = a
        s = super(ConsoleFormatter, self).format(record)
        return s


class LogstashFormatter(logging.Formatter):
    """
    A custom formatter to prepare logs to be
    shipped out to logstash.
    """

    def __init__(self,
                 fmt=None,
                 datefmt=None,
                 json_cls=None,
                 json_default=_default_json_default):
        """
        :param fmt: Config as a JSON string, allowed fields;
               extra: provide extra fields always present in logs
               source_host: override source host name
        :param datefmt: Date format to use (required by logging.Formatter
            interface but not used)
        :param json_cls: JSON encoder to forward to json.dumps
        :param json_default: Default JSON representation for unknown types,
                             by default coerce everything to a string
        """
        if fmt is not None:
            self._fmt = json.loads(fmt)
        else:
            self._fmt = {}
        self.json_default = json_default
        self.json_cls = json_cls
        if 'extra' not in self._fmt:
            self.defaults = {}
        else:
            self.defaults = self._fmt['extra']
        if 'source_host' in self._fmt:
            self.source_host = self._fmt['source_host']
        else:
            try:
                self.source_host = socket.gethostname()
            except:
                self.source_host = ""

    def format(self, record):
        """
        Format a log record to JSON, if the message is a dict
        assume an empty message and use the dict as additional
        fields.
        """
        fields = record.__dict__.copy()
        if 'msg' in fields and 'message' not in fields:
            msg = fields.pop('msg')
            try:
                msg = msg.format(**fields)
            except KeyError:
                pass
            fields['message'] = msg
        if 'exc_info' in fields:
            if fields['exc_info']:
                formatted = tb.format_exception(*fields['exc_info'])
                fields['exception'] = formatted
            fields.pop('exc_info')
        if 'exc_text' in fields and not fields['exc_text']:
            fields.pop('exc_text')

        for key, value in fields["args"].items():
            fields[key] = value
        del fields["args"]
        if "process" in fields: del fields["process"]
        if "module" in fields: del fields["module"]
        if "funcName" in fields: del fields["funcName"]
        if "filename" in fields: del fields["filename"]
        if "thread" in fields: del fields["thread"]
        if "threadName" in fields: del fields["threadName"]
        if "msecs" in fields: del fields["msecs"]
        if "processName" in fields: del fields["processName"]
        if "pathname" in fields: del fields["pathname"]
        if "lineno" in fields: del fields["lineno"]
        if "offset" in fields: del fields["offset"]
        if "relativeCreated" in fields: del fields['relativeCreated']
        if "created" in fields: del fields['created']
        if "levelno" in fields: del fields['levelno']

        now = datetime.datetime.utcnow()
        base_log = {'@timestamp': now.strftime("%Y-%m-%dT%H:%M:%S") +
                    ".%03d" % (now.microsecond / 1000) + "Z",
                    '@version': 1}
        base_log.update(fields)
        logr = self.defaults.copy()
        logr.update(base_log)
        return json.dumps(logr, default=self.json_default, cls=self.json_cls,
                          ensure_ascii=False, encoding="utf-8")

    def _build_fields(self, defaults, fields):
        """Return provided fields including any in defaults
        >>> f = LogstashFormatter()
        # Verify that ``fields`` is used
        >>> f._build_fields({}, {'foo': 'one'}) == \
                {'foo': 'one'}
        True
        # Verify that ``@fields`` in ``defaults`` is used
        >>> f._build_fields({'@fields': {'bar': 'two'}}, {'foo': 'one'}) == \
                {'foo': 'one', 'bar': 'two'}
        True
        # Verify that ``fields`` takes precedence
        >>> f._build_fields({'@fields': {'foo': 'two'}}, {'foo': 'one'}) == \
                {'foo': 'one'}
        True
        """
        return dict(list(defaults.get('@fields', {}).items()) + list(fields.items()))


class MongoHandler(logging.Handler):
    
    def __init__(self, host, port, db, user, password):
        client = MongoClient(host, port, username=user, password=password)
        self.db = client[db]

    def emit(self, record):
        data = self.format(record)
        index = 'index' in data and data['index'] or 'default'
        collection = self.db[index]
        doc_id = data['document_id']
        collection.update({'document_id': doc_id}, data, upsert=True)


default_logging_config = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'json': {
            'format': ''
        },
        'logstash': {
            'format': '{}',
            '()': LogstashFormatter,
        },
        'console': {
            '()': ConsoleFormatter
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOGPATH, 'logs/file.log'),
            'maxBytes': 1024000,
            'backupCount': 10,
        },
        'sql': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOGPATH, 'logs/sql.log'),
            'maxBytes': 1024000,
            'backupCount': 10,
        },
        'logstash': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'logstash',
            'filename': os.path.join(LOGPATH, 'logs/info.log'),
            'maxBytes': 1024000000,
            'backupCount': 10,
        },
        'mongo': {
            'level': 'INFO',
            'class': MongoHandler,
            'formatter': 'logstash',
            'host': os.environ.get('MONGO_INITDB_HOST', 'localhost'),
            'port': os.environ.get('MONGO_INITDB_PORT', 27017),
            'user': os.environ.get('MONGO_INITDB_ROOT_USERNAME', 'root'),
            'password': os.environ.get('MONGO_INITDB_ROOT_PASSWORD', 'Song123654'),
            'db': 'data',
        }
    },
    'loggers': {
        'root': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'itmap': {
            'handlers': ['logstash', 'console', 'mongo'],
            'propagate': False,
            'level': 'DEBUG'
        },
        'scrapy': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'exception': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'DEBUG',
        }
    }
}
