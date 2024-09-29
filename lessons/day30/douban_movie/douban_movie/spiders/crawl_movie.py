import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider


class CrawlMovieSpider(RedisCrawlSpider):
    name = "crawl_movie"
    allowed_domains = ["movie.douban.com"]
    # start_urls = ["https://movie.douban.com/top250"]
    redis_key = 'start_urls'

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="hd"]/a'), callback="parse_item", follow=False),
        Rule(LinkExtractor(restrict_xpaths='//span[@class="next"]/a'), follow=True)
    )

    def parse_item(self, response):
        item = {"title": response.xpath('//h1/span[1]/text()').get(), "rate": response.xpath('//strong/text()').get()}
        return item
