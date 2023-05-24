# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TunisieannonceItem(scrapy.Item):
     titre = scrapy.Field()
     price =scrapy.Field()
     surface =scrapy.Field()
     nbpiece =scrapy.Field()
     link =scrapy.Field()
