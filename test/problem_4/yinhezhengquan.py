import time

import pymongo
from DrissionPage import ChromiumPage

page = ChromiumPage()
page.get('http://www.chinastock.com.cn/newsite/cgs-services/stockFinance/businessAnnc.html?type=marginList')
time.sleep(2)
# 点击融资融券业务公告分类
page.ele('xpath=//*[@id="accordion"]/div[1]/div[1]/div/a').click()
time.sleep(2)
# 点击关于调整融资融券标的证券名单的公告
page.ele('xpath=//*[@id="collapseOne"]/div/ul/li[2]').click()
time.sleep(2)

data = []
for _ in range(3):
    # 筛选字段：标题、时间
    title_list = page.eles('xpath=//div[@id="notice"]/div/div/a')
    time_list = page.eles('xpath=//div[@id="notice"]/div/div[2]')

    for title, timestamp in zip(title_list, time_list):
        item = {'标题': title.text, '发布时间': timestamp.text}
        data.append(item)
        print(item)
    page.ele('xpath=//*[@id="businessAnnc"]/div[2]/div[2]/div[2]/div[1]/div/div[3]/div[2]/li[8]/a').click()

client = pymongo.MongoClient()
db = client['中国银河证券']
try:
    db.create_collection('notice')
except Exception as e:
    print('数据集已存在')
db.notice.insert_many(data)
client.close()

page.quit()
