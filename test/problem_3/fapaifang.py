import time

from DrissionPage import ChromiumPage
from lxml import etree


# 筛选多页数据
def get_info(city, page_nums):
    html = etree.HTML(tab.html)
    li_list = html.xpath('//div[@data-spm="paiList"]/ul/li')
    data = []
    for i in range(page_nums):
        for li in li_list:
            title = li.xpath('./a/div[@class="header-section "]/p/text()')[0].replace('\n', '').replace(' ', '')
            base_price = li.xpath('./a/div[@class="info-section"]/p[1]/span[2]/em[2]/text()')[0] + '万'
            data.append((title, city, base_price))
            print(title, city, base_price)
        # 点击翻页按钮
        tab.ele('xpath=/html/body/div[4]/div[4]/a[6]').click()
        time.sleep(1)
    return data


page = ChromiumPage()
# 进入登录页面
page.get('https://login.taobao.com/member/login.jhtml')
page.ele('@name=fm-login-id').input('16727283693')
page.ele('@name=fm-login-password').input('Alwayshappy3414')
page.ele('xpath=//*[@id="login-form"]/div[6]/button').click()
time.sleep(2)
page.get('https://www.taobao.com/')
time.sleep(2)
tab = page.latest_tab
# 点击司法拍卖
tab.ele("@text()=司法拍卖").click()
# 切换到最新页面
tab = page.latest_tab
tab.ele('@text()=住宅用房').click()
tab = page.latest_tab

whole_data = []
# 获取北京数据
tab.ele('xpath=/html/body/div[4]/div[2]/ul[2]/li/div[2]/ul/li[1]/em/a').click()
time.sleep(1)
whole_data += get_info('北京', 4)
# 获取上海数据
tab.ele('xpath=/html/body/div[4]/div[2]/ul[2]/li/div[2]/ul/li[9]/em/a').click()
time.sleep(1)
whole_data += get_info('上海', 4)
# 获取广州数据
tab.ele('xpath=/html/body/div[4]/div[2]/ul[2]/li/div[2]/ul/li[19]/em/a').click()
time.sleep(1)
tab.ele('xpath=/html/body/div[4]/div[2]/ul[2]/li/div[2]/ul/li[19]/div/ul/li[1]/em/a').click()
time.sleep(1)
whole_data += get_info('广州', 4)

# 存入mysql数据库
import mysql.connector

db = mysql.connector.connect(host='localhost', user='root', password='root', database='test')

cursor = db.cursor()
try:
    cursor.execute(
        'CREATE TABLE fapaifang (id INT AUTO_INCREMENT PRIMARY KEY, city VARCHAR(255), title VARCHAR(255), base_price VARCHAR(255))')
except Exception as e:
    pass
# 插入数据
sql = 'INSERT INTO fapaifang(city, title, base_price) values(%s, %s, %s)'
try:
    cursor.executemany(sql, whole_data)
    db.commit()
    print('插入成功')
except Exception as e:
    print(e)
    db.rollback()
    print('插入失败')
finally:
    db.close()