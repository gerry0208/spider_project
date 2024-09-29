import time

import pymongo
from lxml import etree
from lessons.selenium import webdriver
from lessons.selenium import By
from lessons.selenium import Options


def get_total_page():
    print('正在抓取首页数据...')
    while True:
        # 等待页面加载
        while True:
            time.sleep(0.1)
            # 获取所有tr
            html = etree.HTML(driver.page_source)
            tr_list = html.xpath('//tbody/tr[@style=" color:#535353"]')
            if tr_list:
                break
        # 获取登记号+试验状态+药物名称+适应症+试验通俗题目+ID
        for tr in tr_list:
            item = {'登记号': tr.xpath('./td[2]/a/text()')[0].replace('\n', '').replace('\t', ''),
                    '试验状态': tr.xpath('./td[3]/a/text()')[0].replace('\n', '').replace('\t', '').replace('\xa0',
                                                                                                            ' '),
                    '药物名称': tr.xpath('./td[4]/a/text()')[0].replace('\n', '').replace('\t', ''),
                    '适应症': tr.xpath('./td[5]/a/text()')[0].replace('\n', '').replace('\t', ''),
                    '试验通俗题目': tr.xpath('./td[6]/a/text()')[0].replace('\n', '').replace('\t', '')}
            # 插入mongodb
            db.drugtrial.insert_one(item)
        # 下一页按钮
        try:
            next_btn = driver.find_element(By.XPATH, '//a[@aria-label="Next"]/span')
            next_btn.click()
        except Exception as e:
            print('已抓取尾页')
            break


def get_detail_info():
    print('正在抓取详情页数据...')
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[1])
    detail_html = etree.HTML(driver.page_source)
    count = int(detail_html.xpath('//div[@id="toolbar_top"]/div/span[2]/text()')[0])
    for i in range(count - 1):
        # 等待页面加载
        while True:
            time.sleep(0.1)
            if driver.page_source:
                break

        detail_html = etree.HTML(driver.page_source)
        # 获取字段
        item = {'申请联系人': detail_html.xpath('//*[@id="collapseOne"]/div/table/tbody/tr[2]/td[1]/text()')[0],
                '首次公示信息日期': detail_html.xpath('//*[@id="collapseOne"]/div/table/tbody/tr[2]/td[2]/text()')[
                    0].replace('\n', '').replace('\t', '').replace(' ', ''),
                '申请人名称': detail_html.xpath('//*[@id="collapseOne"]/div/table/tbody/tr[3]/td/text()')[0].replace(
                    '\n', '').replace('\t', '')}
        print(item)
        # 更新数据库中对应登记号的数据
        ID = detail_html.xpath('//*[@id="collapseOne"]/div/table/tbody/tr[1]/td[1]/text()')[0]
        db.drugtrial.update_one({'登记号': ID}, {'$set': item})
        # 下一页
        if i == 0:
            driver.find_element(By.XPATH, '//div[@id="toolbar_top"]/div/a').click()
        else:
            driver.find_element(By.XPATH, '//div[@id="toolbar_top"]/div/a[2]').click()
    print('详情页数据抓取完成')


if __name__ == '__main__':

    options = Options()
    # 设置自动化特性的关闭，防止被服务器检测到是由selenium驱动的
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('--disable-blink-features=AutomationControlled')
    # 关闭证书报错
    options.add_argument('ignore-certificate-errors')
    # 设置无头模式
    # options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get('http://www.chinadrugtrials.org.cn/clinicaltrials.searchlist.dhtml')
    time.sleep(3)
    # mongodb初始化
    client = pymongo.MongoClient()
    db = client['药物试验']
    try:
        db.create_collection('drugtrial')
    except Exception as e:
        print('数据集已存在')

    # 获取每页信息
    get_total_page()
    # 回到第一页
    page_1 = driver.find_element(By.XPATH, '//a[@onclick="gotopage(1)"]')
    page_1.click()
    # 点击第一条，进入详情页
    driver.find_element(By.XPATH, '//a[@name="1"]').click()
    time.sleep(1)
    # 获取全部详情页数据
    get_detail_info()

    time.sleep(10)
