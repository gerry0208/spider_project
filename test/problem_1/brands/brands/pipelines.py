# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BrandsPipeline:
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client['赢商大数据']
        try:
            self.db.create_collection('brands')
        except:
            print('集合已存在')

    def process_item(self, item, spider):
        self.db.brands.insert_one(item)
        print(item)
        return item
