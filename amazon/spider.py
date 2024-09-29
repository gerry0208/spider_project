import time
from DrissionPage import ChromiumPage, ChromiumOptions
import sys
from threading import Thread


def get_info(browser, url, id):
    tab = browser.new_tab(url)
    # 抓取所有字段
    brand = tab.s_ele('xpath=//tr[@class="a-spacing-small po-brand"]/td[2]/span').text
    name = tab.s_ele('xpath=//h1[@id="title"]/span').text
    tab_keys = tab.s_eles('xpath=//th[@class="a-color-secondary a-size-base prodDetSectionEntry"]').get.texts()
    tab_values = tab.s_eles('xpath=//td[@class="a-size-base prodDetAttrValue"]').get.texts()
    details = {key: value for key, value in zip(tab_keys, tab_values)}

    # 图片url
    photo_urls = tab.s_eles('xpath=//ul/li/span/span/span/span/img').get.attrs('src')
    try:
        photo_url = '\n'.join(photo_urls[:6])
    except:
        photo_url = '\n'.join(photo_urls[:])
    # 获取商品描述
    details = tab.s_eles('xpath=//div[@data-expanded="true"]/table/tbody/tr')
    details = {det.s_ele('xpath=./th').text: det.s_ele('xpath=./td').text for det in details}
    # 获取关于about
    about = tab.s_eles('xpath=//ul[@class="a-unordered-list a-vertical a-spacing-mini"]/li/span').get.texts()

    tab.close()

    return {'id': id, 'Brand': brand, '产品名称': name, '图片地址': photo_url, '商品描述': details, '关于': about}


def run(url, page):
    browser = ChromiumPage()
    browser.get(url)
    browser.wait.doc_loaded()
    if page == 1:
        pass
    else:
        aim_page_url = browser.s_ele(f'xpath=//span[@class="s-pagination-strip"]/a[{int(page) - 1}]').attr('href')
        browser.get(aim_page_url)
        browser.wait.doc_loaded()
    goods_urls = browser.s_eles('xpath=//h2/a').get.attrs('href')
    information = []
    for index, goods_url in enumerate(goods_urls):
        ID = page + '_' + str(index + 1)
        information.append(get_info(browser, goods_url, ID))
    browser.quit()

    return information


res = run('https://www.amazon.co.uk/s?i=merchant-items&me=A1A8TOSJMUGK5U&page=2&qid=1726292497&ref=sr_pg_2', str(2))
# res = run(sys.argv[1], sys.argv[2])
print(res)
