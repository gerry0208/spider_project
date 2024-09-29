# Define here the models for your 爬虫项目 middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from fake_useragent import FakeUserAgent


class Fanyi360SpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the 爬虫项目 middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the 爬虫项目
        # middleware and into the 爬虫项目.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a 爬虫项目 or process_spider_input() method
        # (from other 爬虫项目 middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the 爬虫项目, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class Fanyi360DownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class MyDownloaderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        request.headers["User-Agent"] = FakeUserAgent().random
        request.headers["Pro"] = "fanyi"
        request.cookies = {
            "QiHooGUID": "0451E414034FDC40595391A663C21B40.1721750533746",
            "__guid": "15484592.4436683330458188000.1721750536111.1016",
            "so_huid": "11%2BqipTBaFXfjV%2FfVUBAWiasDmxBQVuRbHD337g0DF0OI%3D",
            "__huid": "11%2BqipTBaFXfjV%2FfVUBAWiasDmxBQVuRbHD337g0DF0OI%3D",
            "Q_UDID": "609bf48f-cf58-27df-e3d3-d4be1c1d19aa",
            "count": "4",
        }
        # request.meta["proxy"] = "127.0.0.0:1080"
        referer = request.url
        if referer:
            request.headers["referer"] = referer
        return None

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
