# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FreetravelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    detail_link = scrapy.Field()
    city = scrapy.Field()
    initiator = scrapy.Field()
    desc = scrapy.Field()
    level = scrapy.Field()
    attention = scrapy.Field()
    gender = scrapy.Field()

class DetailMsg(scrapy.Item):
    views = scrapy.Field()
    enlist = scrapy.Field()
    attention = scrapy.Field()
    departure_time = scrapy.Field()
    during = scrapy.Field()
    destination = scrapy.Field()
    departure_place = scrapy.Field()
    expected_number = scrapy.Field()
    initiator = scrapy.Field()
    level = scrapy.Field()
    title = scrapy.Field()
    plan = scrapy.Field()


