# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# 3rd party modules
import pymongo
import json
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import urllib

class ipPoolPipeline(object):
    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.db = settings['MONGODB_DB']
        self.col = settings['MONGODB_COLLECTION']
        connection = pymongo.MongoClient(self.server, self.port)
        db = connection[self.db]
        self.collection = db[self.col]
        self.url = 'https://github.com/'

    def process_item(self, item, spider):
        err_msg = ''
        for field, data in item.items():
            if not data:
                err_msg += 'Missing %s of poem from %s\n' % (field, item['url'])
        if err_msg:
            raise DropItem(err_msg)

        enabled = self.detect(item)

        exist = self.collection.find_one(dict(item))
        if exist is not None:
            if enabled:
                #drop items in db
                return item
            else:
                self.collection.delete_one(dict(item))
        if enabled:
            self.collection.insert(dict(item))
            log.msg('Item written to MongoDB database %s/%s' % (self.db, self.col),
                    level=log.DEBUG, spider=spider)
        return item

    def detect(self, proxy):
        ip = ''.join(proxy['ip'])
        port = ''.join(proxy['port'])
        try:
            proxy_host ="http://"+ip+':'+port #
            response = urllib.urlopen(self.url,proxies={"http":proxy_host})
            print response
            if response.getcode()!=200:
                print '----------- No -----------------',ip , "\n"
                return False
            else:
                print '----------- yes -----------------',response.getcode() , "\n"
                return proxy
        except Exception,e:
            print e
            return False

