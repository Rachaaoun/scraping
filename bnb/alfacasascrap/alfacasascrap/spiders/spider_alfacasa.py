import scrapy
import mysql.connector
import requests
import csv
from ..settings import ITEM_PIPELINES
from ..items import AlfacasascrapItem
from alfacasascrap.pipelines import AlfacasascrapPipeline

class SpiderAlfacasaSpider(scrapy.Spider):
    name = "alfacasaimmobiliere"
    allowed_domains = ["bnb.tn"]
    start_urls = ["https://www.bnb.tn/properties/"]
    for i in range(1,824):
        start_urls.append(f"https://www.bnb.tn/properties/page/{i}/")

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)


    custom_settings = {
        'ITEM_PIPELINES': {
            'alfacasascrap.pipelines.AlfacasascrapPipeline': 300,
        },
        'MYSQL_CONFIG': {'host': 'localhost', 'port': 3306, 'user': 'root', 'password': '', 'database': 'immobilier'}
      
    }
       

    def parse(self, response):
        immobiliers_list=[]
        page_immobilier = response.css('#main div').getall()
        print(f"^^^^^^^^^^^^^^^^^^^^{len(page_immobilier)}")
        titres=[]
        locations=[]
        surfaces=[]
        prices=[]
        nbpieces=[]
        texts=[]
        links=[]
        list=[]
        connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="immobilier",
                port=3306
                
                )
        cursor = connection.cursor()
        details=[]
        for i in range (1,10):
            location = response.css('div.property-row-location::text').getall()
            titre = response.css('.property-row-title  a::text').getall()
            surface = response.css('div.property-row-meta div.field-item:nth-child(3)::text').getall()            
            price=response.css('.property-row-price::text').getall()
            nbpiece = response.css('div.property-row-meta div.field-item:nth-child(1)::text').getall()
            text =response.css('p.justify::text').getall()
            link =response.css('div.read-more-wrapper a::attr(href)').getall()
            
            for l in location:
                location = l.strip()
                locations.append(location)
                #immobiliers_list.append({'location': location})
            for t in titre :
                titre=t.strip()
                titres.append(titre)
                #immobiliers_list.append({'titre': titre})
            for s in surface:
                surface=s.strip()
                surfaces.append(surface)
                #immobiliers_list.append({'surface': surface})
            for p in price:
                price=p.strip()
                prices.append(price)
                #immobiliers_list.append({'price': price})
            for n in nbpiece:
                nbpiece=n.strip()
                nbpieces.append(nbpiece)
                #immobiliers_list.append({'nbpiece': nbpiece})
            for te in text:
                text=te.strip()
                texts.append(text)
                #immobiliers_list.append({'text': text})
            for li in link:
                link=li.strip()
                links.append(link)
                #immobiliers_list.append({'link': link})
            yield {
             'titre': titre,
             'price' :price,
             'surface' : surface,
             'nbpiece' :nbpiece,
             'location' :location,
             'text' :text,
             'link' :link
        }
 
            insert_stmt = "INSERT INTO scrapingr_annonce (nom, prix, surface_total,nb_piece,ville,annonce_text,adresse,annonce_link) VALUES ("
            insert_stmt =insert_stmt + "%s,%s,%s,%s,%s,%s,%s,%s)"
        for i in range(1,10):    
            scrapped_data = (titres[i],prices[i],surfaces[i],nbpieces[i],locations[i],texts[i],locations[i],links[i])
            cursor.execute(insert_stmt, scrapped_data)
        #for row in scrapped_data:
         #   cursor.execute(insert_stmt, row)

        # Commit the changes to the database
        connection.commit()

        cursor.close()
        connection.close()









            # data=zip(titres,prices,surfaces,nbpieces,locations,texts,locations,links)
            # insert_stmt = "INSERT INTO scrapingr_annonce_copy (nom, prix, surface_total,nb_piece,ville,annonce_text,adresse,annonce_link) VALUES ("
            # insert_stmt =insert_stmt + "%s,%s,%s,%s,%s,%s,%s,%s)"
            # for row in data:
            #     cursor.execute(insert_stmt, row)
            # connection.commit()

        # cursor.close()
        # connection.close()
        #immobiliers_list.append({'location': locations, 'titre': titres, 'surface': surfaces,'price':prices,'nbpiece':nbpieces,'text':texts,'link':links})
        #print(f"******************{len(immobiliers_list)}*************")  
        #print(f"********************{links}")

        
    def open_spider(self, spider):
        self.cnx = mysql.connector.connect(**self.mysql_config)
        self.cursor = self.cnx.cursor()
    def close_spider(self, spider):
        self.cursor.close()
        self.cnx.close()   

        #page_immobilier = response.css('#main-content div').getall()
        # titres =[] 
        # prix=[]
        # villes=[]
        # for i in range(1, 100):
        #     titre = response.css('.property-row-title  a::text').getall()
        #     prix = response.css('.property-row-price div').getall()
        #     ville = response.css('div.property-row-subtitle  div.property-row-location').getall()
            

        #     #response.css('.content h3 a::text').getall(): 
        #     titres.append(titre)
        #     prix.append(prix)
        #     villes.append(ville)

            #item = AlfacasascrapItem()
            #item['title'] = page_immobilier.strip()              

            # with open('annonces.csv', 'w', newline='') as file:
            #     rows =titres
    # Create a CSV writer
                # writer = csv.writer(file)
                # # Write headers
                # writer.writerow([ i[0] for i in titres])
                # writer.writerow([ i[0] for i in ville])
                # #writer.writerow([[ i[0] for i in titres],[ i[1] for i in prix], [i[2] for i in ville ]])
                # # Write rows
                # writer.writerows(rows)
    