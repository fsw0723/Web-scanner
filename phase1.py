import json
import os
import glob
from scrapy.crawler import CrawlerProcess
from project.spiders.test import TestSpider
from scrapy.utils.project import get_project_settings

output_urls = []


def remove_files():
    try:
        for name in glob.glob('items?.json'):
            print name
            os.remove(name)
        os.remove("phase1.json")
    except OSError:
        pass


def read_config():
    with open('config.json') as config_file:
        config_inputs = json.load(config_file)["loginurls"]
        configs = []
        for config_input in config_inputs:
            config = {"start_url": config_input["start_url"],
                      "login_page": config_input["loginurl"],
                      "domain": config_input["domain"],
                      "ignore_params": config_input["ignore_params"],
                      "username": config_input["loginpayload"].values()[0],
                      "password": config_input["loginpayload"].values()[1],
                      "username_field": config_input["loginpayload"].keys()[0],
                      "password_field": config_input["loginpayload"].keys()[1]}
            configs.append(config)

    return configs


def crawler_execution(crawler_config, output_file):
    settings = get_project_settings()
    settings.set("FEED_URI", output_file)
    process = CrawlerProcess(settings)

    process.crawl(TestSpider,
                  start_url=crawler_config["start_url"],
                  domain=crawler_config["domain"],
                  login_page=crawler_config["login_page"],
                  username=crawler_config["username"],
                  password=crawler_config["password"],
                  username_field=crawler_config["username_field"],
                  password_field=crawler_config["password_field"],
                  ignore_params=crawler_config["ignore_params"])
    process.start()  # the script will block here until the crawling is finished


def reformat_output(output_file):
    with open(output_file) as my_file:
        urls = json.load(my_file)
        for item in urls:
            if item not in output_urls:
                output_urls.append(item)


def write_to_file():
    phase1_file = open("phase1.json", 'w')
    print len(output_urls)
    output = {"urls": output_urls}
    phase1_file.write(json.dumps(output))

remove_files()
crawler_configs = read_config()
for index, crawler_config in enumerate(crawler_configs):
    output_file = "items" + str(index) + ".json"
    crawler_execution(crawler_config, output_file)
    reformat_output(output_file)

write_to_file()

