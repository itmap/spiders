#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import logging
from datetime import datetime, timedelta
from itspider.utils import get_ip_proxy

logger = logging.getLogger("root")

class ProxyMiddleware(object):

    def __init__(self):
        self.now = None
        self.ips = []

    def get_proxy(self):
        now = datetime.now()
        if not self.ips or not self.now or (now-self.now).total_seconds() > 20:
            self.ips = get_ip_proxy()
            self.now = now
        ip = random.choice(self.ips)
        logger.info('Use ip proxy: %s:%s' % (ip[0], ip[1]))
        return ip

    def set_ip_proxy(self, request, ip):
        protocol = 'https'
        request.meta['proxy'] = '%s://%s:%s' % (protocol, ip[0], ip[1])

    def process_request(self, request, spider):
        if getattr(spider, 'ipproxy', False):
            ip = self.get_proxy()
            if ip:
                self.set_ip_proxy(request, ip)

    def process_exception(self, request, exception, spider):
        if getattr(spider, 'ipproxy', False):
            if 'proxy' not in request.meta:
                return
            proxy = request.meta['proxy']
            logger.info('Http proxy failed <%s>, %d proxies left' % (proxy, len(self.ips)))
            retry = (request.meta['retry']) if 'retry' in request.meta else 0
            if retry < 6:
                ip = self.get_proxy()
                if ip:
                    self.set_ip_proxy(request, ip)
                logger.info('Retry Http proxy <%s>, %d proxies left' % (proxy, len(self.ips)))
                request.meta['retry'] = retry + 1
                return request
            else:
                log.info('Failed proxy <%s>, %d proxies left' % (proxy, len(self.ips)))
