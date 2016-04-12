from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from project.items import ProjectItem
from scrapy.http import  Request
#import sys
#sys.stdout=open('output.txt','w')
class OtherSpider(CrawlSpider):
    name = "other"
    allowed_domains = ["dhgate.com"]
    start_urls = ["http://www.dhgate.com/wholesale/casual-dresses/c014031016001-199.html",
    ]
    link_extractor = {
        'next_page':  LinkExtractor(allow=('/who.*?.html'),restrict_xpaths=('//a[@class="next"]')),
        'pro_link': LinkExtractor(allow=('/product/')),
    }

    def parse(self, response):
        for link in self.link_extractor['next_page'].extract_links(response):
            yield Request(url = link.url, callback=self.parse)
        for link in self.link_extractor['pro_link'].extract_links(response):
            yield Request(url = link.url, callback=self.myparse)


    def myparse(self, response):
        hxs = Selector(response)
        items =[]
        item = ProjectItem()
        item['url'] =  response.url
        items.append(item)
        return items