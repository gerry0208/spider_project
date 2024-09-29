import time

from lessons.selenium import webdriver
from lessons.selenium import By

from chaojiying import Chaojiying_Client

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.chaojiying.com/user/login/')
time.sleep(1)
# 输入账户名和密码
driver.find_element(By.XPATH, '//input[@name="user"]').send_keys('gerrychan')
time.sleep(1)
driver.find_element(By.XPATH, '//input[@type="password"]').send_keys('gerrychan*')
# 获取验证码图片
pic = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/form/div/img')
pic.screenshot('验证码.png')
# 发送图片给超级鹰，获取json数据
chaojiying = Chaojiying_Client('gerrychan', 'gerrychan*', '962323')
img = open('验证码.png', 'rb').read()
data = chaojiying.PostPic(img, 1902)
# 填入验证码并登录
driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/form/p[3]/input').send_keys(data['pic_str'])
time.sleep(1)
driver.find_element(By.XPATH, '//input[@type="submit"]').click()

time.sleep(3)