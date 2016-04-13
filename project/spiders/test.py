import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
import urlparse
from project.items import ProjectItem
from scrapy.http import  Request
import pprint
from scrapy.contrib.spiders.init import InitSpider

#import sys
#sys.stdout=open('output.txt','w')
class TestSpider(InitSpider):
    name = "test"
    allowed_domains = ["app5.com"]
    start_urls = ["https://app5.com/www/index.php",
    ]
    link_extractor = {
        'next_page':  LinkExtractor(allow=(),restrict_css=('a'))
    }

    login_page = "https://app5.com/www/index.php?index_page"

    def parse(self, response):
        # print "---------------"
        # pprint.pprint(self.link_extractor['next_page'].extract_links(response))

        item = ProjectItem()
        parsed = urlparse.urlparse(response.url)
        parameters = urlparse.parse_qs(parsed.query)
        print "parameters: " + ', '.join(parameters)

        item['url'] = parsed.path
        item['param'] = parameters
        item['type'] = "GET"
        yield item

        for link in self.link_extractor['next_page'].extract_links(response):
            if "http" not in link.url:
                continue
            if "logout" in link.url:
                continue

            yield Request(url = link.url, callback=self.parse)

    def init_request(self):
        print "init request!!!!!!!!!!"
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """Generate a login request."""
        return scrapy.FormRequest.from_response(response,
                                         formdata={'login': 'student', 'password': 'student'},
                                         callback=self.check_login_response)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if "incorrect" not in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            return self.initialized()
        else:
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.
