import scrapy


class FanyiSpider(scrapy.Spider):
    name = "fanyi"
    allowed_domains = ["fanyi.so.com"]
    # start_urls = ["https://fanyi.so.com/"]

    def start_requests(self):
        url = "https://fanyi.so.com/index/search"
        form_data = {"eng": "0", "validate": "", "ignore_trans": "0", "query": "你好"}

        yield scrapy.FormRequest(url, formdata=form_data)

    def parse(self, response):
        json_data = response.json()
        data = json_data["data"]["fanyi"]
        print(data)
        pass
