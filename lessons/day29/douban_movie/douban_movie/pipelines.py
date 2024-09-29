# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


# class DoubanMoviePipeline:
#     def process_item(self, item, 爬虫项目):
#         return item


class DoubanMovieImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        urls = ItemAdapter(item).get(self.images_urls_field, [])
        return [Request(u, meta={"image": item}) for u in urls]

    def file_path(self, request, response=None, info=None, *, item=None):
        item = request.meta.get("image")
        image_name = item["image_names"]
        return f"./douban_movie_covers/{image_name}.jpg"
