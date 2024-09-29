import time

import requests
from PIL import Image, ImageDraw
from lxml import etree
from lessons.selenium import webdriver
from lessons.selenium import By
from lessons.selenium import Options

from chaojiying import Chaojiying_Client

options = Options()
# 设置自动化特性的关闭，防止被服务器检测到是由selenium驱动的
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument('--disable-blink-features=AutomationControlled')
# 关闭证书报错
options.add_argument('ignore-certificate-errors')

# 实例化并打开谷歌浏览器
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get('https://passport.fang.com/?backurl=https%3A%2F%2Fwww1.fang.com%2F')

# 点击账号密码登录
driver.find_element(By.XPATH, '//div[@class="login-cont"]/dt/span[2]').click()
# 输入账号和密码
driver.find_element(By.XPATH, '//input[@id="username"]').send_keys('jaychan0218')
driver.find_element(By.XPATH, '//input[@id="password"]').send_keys('1a2b3c4D')
time.sleep(1)
# 点击登录按钮
driver.find_element(By.XPATH, '//button[@id="loginWithPswd"]').click()
time.sleep(1)
# 定位滑块标签并点击
slider = driver.find_element(By.XPATH, '//*[@id="mathCodePswd"]/div/div/div[5]')
webdriver.ActionChains(driver).move_to_element(slider).perform()
# slider.click()
# time.sleep(3)
# 获取验证图片
html = etree.HTML(driver.page_source)
src = html.xpath('//*[@id="mathCodePswd"]/div/div/div[2]/div/img[1]/@src')[0]
response = requests.get(src)
with open('验证图片.png', 'wb') as file:
    file.write(response.content)

# 发送图片给超级鹰，获取坐标数据
chaojiying = Chaojiying_Client('gerrychan', 'gerrychan*', '962323')
img = open('验证图片.png', 'rb').read()
data = chaojiying.PostPic(img, 9101)['pic_str']
x = int(data.split(',')[0])
y = int(data.split(',')[1])
# 使用图片处理库，在返回的坐标上打一个小红点，用于测试超级鹰识别是否正确
img = Image.open('验证图片.png')
draw = ImageDraw.Draw(img)
box = (x-5, y-5, x+5, y+5)
draw.ellipse(box, fill='red')
img.save('验证图片小红点.png')

# 使用动作链移动小滑块到目标位置
action_chains = webdriver.ActionChains(driver)
slider = driver.find_element(By.XPATH, '//*[@id="mathCodePswd"]/div/div/div[5]')
action_chains.click_and_hold(slider)
action_chains.move_by_offset(int(x - slider.size['width']/2), 0)
action_chains.perform()
action_chains.release().perform()

time.sleep(60)