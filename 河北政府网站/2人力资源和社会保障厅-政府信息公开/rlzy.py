import csv
import re
import time
from DrissionPage import ChromiumPage, ChromiumOptions
from threading import Thread
from threading import Lock

'''
https://rst.hebei.gov.cn/rsmh_file/subjectPictures/20240201/fe0af8e2-7c75-4489-b9e3-fb0e22e9a1ea10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80-10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80/index.html?article=&column=1426
https://rst.hebei.gov.cn/rsmh_file/subjectPictures/20240201/fe0af8e2-7c75-4489-b9e3-fb0e22e9a1ea10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80-10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80/index.html?article=&column=1084
https://rst.hebei.gov.cn/rsmh_file/subjectPictures/20240201/fe0af8e2-7c75-4489-b9e3-fb0e22e9a1ea10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80-10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80/index.html?article=&column=1085
https://rst.hebei.gov.cn/rsmh_file/subjectPictures/20240201/fe0af8e2-7c75-4489-b9e3-fb0e22e9a1ea10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80-10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80/index.html?article=&column=1458
'''
lock = Lock()

# def get_data(index, parent_url):
#     tab = page.new_tab(parent_url)
#     time.sleep(3)
#     # 获取一级类别和来源网站
#     parent_title = tab.ele(f'xpath=//div[@class="aside"]/div[4]/div[2]/div[2]/ul/li[{index}]/span').text
#     # 记录每个类别的文章数量
#     num = tab.eles('xpath=//*[@id="app"]/div/div[2]/div[2]/div[2]/div/ul/li')[-1].text
#     num = re.findall(r'总共(\d+)条', num)[0]
#     num = int(num)
#     cnt = 0
#     while True:
#         if cnt >= num:
#             break
#         data = []
#         j = 1
#         page_num = len(tab.s_eles('xpath=//tr'))
#         while j <= page_num:
#             # 获取标题和日期
#             title_container = tab.ele(f'xpath=//tr[{j}]/td[1]')
#             title = title_container.text.replace(' ', '')
#             date = tab.s_ele(f'xpath=//tr[{j}]/td[2]').text
#             # 进入详情页，获取内容和url
#             title_container.click()
#             time.sleep(0.5)
#             content = tab.s_eles('xpath=//p').get.texts()
#             content = ''.join(content).replace(' ', '').replace('\n', '')
#             its_url = tab.url
#             # 返回上级页面
#             if index == 4:
#                 tab.ele('xpath=//*[@id="app"]/div/div[2]/div[2]/div[1]/div[1]/div').click()
#             else:
#                 tab.ele(f'xpath=//div[@class="aside"]/div[4]/div[2]/div[2]/ul/li[{index}]').click()
#             time.sleep(0.5)
#             if not (title and date and content and its_url):
#                 print('数据缺失')
#                 continue
#             item = [title, date, content, parent_title, parent_url, its_url]
#             data.append(item)
#             lock.acquire()
#             print(index, title, date)
#             print(content)
#             lock.release()
#             j += 1
#             cnt += 1
#         tab.ele('text=下一页').click()
#         time.sleep(2)
#         lock.acquire()
#         writer.writerows(data)
#         lock.release()
#
#     tab.close()
#     print('已抓取' + parent_title)


# if __name__ == "__main__":
#     # co = ChromiumOptions().headless()
#     page = ChromiumPage()
#     url_list = [
#         'https://rst.hebei.gov.cn/rsmh_file/subjectPictures/20240201/fe0af8e2-7c75-4489-b9e3-fb0e22e9a1ea10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80-10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80/index.html?article=&column=1426',
#         'https://rst.hebei.gov.cn/rsmh_file/subjectPictures/20240201/fe0af8e2-7c75-4489-b9e3-fb0e22e9a1ea10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80-10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80/index.html?article=&column=1084',
#         'https://rst.hebei.gov.cn/rsmh_file/subjectPictures/20240201/fe0af8e2-7c75-4489-b9e3-fb0e22e9a1ea10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80-10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80/index.html?article=&column=1085',
#         'https://rst.hebei.gov.cn/rsmh_file/subjectPictures/20240201/fe0af8e2-7c75-4489-b9e3-fb0e22e9a1ea10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80-10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80/index.html?article=&column=1458'
#     ]
#     with open('人力资源和社会保障厅_政策法规+政府信息公开年报.csv', 'w', encoding='utf-8', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(['标题', '日期', '内容', '所属一级类别', '来源网站', '访问地址'])
#         thread_list = []
#         for i, url in enumerate(url_list):
#             t = Thread(target=get_data, args=(i + 1, url))
#             thread_list.append(t)
#             t.start()
#         for t in thread_list:
#             t.join()

page = ChromiumPage()
url = 'https://rst.hebei.gov.cn/rsmh_file/subjectPictures/20240201/fe0af8e2-7c75-4489-b9e3-fb0e22e9a1ea10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80-10_%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80/index.html?article=&column=1153'
page.get(url)
time.sleep(3)
num = len(page.s_eles('xpath=//tr'))
print(num)
data = []
for i in range(1, num+1):
    title = page.ele(f'xpath=//tr[{i}]/td[1]')
    date = page.s_ele(f'xpath=//tr[{i}]/td[2]').text
    title.click()
    title = title.text.replace(' ', '')
    time.sleep(0.5)
    content = page.s_eles('xpath=//p').get.texts()
    content = ''.join(content).replace(' ', '').replace('\n', '')
    its_url = page.url
    page.ele('xpath=//*[@id="app"]/div/div[2]/div[2]/div[1]/div[5]/div/div[2]/a').click()
    time.sleep(1)
    item = [title, date, content, '政府信息公开年报', url, its_url]
    print(item)
    data.append(item)

with open('人力资源和社会保障厅_政策法规+政府信息公开年报.csv', 'a', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)