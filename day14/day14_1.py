from DrissionPage import ChromiumPage

page = ChromiumPage()
page.set.window.max()
page.get('https://www.helloweba.net/demo/2017/unlock/')
# 查找滑块和滑动条元素
slider = page.ele('xpath=//div[@class="bar1 bar"]/div[3]')
line = page.ele('xpath=//div[@class="bar1 bar"]/div[1]')
# 获取滑块和滑动条的宽度
width_1 = slider.rect.size[0]
width_2 = line.rect.size[0]
# 使用动作链移动滑块
page.actions.hold(slider).move(width_2 - width_1, 0).release(slider)
