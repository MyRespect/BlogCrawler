# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CtiCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    publish_date = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    contents = scrapy.Field()
    url = scrapy.Field()
