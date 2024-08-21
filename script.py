from selenium.webdriver.chrome.options import Options

options = Options()
# 设置自动化特性的关闭，防止被服务器检测到是由selenium驱动的
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument('--disable-blink-features=AutomationControlled')
# 关闭证书报错
options.add_argument('ignore-certificate-errors')
