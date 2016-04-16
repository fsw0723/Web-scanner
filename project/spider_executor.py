from scrapy import cmdline
import os


def execute():

    try:
        os.remove("items.json")
        os.remove("phase1.json")
    except OSError:
        pass

    cmdline.execute("scrapy crawl test -o items.json -t json".split())  # followall is the spider's name
