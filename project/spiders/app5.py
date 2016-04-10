# -*- coding: utf-8 -*-
import scrapy
import urlparse
from project.items import ProjectItem


class App5Spider(scrapy.Spider):
    name = "app5"
    allowed_domains = ["app5.com"]
    start_urls = (
        'https://app5.com/www/index.php',
    )

    def parse(self, response):
        # GET requests
        for href in response.css("a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_get_requests)

    def parse_get_requests(self, response):
        item = ProjectItem()
        parsed = urlparse.urlparse(response.url)
        parameters = urlparse.parse_qs(parsed.query)
        for parameter in parameters:
            item['url'] = parsed.path
            item['param'] = parameter
            item['type'] = "GET"
            yield item
