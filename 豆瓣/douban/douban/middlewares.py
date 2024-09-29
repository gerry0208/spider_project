# Define here the models for your 爬虫项目 middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import FakeUserAgent

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class DoubanSpiderMiddleware:
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


class DoubanDownloaderMiddleware:
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
        request.cookies = {
            "ll": "\"108288\"",
            "bid": "rNo1g8RP9BI",
            "_pk_id.100001.8cb4": "2caefa439e7faed8.1725885611.",
            "__utmc": "30149280",
            "__utmz": "30149280.1725885611.1.1.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/",
            "ap_v": "0,6.0",
            "dbcl2": "\"260602628:0hFm83DkmIk\"",
            "ck": "dhJa",
            "push_noty_num": "0",
            "push_doumail_num": "0",
            "__utmv": "30149280.26060",
            "__yadk_uid": "hJyvR6LTaTnWi5M7ItHISTNND0znaqob",
            "ct": "y",
            "frodotk_db": "\"7265fbe0794177005731f3a16bc46500\"",
            "_pk_ref.100001.8cb4": "%5B%22%22%2C%22%22%2C1725889927%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D",
            "_pk_ses.100001.8cb4": "1",
            "__utma": "30149280.32225040.1725885611.1725885611.1725889928.2",
            "__utmt": "1",
            "douban-fav-remind": "1",
            "__utmb": "30149280.15.7.1725890337502"
        }
        request.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
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
