# -*- coding: utf-8 -*-
import logging
from OpenSSL import SSL
from twisted.internet.ssl import ClientContextFactory
from twisted.internet._sslverify import ClientTLSOptions
from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory

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
