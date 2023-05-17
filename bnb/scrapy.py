import scrapy
import requests
import mysql.connector
import csv
from scrapy.exceptions import DropItem


class ScrapySpider(scrapy.Spider):
    name = "scrapy"
    allowed_domains = ["mubawab.tn"]
    start_urls = ["https://mubawab.tn"]
    immobiliers = []
    titre =''
    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', password='',
                                            host='localhost',
                                            database='scraping_project')
        self.cursor = self.cnx.cursor()
    def close_spider(self, spider):
        self.cursor.close()
        self.cnx.close()
    def process_item(self, item, spider):
        # Insert the item into the MySQL database
        try:
            self.cursor.execute("""
                INSERT INTO immobilier (type, titre, prix,ville)
                VALUES (%s, %s, %s,%s)
            """, (item['type'], item['titre'], item['prix'], item['ville']))
            self.cnx.commit()
        except mysql.connector.Error as err:
            raise DropItem("MySQL Error: {}".format(err))

        return item
    def getImmobilier(response):
        immobiliers = []
        titre =response.css('h2.listingTit::text').getall().getall().text.strip()
        immobiliers.append({ 'titre': titre })

    
    
    def parse(self, response,immobiliers):
        for immobilier in immobiliers:
            insert_query = "INSERT INTO immobilier (null, titre, null,null) VALUES (%s, %s, %s,%s)"
            data = (immobilier['type'], immobilier['titre'], immobilier['prix'], immobilier['ville'])
            self.cursor.execute(insert_query, data)
            self.cnx.commit()
