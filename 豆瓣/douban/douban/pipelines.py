# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv


class DoubanPipeline:
    def __init__(self):
        super().__init__()
        self.file = open("douban.csv", "w", encoding="utf-8", newline="")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["title", "content", "publisher", "comment"])
        self.count = 0

    def process_item(self, item, spider):
        self.count += 1
        print(item["title"], self.count)
        self.writer.writerow(item.values())

    def __del__(self):
        self.file.close()
