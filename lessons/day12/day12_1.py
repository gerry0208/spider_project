import time

from lessons.selenium import webdriver
from lessons.selenium import By


driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.helloweba.net/demo/2017/unlock/')

# 查找滑块和滑动条标签
slider = driver.find_element(By.XPATH, '//div[@class="bar1 bar"]/div[@class="slide-to-unlock-handle"]')
line = driver.find_element(By.XPATH, '//div[@class="bar1 bar"]/div[@class="slide-to-unlock-bg"]')
# 创建动作链
action_chains = webdriver.ActionChains(driver)
# 使用动作链对象长按滑块
action_chains.click_and_hold(slider)
# 设置滑块移动距离
action_chains.move_by_offset(line.size['width'], 0)
# 执行动作链
action_chains.perform()

time.sleep(3)
