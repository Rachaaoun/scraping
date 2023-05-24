import scrapy
import mysql.connector
import requests
import csv
from ..settings import ITEM_PIPELINES
from ..items import TunisiaItem


class TunisiapromoSpider(scrapy.Spider):
    name = "tunisiapromo"
    allowed_domains = ["tunisiapromo.com"]
    start_urls = ['https://www.tunisiapromo.com/recherche?page={}&listing_type=4&property_type=1&region1=ANY&property_search=a&'.format(i) for  i in range(0,3524)]

    def parse(self, response):
        print("***********", response.url)
        base_url = "https://www.tunisiapromo.com/"
        list_announce = response.xpath("//*[@id='main_panel']/article/div/h2/a/@href").extract()
        for announce in list_announce:
            url_announce = base_url + announce
            #print(url_announce)
            yield scrapy.Request(url=url_announce, callback=self.details)

    custom_settings = {
        'ITEM_PIPELINES': {
            "tunisia.pipelines.TunisiaPipeline": 300,
        },
        'MYSQL_CONFIG': {'host': 'localhost', 'port': 3306, 'user': 'root', 'password': '', 'database': 'immobilier'}
      
    }

    def details(self, response):
        item = TunisiaPromoItem()
        item["link"] = response.url
        #link = response.url
        try:
            item["titre"] = response.xpath('//header[@class="item_title"]/h1/text()').extract_first()
        except:
            pass
        try:
            item["location"] = response.xpath('//*[@id="tab-1"]/div[4]/text()').extract()[1].strip()
        except:
            pass
        try:
            item["text"] = response.xpath('//*[@id="tab-1"]/div[4]/p/text()[1]').extract_first().strip()
        except:
            pass
        try:
            item["surface"]= response.xpath('//*[@id="tab-1"]/div[5]/div[1]/span[10]/text()').extract_first().split(" ")[0]
        except:
            pass
        
        try:
            item["nbpiece"]= response.xpath('//*[@id="tab-1"]/div[5]/div[1]/span[2]/text()').extract_first()
        except:
            pass
        try:
            item["price"]= response.xpath('//span[@class="leftColumn"]/span/span[@class="property_price"]/text()').extract_first().strip().replace("DT","").replace(" ","")
        except:
            pass
        
        yield item
        connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="immobilier",
                port=3306
                
                )
        cursor = connection.cursor()

        insert_stmt = "INSERT INTO scrapingr_annonce (nom, prix, surface_total,nb_piece,ville,annonce_text,adresse,annonce_link) VALUES ("
            insert_stmt =insert_stmt + "%s,%s,%s,%s,%s,%s,%s,%s)"
        for i in range(1,10):    
            scrapped_data = (item["titre"],item["price"],item["surface"],item["nbpiece"],item["location"],item["text"],item["location"],item["link"])
            cursor.execute(insert_stmt, scrapped_data)
        #for row in scrapped_data:
         #   cursor.execute(insert_stmt, row)

        # Commit the changes to the database
        connection.commit()

        cursor.close()
        connection.close()

