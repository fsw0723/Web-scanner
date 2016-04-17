from scrapy import cmdline
import json
import os
from scrapy.crawler import CrawlerProcess
from project.spiders.test import TestSpider
from scrapy.utils.project import get_project_settings


def remove_files():
    try:
        os.remove("items.json")
        os.remove("phase1.json")
    except OSError:
        pass


def crawler_execution():
    process = CrawlerProcess(get_project_settings())

    process.crawl(TestSpider)
    process.start()  # the script will block here until the crawling is finished


def reformat_output():
    print "something here----------------------------------------------"
    with open('items.json') as my_file:
        urls = json.load(my_file)

        output_file = open("phase1.json", 'w')
        output_urls = []
        for item in urls:
            if item not in output_urls:
                output_urls.append(item)

        print len(output_urls)
        output = {"urls": output_urls}
        output_file.write(json.dumps(output))


remove_files()
crawler_execution()
reformat_output()
