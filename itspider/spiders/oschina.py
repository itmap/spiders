# -*- coding: utf-8 -*-

import scrapy
import urlparse

from itspider.items import ArticleItem
from itspider.utils import md5


class OschinaSpider(scrapy.Spider):
    name = 'oschina'
    allowed_domains = ['www.oschina.net', 'my.oschina.net']
    start_urls = (
        'https://www.oschina.net/blog',
    )
    more_url = 'https://www.oschina.net/action/ajax/get_more_recommend_blog'

    def __init__(self, *args, **kwargs):
        super(OschinaSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        navs = response.xpath('//nav[@class="box-fr blog-nav-wrapper"]/ul[@class="blog-nav"]/li/a')
        for nav in navs:
            title = nav.xpath('@title').extract_first()
            if not title:
                continue
            url = nav.xpath('@href').extract_first()
            req = scrapy.Request(url, self.article_list)
            req.meta['classify'] = title
            req.meta['page'] = 1
            yield req

    def article_list(self, response):
        query = urlparse.urlparse(response.url).query
        params = urlparse.parse_qs(query)
        classify_id = params['classification'][0]
        classify = response.meta['classify']
        page = response.meta['page']
        dlist = response.xpath('//div[@class="box item"]/div[@class="box-aw"]/header/a')
        if not dlist:
            return
        for l in dlist:
            url = l.xpath('@href').extract_first()
            req = scrapy.Request(url, self.article_detail)
            req.meta['classify'] = classify
            yield req
        page =+ 1
        url = "{}?classification={}&p={}".format(self.more_url, classify_id, page)
        req = scrapy.Request(url, self.article_list)
        req.meta['classify'] = classify
        req.meta['page'] = page
        yield req

    def article_detail(self, response):
        item = ArticleItem()
        item['index'] = 'article-{}'.format(self.name)
        item['document_id'] = md5(response.url)
        item['document_type'] = self.name
        item['source'] = response.url
        item['classify'] = response.meta['classify']
        titles = response.xpath('//h1[@class="header"]/text()').extract()
        item['title'] = ''.join(''.join(t.split()) for t in titles if ''.join(t.split()))
        user = response.xpath('//div[@class="article-detail"]//div[contains(@class, "osc-avatar small-portrait")]/@title').extract_first()
        item['user'] = user
        body = response.xpath('//div[@id="articleContent"]//text()').extract()
        item['body'] = '\n'.join(b for b in body if ''.join(b.split()))
        yield item
