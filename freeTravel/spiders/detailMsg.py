# -*- coding: utf-8 -*-

import pymongo
import re
import scrapy
import time
from freeTravel.items import DetailMsg


class DetailmsgSpider(scrapy.Spider):
    name = 'detailMsg'
    allowed_domains = ['www.mafengwo.cn']
    # start_urls = ['http://www.mafengwo.cn/']

    def start_requests(self):
        self.client = pymongo.MongoClient(host="localhost", port=27017)
        self.db = self.client['mafengwo']
        self.collection = self.db["mafengwo"]
        requests_list = self.collection.find({},{"_id":0,"detail_link":1})
        for i in requests_list:
            yield scrapy.Request(url=i["detail_link"],callback=self.parse)

    def parse(self, response):
        result = response.text
        item = DetailMsg()
        pattern = r'class="total">[\s\S]*?span>([\s\S]*?)<[\s\S]*?dot[\s\S]*?span>([\s\S]*?)<[\S\s]*?dot[\s\S]*?span>([\s\S]*?)<[\S\s]*?出发时间：([\s\S]*?)<[\s\S]*?大约：([\s\S]*?)<[\S\s]*?目的地：([\s\S]*?)<[\s\S]*?出发地：([\s\S]*?)<[\s\S]*?希望人数：([\s\S]*?)<[\s\S]*?name[\s\S]*?>([\S\s]*?)<[\s\S]*?level[\s\S]*?>([\S\s]*?)<[\s\S]*?class="title">([\s\S]*?)</div>([\s\S]*?)</div'
        result_list = re.findall(pattern,result)
        lst = ["views","enlist","attention","departure_time","during","destination","departure_place","expected_number","initiator","level","title","plan"]
        for i in range(len(lst)):
            item[lst[i]] = result_list[0][i]
        # print(result_list)
        # print(len(result_list))
        # print(item)
        return item