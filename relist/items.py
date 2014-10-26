# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class Property(Item):
    url = Field()
    cost = Field()
    size = Field()
    postcode = Field()
    description = Field()
    
    @property
    def ppsqm(self):
    	'''Price per square meter'''
        return float(self.cost) / self.size
