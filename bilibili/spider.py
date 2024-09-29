import re
import sys
import time
import requests
from playwright.sync_api import Playwright, sync_playwright, expect
from jsonpath import jsonpath
from PySide6.QtWidgets import QMainWindow, QApplication ,QMessageBox
from PySide6.QtCore import Signal, Slot
from ui_bilibili import Ui_mainWindow


class BilibiliComment(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.url = None
        self.cookie = None
        self.comment = None
        self.ui.BTN_Send.clicked.connect(self.get_info_and_execute)

    @Slot()
    def get_info_and_execute(self):
        self.url = self.ui.EDIT_URL.toPlainText()
        if not self.url:
            QMessageBox.warning(self, "警告", "请输入url")
        self.cookie = self.ui.EDIT_Cookies.toPlainText()
        if not self.cookie:
            QMessageBox.warning(self, "警告", "请输入cookie")
        self.comment = self.ui.EDIT_Comment.toPlainText()
        if not self.comment:
            QMessageBox.warning(self, "警告", "请输入评论")
        if self.url and self.cookie and self.comment:
            self.comment.strip('\n').strip(' ')
            print(self.comment)
            try:
                self.comment_into_browser()
            except:
                QMessageBox.warning(self, "警告", "请检查url和cookie")

    def comment_into_browser(self):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=False)
            self.context = self.browser.new_context()
            self.convert_cookie(self.cookie)
            self.page = self.context.new_page()
            self.page.goto(self.url)
            self.page.locator('div.brt-editor').first.fill(self.comment)
            self.page.get_by_role("button", name="发布").click()
            self.page.on("request", self.handle_request)
            self.page.locator('button.button   ').nth(1).click()
            time.sleep(3)

    def convert_cookie(self, cookies):
        cookies = cookies.split(';')
        for cookie in cookies:
            if cookie.strip():
                key, value = cookie.strip().split('=', 1)
                self.context.add_cookies([{"name": key, "value": value, "domain": ".bilibili.com", "path": "/"}])

    def handle_request(self, request):
        pattern = r'https://api.bilibili.com/x/v2/reply/wbi/main'
        if re.findall(pattern, request.url):
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
                'accept-language': "zh-CN,zh;q=0.9",
                'cookie': self.cookie,
                'origin': "https://www.bilibili.com",
                'priority': "u=1, i",
                'referer': "https://www.bilibili.com/video/BV1qSpTeAETx/?spm_id_from=333.1007.tianma.1-2-2.click&vd_source=a2c807258efa860daa1912153cd07c70",
                'sec-ch-ua': "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
                'sec-ch-ua-mobile': "?0",
                'sec-ch-ua-platform': "\"Windows\"",
                'sec-fetch-dest': "empty",
                'sec-fetch-mode': "cors",
                'sec-fetch-site': "same-site"
            }

            response = requests.get(request.url, headers=headers)
            print(request.url)
            print(response.text)


if __name__ == "__main__":
    app = QApplication()
    window = BilibiliComment()
    window.show()
    sys.exit(app.exec())
