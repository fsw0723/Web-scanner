# -*- coding: utf-8 -*-
import scrapy
import urlparse
from project.items import ProjectItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from project.items import ProjectItem
from scrapy.http import Request


class App5Spider(CrawlSpider):
    name = "app5"
    allowed_domains = ["app5.com"]
    start_urls = (
        'https://app5.com/www/index.php?index_page',
    )

    # rules = (Rule(LinkExtractor(allow=('/php/')), callback='parse_url', follow=True), )
    #
    # def parse_url(self, response):
    #     # GET requests
    #     print("----------------------------")
    #     print response.request.url
    #     item = ProjectItem()
    #     parsed = urlparse.urlparse(response.url)
    #     parameters = urlparse.parse_qs(parsed.query)
    #     for parameter in parameters:
    #         item['url'] = parsed.path
    #         item['param'] = parameter
    #         item['type'] = "GET"
    #         yield item
    #
    #     # for href in response.css("a::attr('href')"):
    #     #     url = response.urljoin(href.extract())
    #     #     yield scrapy.Request(url, callback=self.parse_url)
    #
    # def parse_get_requests(self, response):
    #     item = ProjectItem()
    #     parsed = urlparse.urlparse(response.url)
    #     parameters = urlparse.parse_qs(parsed.query)
    #     for parameter in parameters:
    #         item['url'] = parsed.path
    #         item['param'] = parameter
    #         item['type'] = "GET"
    #         yield item

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'login': 'student', 'password': 'student'},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        print "----------------------"
        print response
        if "incorrect" in response.body:
            self.logger.error("Login failed")
            return
        else:
            # item = ProjectItem()
            # parsed = urlparse.urlparse(response.url)
            # parameters = urlparse.parse_qs(parsed.query)
            # for parameter in parameters:
            #     item['url'] = parsed.path
            #     item['param'] = parameter
            #     item['type'] = "GET"
            #     yield item

            for href in response.css("a::attr('href')"):
                url = response.urljoin(href.extract())
                print "url ========= " + url
                if "http" not in url:
                    continue
                if "logout" in url:
                    continue
                item = ProjectItem()
                parsed = urlparse.urlparse(response.url)
                parameters = urlparse.parse_qs(parsed.query)
                print "parameters: " + ', '.join(parameters)

                item['url'] = parsed.path
                item['param'] = parameters
                item['type'] = "GET"
                yield item

                yield scrapy.Request(url, callback=self.after_login)




