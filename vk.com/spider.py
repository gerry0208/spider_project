import csv
import time
from DrissionPage import ChromiumPage


delay = 3

page = ChromiumPage()
# 进入登录页面
page.get('https://vk.com')
page.wait.doc_loaded()
while True:
    profile = page.s_ele('xpath=//*[@id="top_profile_link"]/img')
    if profile:
        break
    print('请登录')
    time.sleep(1)
# 进入我喜欢
page.get('https://vk.com/video/liked')
page.scroll.to_bottom()
page.wait.doc_loaded()
my_liked_urls = page.s_eles('xpath=//a[@class="VideoCard__thumbLink video_item__thumb_link"]').get.attrs('href')
with open('我喜欢_url.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    for url in my_liked_urls:
        writer.writerow([url])
print('我喜欢_url.csv生成完毕')
# 输入搜索词
while True:
    ID = input('请输入视频id：')
    new_tab = page.new_tab('https://vk.com/video/@id' + ID)
    new_tab.wait.doc_loaded()
    new_tab.scroll.to_bottom()
    new_tab.wait.doc_loaded()
    user_urls = new_tab.s_eles('xpath=//a[@class="VideoCard__thumbLink video_item__thumb_link"]').get.attrs('href')
    with open('user_url.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for url in user_urls:
            writer.writerow([url])
    print(ID + '主页视频url已存入user_url.csv')
