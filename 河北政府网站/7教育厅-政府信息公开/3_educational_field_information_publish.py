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
        tr_list = html.xpath('//table//tr[not(@id="th")]')
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
    id_list = ['1533807631441', '1533807643547', '1533807656246', '1533807972414', '1533808726213', '1533808794703',
               '1533808807647', '1533808821404', '1533808832328', '1533808854669']
    page_num_list = [3, 1, 2, 1, 2, 1, 1, 2, 1, 2]
    name_list = ['基础教育',
                 '职业教育',
                 '高等教育',
                 '民办教育',
                 '学生资助',
                 '教育法规',
                 '国际交流',
                 '思政体卫与学校安全',
                 '语言文字',
                 '师资建设',]
    for id, page_num, name in zip(id_list, page_num_list, name_list):
        get_data(name, id, page_num)

