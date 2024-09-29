import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import DoubanMovieItem


class MovieSpider(CrawlSpider):
    name = "movie"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths='//div[@class="hd"]/a'),
            callback="parse_item",
            follow=False,
        ),
        Rule(
            LinkExtractor(
                restrict_xpaths='//*[@id="content"]/div/div[1]/div[2]/span[3]/a'
            ),
            follow=True,
        ),
    )

    def parse_item(self, response):
        item = DoubanMovieItem()
        img_urls = response.xpath('//a[@class="nbgnbg"]/img/@src').getall()
        item["image_urls"] = img_urls
        img_names = response.xpath('//span[@property="v:itemreviewed"]/text()').get()
        img_names = img_names.replace(":", "：")
        item["image_names"] = img_names
        return item
