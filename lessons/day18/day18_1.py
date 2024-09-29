import json
import requests
from jsonpath import jsonpath
import execjs

song_id = input('请输入歌曲ID：')

data = {
    "rid": f"R_SO_4_{song_id}",
    "threadId": f"R_SO_4_{song_id}",
    "pageNo": "1",
    "pageSize": "20",
    "cursor": "-1",
    "offset": "0",
    "orderType": "1",
    "csrf_token": ""
}
json_data = json.dumps(data)
# 导入js代码
with open('day18_1.js', 'r') as file:
    js_text = file.read()
js_code = execjs.compile(js_text)
# 调用my_func函数，计算form_data
form_data = js_code.call('my_func', json_data)


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}
url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
# 获取网易云音乐评论数据
response = requests.post(url, headers=headers, data=form_data)
json_data = response.json()
user_names = jsonpath(json_data, '$.data.hotComments[*].user.nickname')
hot_comments = jsonpath(json_data, '$.data.hotComments[*].content')
for user_name, hot_comment in zip(user_names, hot_comments):
    print('{}:{}\n'.format(user_name, hot_comment))
