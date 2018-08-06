# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from urllib.parse import urljoin

import datetime
import pymongo
import re

from freeTravel.items import FreetravelItem
from freeTravel.items import DetailMsg

class DataClear(object):
    def process_item(self,item,spider):
        if isinstance(item,FreetravelItem):
            # item = dict(item)
            if item["gender"] == "female":
                item["gender"] = "0"
            else:
                item["gender"] = "1"
            item["level"] = item['level'][3:]
            item["attention"] = int(item['attention'])
            item["detail_link"] = urljoin("http://www.mafengwo.cn",re.sub(r"\\",'',item["detail_link"]))
            if "|" in item["city"]:
               item['city'] = item['city'].split("|")
        elif isinstance(item,DetailMsg):
            item["during"] = item["during"][:-1]
            item["expected_number"] = item["expected_number"][:-1]
            item["level"] = item["level"][3:]
            item["departure_time"] = datetime.datetime.strptime(item["departure_time"],'%Y-%m-%d')
            item["plan"] = re.sub(r"<[\s\S]*?>","",re.sub('\s',"",item["plan"]))
        return item

class FreetravelPipeline(object):
    def __init__(self,host,port,mongodb,collection):
        self.host = host
        self.db = mongodb
        self.collection = collection
        self.port = port

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host = crawler.settings.get("HOST"),
            port = crawler.settings.get("PORT"),
            mongodb = crawler.settings.get("MONGODB"),
            collection = crawler.settings.get("COLLECTION")
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(host=self.host,port=self.port)
        self.db = self.client[self.db]
        self.collection = self.db[self.collection]

    def process_item(self, item, spider):
        if isinstance(item,FreetravelItem):
            if isinstance(item['city'],list):
                # print(item['city'])
                # print(type(item['city']))
                lst = item["city"]
                for i in range(len(item['city'])):
                    # print((item['city'],item['city'][i]))
                    item['city'] = lst[i]
                    try:
                        self.collection.insert(dict(item))
                    except Exception as e:
                        logging.basicConfig(filename=r'G:\scrapy_execise\freeTravel\freeTravel\log.txt')
                        logging.error(e)
                        logging.warning(e)
                        logging.critical(e)
            else:
                try:
                    self.collection.insert(dict(item))
                except Exception as e:
                    logging.basicConfig(filename=r'G:\scrapy_execise\freeTravel\freeTravel\log.txt')
                    logging.error(e)
                    logging.warning(e)
                    logging.critical(e)
        return item

    def close_spider(self,spider):
        self.client.close()

class DetailMsgPipeline(object):
    def __init__(self,host,port,mongodb,collection):
        self.host = host
        self.db = mongodb
        self.collection = collection
        self.port = port

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host = crawler.settings.get("HOST"),
            port = crawler.settings.get("PORT"),
            mongodb = crawler.settings.get("MONGODB"),
            collection = crawler.settings.get("DETAIL_COLLECTION")
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(host=self.host,port=self.port)
        self.db = self.client[self.db]
        self.collection = self.db[self.collection]

    def process_item(self, item, spider):
        if isinstance(item,DetailMsg):
            try:
                self.collection.insert(dict(item))
            except Exception as e:
                logging.basicConfig(filename=r'G:\scrapy_execise\freeTravel\freeTravel\log.txt')
                logging.error(e)
                logging.warning(e)
                logging.critical(e)
        return item

    def close_spider(self,spider):
        self.client.close()
