import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DoubanxiaozuSpider(CrawlSpider):
    name = "doubanxiaozu"
    allowed_domains = ["www.douban.com"]
    start_urls = ["https://www.douban.com/group/721021/discussion"]

    rules = (Rule(LinkExtractor(restrict_xpaths=r'//tr/td[@class="title"]/a'), callback="parse_item", follow=False),
             Rule(LinkExtractor(restrict_xpaths=r'//span[@class="next"]/a'), follow=True))

    def parse_item(self, response):
        title = response.xpath('//div[@class="article"]/h1/text()').getall()
        title = ''.join(title)
        content_list = response.xpath('//div[@class="rich-content topic-richtext"]/p/text()').getall()
        content = "".join(content_list)
        publisher = response.xpath('//*[@id="topic-content"]/div[2]/h3/span/a/text()').get()
        comment_list = response.xpath('//li[@class="clearfix comment-item reply-item"]/div[2]/p/text()').getall()
        item = {
            "title": title,
            "content": content,
            "publisher": publisher,
            "comment": comment_list
        }
        return item
