# -*- coding: utf-8 -*-
import scrapy
import urlparse


class App5Spider(scrapy.Spider):
    name = "app5"
    allowed_domains = ["app5.com"]
    start_urls = (
        'https://app5.com/www/index.php',
    )

    def parse(self, response):
        for href in response.css("a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        print "current url:" + response.url
        parsed = urlparse.urlparse(response.url)
        print urlparse.parse_qs(parsed.query)
