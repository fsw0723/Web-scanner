import scrapy
from scrapy.linkextractors import LinkExtractor
import urlparse
from project.items import ProjectItem
from scrapy.http import Request
from scrapy.spiders.init import InitSpider
import fill_form


class TestSpider(InitSpider):
    name = "test"
    login_required = False

    link_extractor = {
        'next_page': LinkExtractor(allow=(), restrict_css=('a'))
    }

    def __init__(self, *args, **kwargs):
        super(TestSpider, self).__init__(*args, **kwargs)

        self.start_urls = [kwargs.get('start_url')]
        self.allowed_domains = [kwargs.get('domain')]
        self.login_page = kwargs.get('login_page')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.ignore_params = kwargs.get('ignore_params')

    def init_request(self):
        print "-------------init request-----------"
        if self.username and self.password:
            return Request(url=self.login_page, callback=self.login)
        return self.initialized()

    def login(self, response):
        return scrapy.FormRequest.from_response(response,
                                                formdata={'login': self.username, 'password': self.password},
                                                callback=self.check_login_response)

    def check_login_response(self, response):
        if "incorrect" not in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            self.login_required = True
            return self.initialized()
        else:
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.

    def parse(self, response):
        post_forms = fill_form.fetch_form(response.url, response.body)
        for post_form in post_forms:
            yield self.generate_post_item(post_form)

        yield self.generate_get_item(response)

        # Find links to the next page
        for link in self.link_extractor['next_page'].extract_links(response):
            if "http" not in link.url:
                continue
            if "logout" in link.url:
                continue

            yield Request(url=link.url, meta={'ignore_params': self.ignore_params}, callback=self.parse)

    def generate_post_item(self, post_form):
        post_item = ProjectItem()
        post_item["url"] = post_form["url"]
        post_item["param"] = post_form["fields"]
        post_item["type"] = "POST"
        if self.login_required:
            post_item["loginrequired"] = "true"
        else:
            post_item["loginrequired"] = "false"
        post_item["loginurl"] = self.login_page
        return post_item

    def generate_get_item(self, response):
        parsed = urlparse.urlparse(response.url)
        parameters = urlparse.parse_qs(parsed.query)

        item = ProjectItem()
        url = parsed.geturl()
        if "?" in url:
            item['url'] = url[:url.find('?')]
        else:
            item['url'] = url

        item['param'] = parameters
        item['type'] = "GET"
        if self.login_required:
            item["loginrequired"] = "true"
        else:
            item["loginrequired"] = "false"
        item["loginurl"] = self.login_page
        return item
