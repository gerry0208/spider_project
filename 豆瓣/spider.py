import time

from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state='state.json')
    page = context.new_page()
    page.goto('https://www.douban.com/group/721021/discussion?start=32150&type=new')
    # # 等待登录
    # while True:
    #     try:
    #         expect(page.locator('xpath=//*[@id="g-side-info-member"]/div/div/div[2]/div[1]/a')).to_be_visible()
    #         break
    #     except:
    #         time.sleep(0.1)
    # 保存登录状态
    # context.storage_state(path="state.json")


with sync_playwright() as playwright:
    run(playwright)
    time.sleep(10)