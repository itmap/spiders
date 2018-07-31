# -*- coding: utf-8 -*-

import logging

from itspider.items import ArticleItem
from itspider.utils import md5
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

logger = logging.getLogger(__name__)


class CsdnSpider(CrawlSpider):
    name = 'csdn'
    allowed_domains = ['blog.csdn.net']
    start_urls = (
        'https://blog.csdn.net/',
    )
    rules = (
        Rule(LinkExtractor(allow=('nav/(.*?)'))),
        Rule(LinkExtractor(allow=('(.*?)/article/list/(.*?)'))),
        Rule(LinkExtractor(allow=('(.*?)/article/details/(.*?)')), callback='parse_article'),
        Rule(LinkExtractor(allow=('(.*?)'))),
    )
    download_delay = 0.1

    def parse_article(self, response):
        item = ArticleItem()
        logger.info(response.url)
        item['index'] = 'article-{}'.format(self.name)
        item['document_id'] = md5(response.url)
        item['document_type'] = self.name
        item['source'] = response.url
        item['title'] = response.xpath('//h1[@class="title-article"]//text()').extract_first().strip()
        item['user'] = response.xpath('//a[@id="uid"]//text()').extract_first().strip()
        body = response.xpath('//article//text()').extract()
        item['body'] = '\n'.join(b for b in body if ''.join(b.split()))
        yield item
