# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class Property(Item):
    url = Field()
    price = Field()
    size = Field()
    ppsqm = Field()
    postcode = Field()
    title = Field()
    description = Field()
