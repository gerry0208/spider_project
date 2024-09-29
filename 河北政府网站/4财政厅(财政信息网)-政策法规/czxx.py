import time
from DrissionPage import SessionOptions, SessionPage, ChromiumOptions, Chromium
import csv
from fake_useragent import FakeUserAgent


# SessionPage请求方法
def session_get(url):
    co = SessionOptions()
    co.set_headers({'user-agent': FakeUserAgent().random})
    Session = SessionPage(co)
    Session.get(url)
    while Session.response.status_code != 200:
        time.sleep(0.1)
        co = SessionOptions()
        co.set_headers({'user-agent': FakeUserAgent().random})
        Session = SessionPage(co)
        Session.get(url)
    return Session


domain_url = 'https://czt.hebei.gov.cn/zcfg/'
session = session_get(domain_url + 'ysl/')
file = open('财政信息网_政策法规.csv', 'a', encoding='utf-8', newline='')
writer = csv.writer(file)
writer.writerow(['标题', '时间', '内容', '一级类别', '来源网站', '访问地址', '附件链接'])

a_list = session.eles('xpath=//div[@class="col-lg-3 left visible-lg"]/ul/li/a')
for i, a in enumerate(a_list, 0):
    # 获取一级类别
    heading = a.text

    # 获取来源网站并打开
    head_url = a.attr('href')
    if i == 0:
        head_url = head_url + 'ysl/'
    else:
        head_url = domain_url + head_url.replace('https://czt.hebei.gov.cn/', '')

    # 使用driver模式打开页面，监听列表页数据包
    driver_co = ChromiumOptions()
    driver_co.auto_port()
    browser = Chromium(addr_or_opts=driver_co)
    page = browser.latest_tab
    page.listen.start(targets='list_292.htm')
    page.get(head_url)
    packet = page.listen.wait()

    # 获取页数
    frame = page.get_frame('@frameborder=0')
    page_num = int(frame.ele('xpath=//div[@class="pageInfo list_navigator"]/span[last()]/a').text)

    # 循环获取列表页数据包
    for j in range(page_num):
        # 获取列表页数据包url
        if j == 0:
            list_url = packet.url
        else:
            list_url = packet.url.replace('list_292.htm', f'list_292_{j}.htm')
        print(f'第{j + 1}页数据包URL：', list_url)

        # 使用SessionPage发送请求
        session = session_get(list_url)

        # 提取列表数据
        item_list = session.eles('xpath=//table[@class="xitable"]')

        # 遍历列表数据
        print('------------------------------------------------')
        for item in item_list:
            # 提取标题、时间、主题、访问地址
            time_stamp = item.ele('xpath=//tr/td[4]').text
            title = item.ele('xpath=//tr/td[1]/a').text
            sub_url = item.ele('xpath=//tr/td[1]/a').attr('href')
            print(title, time_stamp, sub_url)

            # 打开s模式，请求子页面
            session = session_get(sub_url)

            # 提取正文和附件链接
            try:
                text = session.ele('xpath=//div[@class="c_content"]').text
                appendix_url = session.eles('xpath=//div[@class="c_appendix"]/fieldset/ul/li/a').get.attrs('href')
            except:
                text = session.ele('xpath=//div[@class="content"]').text
                appendix_url = session.eles('xpath=//div[@class="content"]/div/a').get.attrs('href')

            text = text.replace('\u3000', '').replace(' ', '').replace('\n\n', '\n')
            appendix_url = '\n'.join(appendix_url)

            # 写入csv文件
            item = [title, time_stamp, text, heading, head_url, sub_url, appendix_url]
            writer.writerow(item)

        print('------------------------------------------------')

    browser.close_tabs(browser.tab_ids)
    print(heading + '类已抓取完成...')
    time.sleep(1)

file.close()
