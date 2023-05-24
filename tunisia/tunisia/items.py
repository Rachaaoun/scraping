# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TunisiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    titre = scrapy.Field()
    price = scrapy.Field()
    surface =  scrapy.Field()
    nbpiece = scrapy.Field()
    location = scrapy.Field()
    text     = scrapy.Field()
    link     = scrapy.Field()
