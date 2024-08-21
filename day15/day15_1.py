import re
from fontTools.ttLib import TTFont
import requests
from DrissionPage import ChromiumPage
from lxml import etree

page = ChromiumPage()
page.set.window.max()
page.get('https://www.qidian.com/rank/yuepiao/')

# 筛选月票榜数据, 得到书名和月票数密文
html = etree.HTML(page.html)
book_name_lst = html.xpath('//div[@class="book-img-text"]/ul/li/div[@class="book-mid-info"]/h2/a/text()')
ticket_code_lst = html.xpath('//div[@class="book-img-text"]/ul/li/div[3]/div/p/span/span/text()')
ticket_code_raw_lst = []
for ticket_code in ticket_code_lst:
    ticket_code_raw_lst.append([ord(c) for c in ticket_code])

# 获取字体文件
font_re = r"format\('eot'\); src: url\('(.*?)'\) format\('woff'\)"
font_url = re.findall(font_re, page.html)[0]
response = requests.get(font_url)
with open('font.woff', 'wb') as file:
    file.write(response.content)

# 读取字体文件, 获取字体映射
font = TTFont('font.woff')
cmap = font.getBestCmap()
# 创建英文数字和阿拉伯数字的映射字典
num_dict = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'zero': '0',
    'period': '.',
}
# 将月票密文通过cmap、num_dict映射转换成数字，储存到ticket_val_lst中
ticket_val_lst = []
for ticket_code_raw in ticket_code_raw_lst:
    val = ''.join([num_dict[cmap[i]] for i in ticket_code_raw])
    ticket_val_lst.append(val)

# 打印结果
for name, ticket in zip(book_name_lst, ticket_val_lst):
    print('书名: {}    月票: {}'.format(name, ticket))
