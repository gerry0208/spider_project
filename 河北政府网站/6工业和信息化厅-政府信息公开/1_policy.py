import csv
import time
import requests
from lxml import etree
import random

def get_data(name, url, page_num):
    file = open(f'{name}.csv', 'a', encoding='utf-8', newline='')
    writer = csv.writer(file)
    writer.writerow(['标题', '时间', '内容', '一级类别', '来源网站', '访问地址'])

    for page in range(1, page_num + 1):

        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
        }

        response = requests.get(url, headers=headers)

        print(url)
        print(page, response.status_code)

        html = etree.HTML(response.content.decode('utf-8'))

        # 获取列表数据
        li_list = html.xpath('//ul[@class="xxgkList"]/li')
        for li in li_list:
            # 获取详情页链接和时间
            detail_url = li.xpath('./a[1]/@href')[0]
            detial_url = f"http://gxt.hebei.gov.cn/{detail_url}"
            time_stamp = li.xpath('./span/text()')[0]

            # 获取详情页数据
            response = requests.get(detial_url, headers=headers)
            detail_html = etree.HTML(response.content.decode('utf-8'))

            # 获取标题和内容
            try:
                title = detail_html.xpath('//h3[@class="detailTitle"]/text()')[0]
                text = detail_html.xpath('//div[@class="overview"]//text()')
                text = ''.join([i if i else '' for i in text]).replace(' ', '').replace('\t', '').replace(' ', '')

                print(title, time_stamp, detial_url)
                writer.writerow([title, time_stamp, text, name, url, detial_url])
            except:
                pass

            time.sleep(random.random() / 3)
        time.sleep(random.random())
    file.close()


get_data('政府信息公开年报', 'http://gxt.hebei.gov.cn/hbgyhxxht/zfxxgk/zfxxgknb/index.html', 1)
