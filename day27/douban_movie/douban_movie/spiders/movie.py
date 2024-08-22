import scrapy


class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    def parse(self, response):
        title_list = response.xpath('//div[@class="hd"]/a/span[1]/text()').getall()
        score_list = response.xpath('//div[@class="star"]/span[2]/text()').getall()
        url_list = response.xpath('//div[@class="hd"]/a/@href').getall()
        for title, score, url in zip(title_list, score_list, url_list):
            yield scrapy.Request(
                url=url,
                callback=self.parse_detail,
                meta={"data": {"title": title, "score": score, "url": url}},
            )
        next_url = response.xpath('//span[@class="next"]/a/@href').get()
        # print(next_url)
        yield response.follow(next_url, callback=self.parse)

    def parse_detail(self, response):
        info = response.xpath('//span[@property="v:summary"]/text()').getall()
        # print(info)
        info = "".join(info).replace("\n", "").replace(" ", "").replace("\u3000", "")
        item = response.meta.get("data")
        item["info"] = info
        # print(item)
        yield item
