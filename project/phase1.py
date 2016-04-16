from scrapy import cmdline
import json
import os

# try:
#     os.remove("items.json")
#     os.remove("phase1.json")
# except OSError:
#     pass
#
# cmdline.execute("scrapy crawl test -o items.json -t json".split())  # followall is the spider's name


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