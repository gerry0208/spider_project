# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DoubanMoviePipeline:
    def __init__(self):
        self.file = open("douban_movie.csv", "w", encoding="utf-8", newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['电影名称', '评分'])

    def process_item(self, item, spider):
        print(item)
        self.writer.writerow(item.values())
        return item

    def __del__(self):
        self.file.close()
