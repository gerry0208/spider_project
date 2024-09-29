import json
import scrapy
from jsonpath import jsonpath


class SpiderSpider(scrapy.Spider):
    name = "爬虫项目"
    allowed_domains = ["www.winshangdata.com"]
    start_urls = ["http://www.winshangdata.com/brandList"]

    def start_requests(self):
        url = "http://www.winshangdata.com/wsapi/brand/getBigdataList3_4"
        # 爬取总共83页数据
        for page in range(1, 83):
            json_data = {
                "isHaveLink": "",
                "isTuozhan": "",
                "isXxPp": "",
                "kdfs": "",
                "key": "",
                "orderBy": "1",
                "pageNum": page,
                "pageSize": 60,
                "pid": "",
                "qy_p": "",
                "qy_r": "",
                "xqMj": "",
                "ytlb1": "",
                "ytlb2": "",
            }
            json_str = json.dumps(json_data)
            yield scrapy.FormRequest(
                url, body=json_str.encode("utf-8"), method="POST", callback=self.parse
            )
            print("正在抓取起始链接")

    # 解析列表页
    def parse(self, response):
        json_data = response.json()
        brandIdList = jsonpath(json_data, "$..brandId")
        url = "http://www.winshangdata.com/brandDetail?brandId="
        for brand_id in brandIdList:
            detail_url = url + str(brand_id)
            yield scrapy.Request(detail_url, callback=self.parse_detail)

    # 解析详情页
    def parse_detail(self, response):
        title = response.xpath('//div[@style="margin-right: 15px;"]/text()').get()
        establish_time = response.xpath(
            '//ul[@class="detail-option border-b"]/li[2]/span[2]/text()'
        ).get()
        open_way = response.xpath(
            '//ul[@class="detail-option border-b"]/li[4]/span[2]/text()'
        ).get()
        cooperation_period = response.xpath(
            '//ul[@class="detail-option border-b"]/li[5]/span[2]/text()'
        ).get()
        area_requirement = response.xpath(
            '//ul[@class="detail-option border-b"]/li[6]/span[2]/text()'
        ).get()
        yield {
            "标题": title,
            "创建时间": establish_time,
            "开店方式": open_way,
            "合作期限": cooperation_period,
            "面积要求": area_requirement,
        }
