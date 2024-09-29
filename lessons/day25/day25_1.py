import requests
from jsonpath import jsonpath
import pymongo

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}

url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E8%B1%86%E7%93%A3%E9%AB%98%E5%88%86&sort=rank&page_limit=100&page_start=0'

response = requests.get(url, headers=headers)
data = response.json()

rate_list = jsonpath(data, '$..rate')
title_list = jsonpath(data, '$..title')
url_list = jsonpath(data, '$..url')
movie = []
for rate, title, url in zip(rate_list, title_list, url_list):
    movie.append({'rate': rate, 'title': title, 'url': url})

client = pymongo.MongoClient()
db = client['douban']
collection = db['movie']
collection.insert_many(movie)
