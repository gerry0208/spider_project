import scrapy


class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    def parse(self, response):
        # 获取所有电影条目
        title_list = response.xpath('//div[@class="hd"]/a/span[1]/text()').getall()
        score_list = response.xpath('//div[@class="star"]/span[2]/text()').getall()
        for title, score in zip(title_list, score_list):
            # print(title, score)
            yield {'title': title, 'score': score}
