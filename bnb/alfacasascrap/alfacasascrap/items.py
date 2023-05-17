# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AlfacasascrapItem(scrapy.Item):
    # define the fields for your item here like:
     titre = scrapy.Field()
     price =scrapy.Field()
     surface =scrapy.Field()
     nbpiece =scrapy.Field()
     location =scrapy.Field()
     text     =scrapy.Field()
     link     =scrapy.Field()
     #list={"titre": titre , "price":price,"surface":surface,"nbpiece":nbpiece,"location":location,"text":text,"location":location,"link":link}