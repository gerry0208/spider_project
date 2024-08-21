import requests
from jsonpath import jsonpath

url = "https://api.dcarapi.com/motor/car_page/v6/rank_data"

params = {
    '__method': "window.fetch",
    'rank_data_type': "53",
    'energy_type': "",
    'price': "0,-1",
    'market_time': "0",
    'score_type': "configuration",
    'need_recommend': "1",
    'series_id': "",
    'offset': "0",
    'count': "50",
    'scm_version': "1.0.0.1903"
}

headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 12; M2102K1AC Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/95.0.4638.74 Safari/537.36 MMWEBID/1017 MicroMessenger/8.0.50.2701(0x28003257) WeChat/arm64 Weixin Android Tablet NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wx0688e7bcdd17106e",
    'Accept-Encoding': "gzip, deflate",
    'content-type': "application/x-www-form-urlencoded",
    'x-requested-with': "com.tencent.mm",
    'sec-fetch-site': "same-origin",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://api.dcarapi.com/motor/feoffline/autorank/next.html?micro_first_page=&tab=1&link_source=microapp&microapp_immersion=1&status_bar_height=0&hide_bar=0&hide_status_bar=0",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}

response = requests.get(url, params=params, headers=headers)

data = jsonpath(response.json(), '$.data.list')[0]
for item in data:
    print(jsonpath(item, '$.brand_name')[0])
    print(jsonpath(item, '$.series_name')[0])
    print('评分：', jsonpath(item, '$.score')[0])
    print('-----------------------------------------')