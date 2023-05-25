# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class CasaimmoPipeline:
    custom_settings = {
        'MYSQL_CONFIG': {'host': 'localhost', 'port': 3306, 'user': 'root', 'password': '', 'database': 'immobilier'}
        }
    mysql_config = custom_settings.get('MYSQL_CONFIG') 
    def process_item(self, item, spider):
       # i = item['immobilier_list']
        titres =item['titre']
        prices = item['price']
        surfaces=item['surface']
        nbpieces =item['nbpiece']
        locations=item['location']
        texts=item['text']
        villes=item['location']
        links=item['link']
        #immobiliers_list.append({'location': locations, 'titre': titres, 'surface': surfaces,'price':prices,'nbpiece':nbpieces,'text':texts,'link':links})
        list=[]
        for i in titres:
           list.append({'titre': i})
        for i in prices:
            list.append({'price': i})
        for i in surfaces:
            list.append({'surface': i}) 
        for i in nbpieces:
            list.append({'nbpiece': i})
        for i in locations:
            list.append({'location': i})
        for i in texts:
            list.append({'text': i})
        for i in villes:
            list.append({'ville': i})
        for i in links:
            list.append({'link': i})
        print(f"******************{list}*************")
       # print(item['immobiliers_list'])
      # for t,p,s,n,l,t,v,i in titres ,prices,surfaces,nbpieces,locations,texts,villes,links:
                         
        #data = (i['titre'], i['price'], i['surface'],i['nbpiece'],i['location'],i['text'],i['ville'],i['link'])
        # insert_stmt = "INSERT INTO scrapingr_annonce_copy (nom, prix, surface_total,nb_piece,ville,annonce_text,adresse,annonce_link) VALUES ("
        # list=[]
        # for i in item['list']:
        #     list.append(i)
        # print(f"**************listfin {list}")
        #data=(list[1],list[2],list[3],list[4],list[5],list[6],list[7],list[8])
        # insert_stmt =insert_stmt + "%s,%s,%s,%s,%s,%s,%s,%s)"
        # self.cursor.executemany(insert_stmt,list)
        # self.cnx.commit()
        # for i in item['list']:
        #     data=(i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8])
        #     insert_stmt =insert_stmt + "%s,%s,%s,%s,%s,%s,%s,%s)"
        #     self.cursor.executemany(insert_stmt,data)
        #     self.cnx.commit()
                
        
        return item

    def open_spider(self, spider):
        self.cnx = mysql.connector.connect(**self.mysql_config)
        self.cursor = self.cnx.cursor()
    def close_spider(self, spider):
        self.cursor.close()
        self.cnx.close()
