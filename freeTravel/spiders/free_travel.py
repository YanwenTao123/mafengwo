# -*- coding: utf-8 -*-
import logging
import re
import scrapy
import json
from freeTravel.items import FreetravelItem

class FreeTravelSpider(scrapy.Spider):
    name = 'free_travel'
    allowed_domains = ['www.mafengwo.cn']
    # allowed_domains = ['httpbin.org']
    # 目的地
    mddid = 0
    # 时间段
    timeFlag = 1
    # 最新发表/即将出发
    flag = 3

    def start_requests(self):
        for i in range(10):
            offset = str(i)
            base_url = 'http://www.mafengwo.cn/together/travel/more?flag='+str(self.flag)+'&offset=' + offset + '&mddid='+ str(self.mddid) +'&timeFlag='+str(self.timeFlag)+'&timestart='
            yield scrapy.Request(url=base_url,callback=self.parse)

    def parse(self, response):
        # print(response.text)
        item = FreetravelItem()
        try:
            response = eval("u"+"\'"+response.text +"\'")
            pattern = re.compile('li class="item">[\s\S]*?a href="([\s\S]*?)"[\s\S]*?<h3 class="title">([\s\S]*?)<[\s\S]*?class="desc">([\s\S]*?)<[\s\S]*?<i .*?="([\s\S]*?)"[\S\s]*?class="name">([\s\S]*?)<[\S\s]*?class="level">([\s\S]*?)<[\S\s]*?<b>(.*?)<')
            result = re.findall(pattern,response)
            l_item = ['detail_link',"city",'desc','gender','initiator','level','attention']
            for i in result:
                for j in range(len(l_item)):
                    item[l_item[j]] = i[j]
                # print(item)
                yield item
        except Exception as e:
            logging.basicConfig(filename=r'G:\scrapy_execise\freeTravel\freeTravel\log.txt')
            logging.error(e)
            logging.warning(e)
            logging.critical(e)



