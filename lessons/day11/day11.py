import re
import time
from lxml import etree
import csv

from lessons.selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://m.weibo.cn/p/106003type=25&t=3&disable_hot=1&filter_type=realtimehot?jumpfrom=weibocom')
time.sleep(1)

html = etree.HTML(driver.page_source)
data_list = html.xpath('//div[@class="card card11"][1]//div[@class="box-left m-box-col m-box-center-a"]')

# 收集微博热搜数据
rank_list = []
for data in data_list:
    index_src = data.xpath('./span[1]/img/@src')[0]
    index = re.search(r'(\d+)(?=.png)', index_src)
    if index is not None:
        index = index.group()
        title = data.xpath('./span[2]/span[1]/text()')[0].split('\n')[0]
        info = data.xpath('./span[2]/span[2]/text()')[0].split(' ')[0]
        if info.isdigit():
            info, value = '暂无', info
        else:
            info = data.xpath('./span[2]/span[2]/text()')[0].split(' ')[0]
            value = data.xpath('./span[2]/span[2]/text()')[0].split(' ')[1]

        lst = [index, title, info, value]
        rank_list.append(lst)

# 保存热搜数据
with open('微博热搜.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['排名', '标题', '类型', '热度'])
    writer.writerows(rank_list)

time.sleep(3)
