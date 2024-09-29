import json
import requests

url = "https://fwjy.fszj.foshan.gov.cn/foshan/home/#/HOME_PAGE/PCT"

headers = {
    "Referer": "https://fwjy.fszj.foshan.gov.cn/foshan/home/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
}

form_data = {"pageNo": 1, "regionCode": "", "keyword": "", "orgType": "DEVELOPER"}

response = requests.post(url, headers=headers, data=form_data)

print(response.text)
