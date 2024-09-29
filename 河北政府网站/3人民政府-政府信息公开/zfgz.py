import csv
import time
import requests
from lxml import etree

url = "https://www.hebei.gov.cn/columns/e4a82431-5daf-4e1f-b7ff-80a68ad951b2/templates/06113b1b-3575-4358-b511-39028e54a12c/blocks/92c271ad-8bba-4a4d-9e7f-3af5efb2842b"

headers = {
  'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
}

with open('人民政府_政府规章.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['序号', '标题', '摘要', '内容'])
    for i in range(1, 15):
        params = {
            'page': i,
            'fix': "0"
        }
        response = requests.get(url, params=params, headers=headers)
        html = etree.HTML(response.text)

        index = html.xpath('//li[@class="xxgkgzwjk-list-li"]/p[1]/text()')
        title = html.xpath('//li[@class="xxgkgzwjk-list-li"]/p[2]/a/text()')
        summ = html.xpath('//li[@class="xxgkgzwjk-list-li"]/p[2]/span/text()')
        sub_url = html.xpath('//li[@class="xxgkgzwjk-list-li"]/p[2]/a/@href')
        for index, title, summ, sub_url in zip(index, title, summ, sub_url):
            response = requests.get("https://www.hebei.gov.cn" + sub_url, headers=headers)
            html = etree.HTML(response.text)
            text = html.xpath('//div[@class="incontent"]/div/text()')
            content = ''.join(text)
            print('正在抓取第', i, '页第', index, '条数据')
            writer.writerow([index, title, summ, content])
            # print([index, title, summ, content])
            time.sleep(0.5)

        time.sleep(1)