import time
import mysql.connector
from DrissionPage import ChromiumPage

page = ChromiumPage()
page.get('https://pifa.pinduoduo.com/')
# 点击数码, 进入新页面
page.ele('xpath=//*[@id="root"]/div/div[2]/div/div[2]/div[2]/div[1]/div/article/div/div[7]/a[1]/span').click()
tab = page.latest_tab
# 回滚一次页面，避免页面不加载
time.sleep(2)
tab.run_js('window.scrollTo(0, document.body.scrollHeight)')
time.sleep(2)
tab.run_js('window.scrollTo(0, -1000)')
# 批量获取数据
while True:
    # 获取div标签数量，大于300则退出循环，否则向下滚动页面至底部
    div_list = tab.eles('xpath=//div[@class="goods-item"]')
    print(len(div_list))
    if len(div_list) > 300:
        break
    else:
        tab.run_js('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(0.5)
data = []
for div in div_list:
    title = div.ele('xpath=./div/a/div[2]/div/div/div').text
    price = div.ele('xpath=./div/a/div[3]/span[@class="price-text"]').text
    store = div.ele('xpath=./div/a/div[@class="store-name"]/span').text
    sold_quantity = div.ele('xpath=./div/a/div/span[@class="sold-quantity"]').text
    item = {'标题': title, '价格': price, '店铺': store, '销量': sold_quantity}
    data.append(item)
    print(item)

# 将数据存入mysql
db = mysql.connector.connect(host='localhost', user='root', password='root', database='test')
cursor = db.cursor()
try:
    cursor.execute('CREATE TABLE pinduoduopifa(id INT AUTO_INCREMENT PRIMARY KEY, 标题 VARCHAR(255), 价格 VARCHAR(255), 店铺 VARCHAR(255), 销量 VARCHAR(255))')
except Exception as e:
    print(e)
sql = 'INSERT INTO pinduoduopifa(标题, 价格, 店铺, 销量) values(%s, %s, %s, %s)'
try:
    cursor.executemany(sql, data)
    db.commit()
    print('插入成功')
except Exception as e:
    print(e)
    db.rollback()
    print('插入失败')
finally:
    db.close()
