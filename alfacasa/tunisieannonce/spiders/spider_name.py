import scrapy
import mysql.connector
from ..items import TunisieannonceItem

class SpiderNameSpider(scrapy.Spider):
    
    name = "tunisieannoncee"
    allowed_domains = ["alfacasaimmobiliere.com"]
    start_urls = [
        "https://alfacasaimmobiliere.com/biens/page/1" ,
        "https://alfacasaimmobiliere.com/biens/page/2" ,
        "https://alfacasaimmobiliere.com/biens/page/3" ,
        "https://alfacasaimmobiliere.com/biens/page/4" ,
        "https://alfacasaimmobiliere.com/biens/page/5" ,
        "https://alfacasaimmobiliere.com/biens/page/6" ,
        "https://alfacasaimmobiliere.com/biens/page/7" ,
        "https://alfacasaimmobiliere.com/biens/page/8" ,
        "https://alfacasaimmobiliere.com/biens/page/9" ,
        ]
    # for i in range(1,19):
    #     start_urls.append(f"https://alfacasaimmobiliere.com/biens/page/{i}/")

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse)


    custom_settings = {
        'ITEM_PIPELINES': {
            'tunisieannonce.pipelines.AlfacasascrapPipeline': 300,
        },
        'MYSQL_CONFIG': {'host': 'localhost', 'port': 3306, 'user': 'root', 'password': '', 'database': 'immobilier'}
      
    }
       

    def parse(self, response):
        item = TunisieannonceItem()
        titres=[]
        surfaces=[]
        prices=[]
        nbpieces=[]

        connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="immobilier",
                port=3306
                
                )
        for url in self.start_urls:
            for products in response.css('div.g5ere__property-item-inner'):
                print("**********************************",products)
                item = TunisieannonceItem()
                cursor = connection.cursor()
                try:
                    item['titre']= products.css("h3.g5ere__loop-property-title a::text").get()
                    # print("**********************************",item['titre'])
                except:
                    pass
                try:
                    item['link'] =products.css('h3.g5ere__loop-property-title a::text').get()
                except:
                    pass
                try :
                    item['surface'] = products.css("span.g5ere__loop-property-size::text").get() 
                except:
                    pass
                try:           
                    item['price']=products.css("span.g5ere__lpp-price::text").get()
                except:
                    pass
                try : 
                    item['nbpiece'] = products.css("span.g5ere__property-bedrooms::text").get()
                    
                except:
                    pass
                # for t in item['titre'] :
                #     item['titre']=t.strip()

                #     #     titres.append(titre)
                #     #     #immobiliers_list.append({'titre': titre})
                # for s in item['surface']:
                #     item['surface']=s.strip()
                #     #     surfaces.append(surface)
                #     #     #immobiliers_list.append({'surface': surface})
                # for p in item['price']:
                #     item['price']=p.strip()
                #     #     prices.append(price)
                #     #     #immobiliers_list.append({'price': price})
                # for n in item['nbpiece']:
                #     item['nbpiece']=n.strip()
                # for l in item['link']:
                #     item['link']=n.strip()
                #     #     nbpieces.append(nbpiece)
                #         #immobiliers_list.append({'nbpiece': nbpiece})
                # # yield {
                # #      'titre': item['titre'],
                # #      'price' : item['price'],
                # #      'surface' : item['surface'],
                # #      'nbpiece' :item['nbpiece'],
                # # }
                yield item

                
                insert_stmt = "INSERT INTO scrapingr_annonce (annonce_text,annonce_link,nom, prix, surface_total,nb_piece) VALUES ("
                insert_stmt =insert_stmt + "%s,%s,%s,%s,%s,%s)"
                print("***********************************************",insert_stmt)
                    
                scrapped_data = (item["titre"],item["link"],item["titre"],item["price"],item["surface"],item["nbpiece"])
                cursor.execute(insert_stmt, scrapped_data)
                #for row in scrapped_data:
                #   cursor.execute(insert_stmt, row)

                # Commit the changes to the database
                connection.commit()
                #scrapped_data =[]
            #scrapped_data=(item['titre'],item['price'],item['surface'],item['nbpiece'])
            # insert_stmt = "INSERT INTO scrapingr_annonce_copy (nom, prix, surface_total,nb_piece) VALUES ("
            # insert_stmt =insert_stmt + "%s,%s,%s,%s,%s,%s,%s,%s)"

            # for i in range(1,10):
            #     scrapped_data = (item['titre'],item['price'],item['surface'],item['nbpiece'])
            #     cursor.execute(insert_stmt, scrapped_data)
            # for row in scrapped_data:
            #     cursor.execute(insert_stmt, row)

            # Commit the changes to the database
            # connection.commit()

            # cursor.close()
            # connection.close()









            # data=zip(titres,prices,surfaces,nbpieces,locations,texts,locations,links)
            # insert_stmt = "INSERT INTO scrapingr_annonce_copy (nom, prix, surface_total,nb_piece,ville,annonce_text,adresse,annonce_link) VALUES ("
            # insert_stmt =insert_stmt + "%s,%s,%s,%s,%s,%s,%s,%s)"
            # for row in data:
            #     cursor.execute(insert_stmt, row)
            # connection.commit()
            yield response.follow(url , callback=self.parse)
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
    
