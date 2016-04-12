from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
import urlparse
from project.items import ProjectItem
from scrapy.http import  Request
import pprint
#import sys
#sys.stdout=open('output.txt','w')
class TestSpider(CrawlSpider):
    name = "test"
    allowed_domains = ["app5.com"]
    start_urls = ["https://app5.com/www/index.php",
    ]
    link_extractor = {
        'next_page':  LinkExtractor(allow=(),restrict_css=('a'))
    }

    def parse(self, response):
        print "---------------"
        pprint.pprint(self.link_extractor['next_page'].extract_links(response))

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


    def myparse(self, response):
        hxs = Selector(response)
        items =[]
        item = ProjectItem()
        item['url'] =  response.url
        items.append(item)
        return items