# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    urll = scrapy.Field()
    create_date = scrapy.Field()
    praise_num = scrapy.Field()
    fav_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    job_market = scrapy.Field()
    genre = scrapy.Field()
