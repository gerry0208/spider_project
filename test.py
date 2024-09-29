import requests

url = "https://kjt.hebei.gov.cn/www/xxgk2020/228104/228108/228109/2000eff1-3.html"

headers = {
  'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
  'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
  'referer': "https://kjt.hebei.gov.cn/www/xxgk2020/228104/228108/228109/2000eff1-3.html"
}

response = requests.get(url, headers=headers)

print(response.text)