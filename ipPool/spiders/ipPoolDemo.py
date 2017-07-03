# -*- Coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from ipPool.items import ipPoolItem

class ipPoolDemo(scrapy.Spider):
    name = 'ipPool'
    allowed_domains = 'www.xicidaili.com'
    start_urls = ['http://www.xicidaili.com/']
    def parse(self, response):
        sel = Selector(response)
        ips = sel.xpath('//table[@id="ip_list"]/tr')
        for ip in ips:
            item = ipPoolItem()
            item['ip'] = ip.xpath('.//td[2]').xpath('text()').extract()
            item['port'] = ip.xpath('.//td[3]').xpath('text()').extract()
            print item
            yield item
