import csv
import time
import requests
from lxml import etree
import random


def get_data(name, id, page_num):
    file = open(f'教育领域信息公开_{name}.csv', 'a', encoding='utf-8', newline='')
    writer = csv.writer(file)
    writer.writerow(['标题', '时间', '内容', '一级类别', '来源网站', '访问地址', '附件链接'])

    for page in range(1, page_num + 1):

        url = "http://jyt.hebei.gov.cn/column.jsp"

        params = {
            'id': id,
            'current': page
        }

        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            'Referer': url,
        }

        response = requests.get(url, params=params, headers=headers)

        print(url)
        print(page, response.status_code)

        html = etree.HTML(response.text)

        # 获取列表数据
        tr_list = html.xpath('//table[@width="97%"]//tr[not(@id="th")]')
        for tr in tr_list:
            # 获取标题、详情页链接、时间和效力状态
            title = tr.xpath('./td[2]/a/text()')[0]
            detail_url = tr.xpath('./td[2]/a/@href')[0]
            detial_url = f"http://jyt.hebei.gov.cn{detail_url}"
            time_stamp = tr.xpath('./td[3]/text()')[0]

            # 获取详情页数据
            try:
                response = requests.get(detial_url, headers=headers)
                html = response.content.decode('gb2312')
            except:
                continue
            detail_html = etree.HTML(html)

            # 获取内容和附件链接
            try:
                text = detail_html.xpath('//font[@id="Zoom"]//text()')
                text = ''.join([i if i else '' for i in text]).replace(' ', '').replace(' ', '').replace('\t', '')

                # 获取附件链接
                appendix_url_text = ''
                appendix_url_list = detail_html.xpath('//font[@id="Zoom"]//a/@href')
                for appendix_url in appendix_url_list:
                    appendix_uil = 'http://jyt.hebei.gov.cn' + appendix_url
                    appendix_url_text += appendix_uil + ';'
            except:
                text = ''
                appendix_url_text = ''

            print(title, time_stamp, detial_url)
            writer.writerow([title, time_stamp, text, name, url, detial_url, appendix_url_text])

            time.sleep(random.random() / 3)
        time.sleep(random.random())
    file.close()


if __name__ == '__main__':
    get_data('民生工程', '1595832726231', 2)
    get_data('政府信息公开年报', '1414231541890', 2)

