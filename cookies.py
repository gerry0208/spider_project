import time

from DrissionPage import ChromiumPage
import queue

queue = queue.Queue(10)


def update_cookies():
    page = ChromiumPage()
    url = 'https://movie.douban.com/subject/1292052/reviews'
    login_url = 'https://accounts.douban.com/passport/login'
    cookie_list = []
    with open('手机号.txt', 'r+', encoding='utf-8') as file:
        phone_numbers = file.read().split('\n')
        for phone_number in phone_numbers:
            tab = page.new_tab(login_url)
            tab.ele('xpath=//*[@id="account"]/div[3]/div[2]/div/div[1]/ul[1]/li[2]').click()
            time.sleep(0.2)
            tab.ele('xpath=//*[@id="username"]').input(phone_number)
            tab.ele('xpath=//*[@id="password"]').input('Alwayshappy3414')
            time.sleep(0.1)
            tab.ele('xpath=//*[@id="account"]/div[3]/div[2]/div/div[2]/div[1]/div[4]/a').click()
            time.sleep(0.5)
            cookie = tab.cookies()[0]
            cookie_list.append(cookie)
        print(cookie_list)



update_cookies()
