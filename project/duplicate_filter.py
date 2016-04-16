import os

from scrapy.dupefilter import RFPDupeFilter
from scrapy.utils.request import request_fingerprint


class CustomFilter(RFPDupeFilter):
    # def __getid(self, url):
    #     mm = url.split("&view_calendar")[0]  # or something like that
    #     return mm
    #
    # def request_seen(self, request):
    #     print self.__getid(request.url)
    #     fp = self.__getid(request.url)
    #     if fp in self.fingerprints:
    #         return True
    #     self.fingerprints.add(fp)
    #     if self.file:
    #         self.file.write(fp + os.linesep)

    def request_seen(self, request):
        fp = request.method + " " + request.url
        if fp in self.fingerprints:
            return True

        if "view_calendar" in fp:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)
