import requests
from lxml import etree
from fake_useragent import FakeUserAgent

from my_map import my_map

url = 'https://fanqienovel.com/page/7143038691944959011'
headers = {
    'User-Agent': FakeUserAgent().random
}

# 获取目录页的章节路径(1-10章)
response = requests.get(url, headers=headers)
flyleaf_html = etree.HTML(response.text)
path_lst = flyleaf_html.xpath('//div[@class="chapter-item"]/a/@href')[:10]

for path in path_lst:
    # 获取每一章的原始数据
    cpt_url = 'https://fanqienovel.com' + path
    response = requests.get(cpt_url, headers=headers)
    cpt_html = etree.HTML(response.text)
    # 获取每章的标题和密文
    title = cpt_html.xpath('//h1[@class="muye-reader-title"]/text()')[0]
    print("\n" + title)
    code = cpt_html.xpath('//div[@class="muye-reader-content noselect"]/div/p/text()')
    # 根据自定义映射字典my_map将密文转换为明文
    for enc_line in code:
        dec_line = ''
        for enc_char in enc_line:
            dec_char = my_map.get(str(ord(enc_char)))
            if dec_char is None:
                dec_char = enc_char
            dec_line += dec_char
        print(dec_line)