# -*- coding: utf-8 -*-
import scrapy


class MyfirstspiderSpider(scrapy.Spider):
    name = 'myfirstspider'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        pass
