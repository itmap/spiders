# -*- coding: utf-8 -*-

import os
#import logging.config
#from .logger import default_logging_config
# Scrapy settings for itspider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'itspider'

SPIDER_MODULES = ['itspider.spiders']
NEWSPIDER_MODULE = 'itspider.spiders'


RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429, 407]
RETRY_TIMES = 5

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'itspider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'itspider.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'itspider.ipproxy.ProxyMiddleware' :100,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : None,
    'itspider.useragent.RotateUserAgentMiddleware' :200,
    'itspider.exception.ExceptionMiddleware' :500,
}

DOWNLOADER_CLIENTCONTEXTFACTORY='itspider.pipelines.CustomClientContextFactory'
# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'scrapy_redis.pipelines.RedisPipeline': 200,
    'itspider.pipelines.ItspiderPipeline': 300,
    # 'itspider.pipelines.MongoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
#logging.config.dictConfig(default_logging_config)

MAP_AK = "y8xcnaLtEwfxiGmA5GSBeoGzgtenFXLe"
IP_PROXY_URL = 'http://192.168.2.20:8050'

# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# REDIS_HOST = '192.168.2.20'
# REDIS_PORT = 6379


#  DUPEFILTER_CLASS = 'scrapyjs.SplashAwareDupeFilter'
#  SPLASH_URL = 'http://192.168.2.20:8030/'

host = os.environ.get('MONGO_INITDB_HOST', 'localhost')
port = os.environ.get('MONGO_INITDB_PORT', 27017)
user = os.environ.get('MONGO_INITDB_ROOT_USERNAME', 'root')
password = os.environ.get('MONGO_INITDB_ROOT_PASSWORD', 'Song123654')

#MONGO_URI = 'mongodb://localhost:27017/'
MONGO_URI = 'mongodb://{}:{}@{}:{}/'.format(user, password, host, port)
MONGO_DATABASE = 'data'
