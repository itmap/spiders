# -*- coding: utf-8 -*-
import logging
import pymongo

from OpenSSL import SSL
from pymongo.errors import WriteError
from twisted.internet.ssl import ClientContextFactory
from twisted.internet._sslverify import ClientTLSOptions
from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory

from itspider.items import ArticleItem

logger = logging.getLogger("itmap")


class ItspiderPipeline(object):
    def process_item(self, item, spider):
        logger.info(item["message"] if 'message' in item else "", dict(item))
        return item


class CustomClientContextFactory(ScrapyClientContextFactory):

    def getContext(self, hostname=None, port=None):
        ctx = ScrapyClientContextFactory.getContext(self)
        # Enable all workarounds to SSL bugs as documented by
        # http://www.openssl.org/docs/ssl/SSL_CTX_set_options.html
        ctx.set_options(SSL.OP_ALL)
        if hostname:
            ClientTLSOptions(hostname, ctx)
        return ctx


class MongoPipeline(object):

    collections = ['article-csdn',]

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'data')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        for collection_name in self.collections:
            self.db[collection_name].create_index([('document_id', pymongo.ASCENDING),],
                                                  unique=True)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, ArticleItem):
            try:
                self.db[item['index']].insert_one(dict(item))
            except WriteError as e:  # DuplicateKeyError
                logger.warn('---- duplicate ----: {}'.format(item['title']))
        return item
