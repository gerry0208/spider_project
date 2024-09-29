import csv
import time
import requests
from lxml import etree

url = "https://www.hebei.gov.cn/columns/8dff597e-a95c-4b20-b321-a5320af40141/templates/09a19324-88df-4949-b69b-f29b625e5e59/blocks/1af38c7c-a84e-4761-8d1c-ce69b66e8d80"

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
}

with open('人民政府_省政府办公厅文件.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['序号', '标题', '发文日期', '效力状态', '内容', '主题'])
    for i in range(1, 31):
        params = {
            'page': i,
            'fix': "0"
        }
        response = requests.get(url, params=params, headers=headers)
        html = etree.HTML(response.text)

        index = html.xpath('//li[@class="xxgk_gfxwjk-list-li"]/p[1]/text()')
        title = html.xpath('//li[@class="xxgk_gfxwjk-list-li"]/p[2]/a/@title')
        date = html.xpath('//li[@class="xxgk_gfxwjk-list-li"]/p[4]/text()')
        state = html.xpath('//li[@class="xxgk_gfxwjk-list-li"]/p[5]/text()')
        sub_url = html.xpath('//li[@class="xxgk_gfxwjk-list-li"]/p[2]/a/@href')
        for index, title, date, state, sub_url in zip(index, title, date, state, sub_url):
            response = requests.get("https://www.hebei.gov.cn" + sub_url, headers=headers)
            html = etree.HTML(response.text)
            theme = html.xpath('//div[@class="wjct"]/p[6]/text()')
            text = html.xpath('//div[@id="zoom"]/div/text()')
            content = ''.join(text)
            try:
                writer.writerow([index, title, date, state, content, theme[0]])
            except:
                writer.writerow([index, title, date, state, content, theme])
            print([index, title, date, state, content, theme])
            print('正在抓取第', i, '页第', index, '条数据')
            time.sleep(0.1)

        time.sleep(1)
