import scrapy
from scrapy.linkextractors import LinkExtractor
import urlparse
from project.items import ProjectItem
from scrapy.http import Request
from scrapy.contrib.spiders.init import InitSpider
import fill_form


class TestSpider(InitSpider):
    name = "test"
    allowed_domains = ["app5.com"]
    start_urls = ["https://app5.com/www/index.php",
                  ]
    link_extractor = {
        'next_page': LinkExtractor(allow=(), restrict_css=('a'))
    }

    login_page = "https://app5.com/www/index.php?index_page"

    def init_request(self):
        print "init request!!!!!!!!!!"
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        return scrapy.FormRequest.from_response(response,
                                                formdata={'login': 'student', 'password': 'student'},
                                                callback=self.check_login_response)

    def check_login_response(self, response):
        if "incorrect" not in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            return self.initialized()
        else:
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.

    def parse(self, response):

        item = ProjectItem()
        parsed = urlparse.urlparse(response.url)
        parameters = urlparse.parse_qs(parsed.query)
        print "parameters: " + ', '.join(parameters)

        post_forms = fill_form.fetch_form(response.url, response.body)
        print post_forms

        for post_form in post_forms:
            post_item = ProjectItem()
            post_item["url"] = post_form["url"]
            post_item["param"] = post_form["fields"]
            post_item["type"] = "POST"
            yield post_item

        item['url'] = parsed.path
        item['param'] = parameters
        item['type'] = "GET"
        yield item

        # Find links to the next page
        for link in self.link_extractor['next_page'].extract_links(response):
            if "http" not in link.url:
                continue
            if "logout" in link.url:
                continue

            yield Request(url=link.url, callback=self.parse)
