import time
import pymongo
from lxml import etree
from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions

co = ChromiumOptions()
co.headless()

page = ChromiumPage(co)
page.get("https://weibo.com/1323527941/OumcBtDBK#comment")
# 设置cookie并刷新页面
cookie = {
    "XSRF-TOKEN": "1xdaS1kT1iY8ZOgjxid89T-4",
    "SCF": "Ai1P5GoPk7ImgoZwD0PRWd0V7FxtxLz5JaQhy0CLVxDRwnCIe_uu32iP5VqS_i9gVr9QSqSessdMGXNEhqar1cc.",
    "SUB": "_2A25Ly3OTDeRhGeFN6lMW8izFyTWIHXVoqYlbrDV8PUNbmtB-LRX4kW9NQGXsQ4I9sflA17EjEOJVZkFk4cTH0t3a",
    "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9W5xJnV3GKFgeL0siaYSfNBQ5JpX5KzhUgL.FoM0eK2Neoz4eo.2dJLoIpBLxKMLBK5LBoBLxKMLB-2L1KMfentt",
    "ALF": "02_1727434947",
    "WBPSESS": "lTPiWmhuFhmA28R4ScLsIZqutMPbx4S0yCgYJaduiM9OAefOQ9SfxM9960CneB95QxESpezvD3PfeWR2TwCHTrVslpxVgEB_TwbbJ027aD5r4rC7xaLoODMVT8eVqVb3ZgM8AYi-OdvBmg2vwArHRw=="
}
page.set.cookies(cookie)
page.refresh()
time.sleep(1)

item_list = []
# 滚动页面
while True:
    # 获取html
    html = etree.HTML(page.html)
    # 获取div标签列表
    div_list = html.xpath('//div[@class="vue-recycle-scroller__item-wrapper"]/div')
    # 获取每个div标签的字段
    for div in div_list:
        try:
            ID = div.xpath('.//div[@class="text"]/a/text()')[0]
            timestamp = div.xpath(
                './/div[@class="info woo-box-flex woo-box-alignCenter woo-box-justifyBetween"]/div/text()'
            )[0]
            content = div.xpath('.//div[@class="text"]/span/text()')[0]
            address = div.xpath(
                './/div[@class="info woo-box-flex woo-box-alignCenter woo-box-justifyBetween"]/div/span/text()'
            )[0]
            item = {"ID": ID, "时间": timestamp, "内容": content, "地址": address}
            if item not in item_list:
                item_list.append(item)
            print(item)
        except:
            pass
    page.run_js(f"window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(3)
    if len(item_list) > 100:
        break

client = pymongo.MongoClient()
db = client["微博"]
try:
    db.create_collection("comment")
except:
    print("数据集已存在")

db.comment.insert_many(item_list)
