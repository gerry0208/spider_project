import requests
from jsonpath import jsonpath
import execjs

while True:

    text_to_translate = input('请输入需要翻译的文本: ')

    with open('day17_1.js', 'r') as file:
        js_code = file.read()
    js_obj = execjs.compile(js_code)
    sign = js_obj.call('func', text_to_translate)

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'cookie': 'BAIDUID_BFESS=285F0FAD358983E37D9F0E1C7C49249F:FG=1; BIDUPSID=285F0FAD358983E37D9F0E1C7C49249F; PSTM=1723206798; H_PS_PSSID=60563_60573; BA_HECTOR=2k048l8g24a0ak2g04a40k2g2tvlrd1jbc34h1v; ZFY=DLkwNANhid:B3qqynrlX60KM3IaDdxrAI2CGaCf:B29Z8:C; smallFlowVersion=old; RT="z=1&dm=baidu.com&si=d29693bd-c188-4a0c-b3bb-3e0fccb15744&ss=lzmsjqmf&sl=1&tt=15d&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1xh&ul=q54&hd=qa4"; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1723213068; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1723213068; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; ab_sr=1.0.1_MGE2MmRhNTc5NjE3ZjQwMGU4MjE0NjVhYTdhMDZiNGM0NDc1ZTRhNDkzNmI0ZTIyMzFlZjRmZDUzMDAyMWIyOWIxMWFiNjAyODg1NzBiZGMzYjE4MzIwMmQ5ZmFmNDlmOTRmM2M4ZTE2YjU4NmIzOTk1YjdhYjk0ZmFlODUzNWU1YmNmZjgzMmUzNDcyNDliNTZhNGNkOTI5NmEyZDA1MA==',
        'acs-token': '1723186829148_1723214570028_s94bY/5XaPPCoBGaKkO12sWVFKpXvXpNEMlLohGkrn5dh2EdGNSKvOt5nmnxAb90YRSFZi62EiMJKPo+Q2oGBq06pUtKaMaQWypw6AUNGl/9fjB0H2+vRvbEz7F36lLltk+K9wMrHGvzYjYonwj1dDML7Wnw/PqNgpufh+TlVXJl4ltgk/NcqQKj8xG4xw3bPj64AW2woebcVXJ55a0+StFLTmTCi2xzf60WbH66nr5A5ee33nLrjBT7ExVZ5TRIBH9Ed5X+aMkinLIg1yObYPEjxGNpsyS9M5OOhK+EDKUkjtpFtrvKyFs8YPdvV3IGrMlrOfxt85vfqvt3cEU/XlG8dYe0+yoP2dBxDQXAZcja/qnHWnk+dykCE5txpD+XJVg36VF+NCSKqEHyrhCiY2KiZwFO8W9DYngFGb8wkcNh+SweEsnZkTys8EIb0uEl'
    }

    params = {
        "from": "auto",
        "to": "auto",
        "query": text_to_translate,
        "transtype": "realtime",
        "simple_means_flag": "3",
        "sign": sign,
        "token": "b9b59f33a7757801ee7d02196072218b",
        "domain": "common",
        "ts": "1723213077317"
    }

    url = 'https://fanyi.baidu.com/v2transapi?from=zh&to=en'
    response = requests.post(url, headers=headers, params=params)
    json_data = response.json()
    translation = jsonpath(json_data, '$..trans_result.data[*].dst')[0]
    print('翻译结果：' + translation)