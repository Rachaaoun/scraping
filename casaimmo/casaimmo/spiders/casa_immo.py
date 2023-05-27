import scrapy
import mysql.connector
import requests
import csv
from ..settings import ITEM_PIPELINES
from ..items import CasaimmoItem

class CasaImmoSpider(scrapy.Spider):
    name = "casa_immo"
    allowed_domains = ["casaimmo.com"]
    start_urls = ["https://www.casaimmo.tn/acheter/index/"]
    for i in range(1,15):
        start_urls.append(f"https://www.casaimmo.tn/acheter/index/{i}/")

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)



    custom_settings = {
        'ITEM_PIPELINES': {
            "casaimmo.pipelines.CasaimmoPipeline": 300,
        },
        'MYSQL_CONFIG': {'host': 'localhost', 'port': 3306, 'user': 'root', 'password': '', 'database': 'immobilier'}
      
    }

    def parse(self, response):

    
            for products in response.xpath("//div[@class='col-md-4 col-sm-4 col-xs-12']").extract():
            #for i in range(1,10):
                #print("**********************************",products)
                item = CasaimmoItem()
                link = response.xpath('//div[@class="image"]/a/@href').extract()
                titre = response.xpath('//div[@class="proerty_content"]/div[@class="proerty_text"]/h5/@title').extract()
                price = response.xpath('//div[@class="favroute clearfix"]/p[@class="pull-left"]/strong/text()').extract()
                surface= response.xpath('//div[@class="property-detail"]/span[1]/text()').extract()
                nbpiece= response.xpath('//div[@class="property-detail"]/span[2]/text()').extract()
                location = response.xpath('//span[@class="bottom10"]/text()').extract()
                item["text"]=""
                for i in link:
                    item['link']=i.strip()
                for i in titre:
                    item['titre']=i.strip()
                for i in price:    
                    item['price']=i.strip()
                for i in surface:    
                    item["surface"]=i.strip()
                for i in nbpiece:    
                    item["nbpiece"]=i.strip()
                for i in location:
                    item["location"]=i.strip()
                
                
                
                
                yield item

                insert_stmt = "INSERT INTO scrapingr_annonce (nom, prix, surface_total,nb_piece,ville,annonce_text,adresse,annonce_link) VALUES ("
                insert_stmt =insert_stmt + "%s,%s,%s,%s,%s,%s,%s,%s)"
                print("***********************************************",insert_stmt)
                links=[]
                titres=[]
                prices=[]
                surfaces=[]
                nbpieces=[]
                locations=[]
                texts=[]
                links.append(item["link"])
                titres.append(item["titre"])
                prices.append(item["price"])
                surfaces.append(item["surface"])
                nbpieces.append(item["nbpiece"])
                locations.append(item["location"])
                texts.append(item["text"])
                
                connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="immobilier",
                port=3306
                
                )
                cursor = connection.cursor()
                
            for i in range(1,10):
                #scrapped_data = (titres[i],prices[i],surfaces[i],nbpieces[i],locations[i],texts[i],locations[i],links[i])
                scrapped_data = (item['titre'],item['price'],item['surface'],item['nbpiece'],item['location'],item['text'],item['location'],item['link'])
                cursor.execute(insert_stmt, scrapped_data)

            connection.commit()

            cursor.close()
            connection.close()

            #yield response.follow(url , callback=self.parse)


    def open_spider(self, spider):
        self.cnx = mysql.connector.connect(**self.mysql_config)
        self.cursor = self.cnx.cursor()
    def close_spider(self, spider):
        self.cursor.close()
        self.cnx.close()