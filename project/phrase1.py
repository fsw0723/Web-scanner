from scrapy import cmdline

cmdline.execute("scrapy crawl test -o items.json -t json".split())  #followall is the spider's name