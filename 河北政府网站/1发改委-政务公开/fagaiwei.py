import csv
import re
import time
from retrying import retry
from DrissionPage import ChromiumPage
from threading import Thread


@retry(stop_max_attempt_number=3)
def get_detail(li):
    date = li.s_ele('tag:span').text

    url = li.s_ele('tag:a').attr('href')
    detail_tab = page.new_tab(url)
    detail_tab.wait.doc_loaded()

    title = detail_tab.s_ele('xpath=//h1').text

    text_list = detail_tab.s_eles('xpath=//p//span').get.texts()
    text = ''.join(text_list)
    # print(text)
    a_urls = detail_tab.s_eles('tag:a').get.attrs('href')
    pattern = r'^http.+?\.(?:pdf|doc|docx|wps|xls|xlsx)$'
    append_urls = []
    for a_url in a_urls:
        if a_url:
            if re.match(pattern, a_url):
                print(a_url)
                append_urls.append(a_url)
    if append_urls:
        append_urls = '\r\n'.join(append_urls)
    detail_tab.close()
    return title, date, text, url, append_urls


def get_info(tab, refer_text, refer_url):
    print('正在爬取 ' + refer_text + '...')
    while True:
        tab.wait.doc_loaded()
        try:
            li_list = tab.s_eles('xpath=//ul[@class="list_rgterji"]/li')
            if not li_list:
                li_list = tab.s_eles('xpath=//div[@id="search"]/ul/li')
            item_list = []
        except:
            print('')
            continue

        for li in li_list:
            title, date, text, url, append_urls = get_detail(li)
            if not text:
                print(url + ' 无内容')
                continue
            item_list.append([title, date, text, refer_text, refer_url, url, append_urls])

        writer.writerows(item_list)

        next_btn = tab.ele('text=下一页', timeout=1)
        if next_btn:
            next_btn.click()
        else:
            tab.close()
            return


page = ChromiumPage()
page.get('https://hbdrc.hebei.gov.cn/jhlm/jhzcfg/')
page.wait.doc_loaded()
level_1_headings = page.s_eles('xpath=//ul[@class="navullef"]/li/a').get.texts()
level_1_urls = [
    'https://hbdrc.hebei.gov.cn/xxgk_2232/',
    'https://hbdrc.hebei.gov.cn/jhlm/jhzcfg/',
    'https://hbdrc.hebei.gov.cn/ztzl/zdxmxxgk/xmss/',
    'https://hbdrc.hebei.gov.cn/jhlm/jhghjh/',
    'https://hbdrc.hebei.gov.cn/jhlm/jhjjyx/',
    'https://hbdrc.hebei.gov.cn/jhlm/jhfzgh/',
    'https://hbdrc.hebei.gov.cn/tzgg_1234/',
    'https://hbdrc.hebei.gov.cn/jhlm/jhtzgl/',
    'https://hbdrc.hebei.gov.cn/cyfz_1232/',
    'https://hbdrc.hebei.gov.cn/dwkf_1236/',
    'https://hbdrc.hebei.gov.cn/jjhz/',
    'https://hbdrc.hebei.gov.cn/jggl_1243/jgzcfg/',
]

thread_list = []
with open('发改委_政务公开.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['标题', '日期', '内容', '所属一级类别', '来源网站', '访问地址', '附件地址(为空则无)'])
    for level_1_heading, level_1_url in zip(level_1_headings, level_1_urls):
        new_tab = page.new_tab(level_1_url)
        t = Thread(target=get_info, args=(new_tab, level_1_heading, level_1_url))
        thread_list.append(t)
        t.start()
        time.sleep(3)
    for t in thread_list:
        t.join()
