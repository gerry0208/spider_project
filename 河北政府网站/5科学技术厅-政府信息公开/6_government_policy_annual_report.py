import csv
import time
import requests
from lxml import etree
import random


def get_data(name, url, page_num):
    file = open(f'{name}.csv', 'a', encoding='utf-8', newline='')
    writer = csv.writer(file)
    writer.writerow(['标题', '时间', '内容', '一级类别', '来源网站', '访问地址', '附件链接'])

    for page in range(1, page_num + 1):

        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            'referer': url
        }

        response = requests.get(url, headers=headers)
        print(url)
        print(page, response.status_code)

        html = etree.HTML(response.text)

        # 获取列表数据
        li_list = html.xpath('//li[@class="xxgk-comm-line clearfix"]')
        for li in li_list:
            # 获取详情页链接和时间
            detail_url = li.xpath('./span[1]/a/@href')[0]
            detial_url = f"https://kjt.hebei.gov.cn{detail_url}"
            time_stamp = li.xpath('./span[2]/text()')[0]
            title = li.xpath('./span[1]/a/text()')[0]

            # 获取详情页数据
            try:
                response = requests.get(detial_url, headers=headers)
                detail_html = etree.HTML(response.text)
            except:
                pass

            # 获取标题和内容
            try:
                text = detail_html.xpath('//div[@class="xiangqnr"]//text()')
                text = ''.join([i if i else '' for i in text]).replace(' ', '').replace(' ', '').replace('\t', '')

                # 获取附件链接
                appendix_url_text = ''
                appendix_url_list = detail_html.xpath('//div[@class="xiangqnr"]//a/@href')
                for appendix_url in appendix_url_list:
                    appendix_uil = 'https://kjt.hebei.gov.cn' + appendix_url
                    appendix_url_text += appendix_uil + ';'
            except:
                text = ''
                appendix_url_text = ''

            print(title, time_stamp, detial_url)
            writer.writerow([title, time_stamp, text, name, url, detial_url, appendix_url_text])

            time.sleep(random.random() / 3)
        time.sleep(random.random())
    file.close()


get_data('政府信息公开年报', 'https://kjt.hebei.gov.cn/www/xxgk2020/212936/index.html', 1)
