import time

from Demos.mmapfile_demo import offset
from DrissionPage import ChromiumPage
import csv

content = input('请输入检索内容：')
start_day = input('请输入起始年月日(ep:2024-09-07)：')
end_day = input('请输入截止年月日(ep:2024-09-07)：')

delay = 5


def wait_for_load(tab):
    while True:
        cnt = 0
        height = tab.rect.size[1]
        tab.scroll.to_bottom()
        print('正在滚动加载...')
        while tab.rect.size[1] == height:
            cnt += 1
            time.sleep(0.1)
            if cnt > delay / 0.1:
                return


def get_comments():
    # 获取评论信息
    comment_set = []
    offset_1 = 0
    while True:
        detail_tab.wait.doc_loaded()
        comment_list = detail_tab.s_eles('xpath=//div[@class="css-175oi2r"]/div/div/article/div/div/div[2]/div[2]')
        if comment_list:
            for comment in comment_list:
                try:
                    comment_text = comment.s_ele('xpath=/div[2]//span').text
                    if comment_text in comment_set:
                        continue
                    comment_time = comment.s_ele('xpath=/div[1]//time').attr('datetime')
                    writer.writerow(('', '', '', '', comment_time, comment_text))
                    comment_set.append(comment_text)
                    print('评论：', comment_time, comment_text)
                except:
                    pass
        if offset_1 > detail_tab.rect.size[1] - 400:
            print('评论已加载完毕')
            return

        detail_tab.scroll.up(400)
        offset_1 += 400


page = ChromiumPage()
page.get('https://x.com/home')
first_tab = page.get_tab(1)
# 等待登录
first_tab.wait.ele_displayed('xpath=//input[@autocapitalize="sentences"]')
# 输入检索信息
first_tab.ele('xpath=//input[@autocapitalize="sentences"]').input(f'{content} until:{end_day} since:{start_day}\n')

# 筛选数据
name_list = []
offset = 0
with open('TwitterBlog.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(('用户名', '时间', '地区', '内容', '评论时间', '评论内容'))
    while True:
        first_tab.wait.doc_loaded()
        div_list = first_tab.s_eles('xpath=//div[@class="css-175oi2r r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"]')
        if div_list:
            for div in div_list:
                name = div.s_ele(
                    'xpath=//div[@class="css-175oi2r r-1awozwy r-18u37iz r-1wbh5a2 r-dnmrzs"]/div[@dir="ltr"][1]/span/span').text
                if name in name_list:
                    continue
                name_list.append(name)
                time_stamp = div.s_ele('xpath=//div[@class="css-175oi2r r-18u37iz r-1q142lx"]/a/time').attr('datetime')
                span = div.s_eles(
                    'xpath=//div[@class="css-175oi2r"]/div[@dir="auto"]/span[@class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3"]')
                text = ''.join(span.get.texts())
                user_url = div.s_ele('xpath=/div/div/div/div/div/div/div/a').attr('href')
                user_tab = page.new_tab(user_url)
                try:
                    loc = user_tab.s_ele(
                        'xpath=//div[@class="css-175oi2r r-3pj75a r-ttdzmv r-1ifxtd0"]//span[@data-testid="UserLocation"]/span/span').text
                except:
                    loc = None
                user_tab.close()
                item = (name, time_stamp, loc, text, '', '')
                writer.writerow(item)
                print(item)
                # 进入评论页面
                detail_url = div.s_ele('xpath=/div/div/div/div/div/div[2]/div/div[3]/a').attr('href')
                detail_tab = page.new_tab(detail_url)
                # 加载完整评论页面
                wait_for_load(detail_tab)
                get_comments()
                detail_tab.close()

            if offset > first_tab.rect.size[1]:
                break

            first_tab.scroll.down(400)
            offset += 400

page.quit()
