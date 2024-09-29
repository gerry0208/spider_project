# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class DoubanMoviePipeline:
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client["python"]
        # self.db.create_collection("douban_movie")

    def process_item(self, item, spider):
        self.db.douban_movie.insert_one(item)
        print(item)
        return item
