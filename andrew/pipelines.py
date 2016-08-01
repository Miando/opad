# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline,FilesPipeline
from PIL import Image
class AndrewPipeline(ImagesPipeline):
    '''
    def set_filename(self, key, response):
        if response.meta['x']==1:
            return "full/Schematics/%s.jpg" % (response.meta['title'])
        elif response.meta['x']==0:
            return "full/Product Images/%s.jpg" % (response.meta['title'])
        else:
            return "full/Product Images/%s-image%s.jpg" % (response.meta['title'],response.meta['x']-1)



    def get_media_requests(self, item, info):
        x=0
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'title': item['title'],'x': x})
            x=x+1

    def get_images(self, response, request, info):
        for key, image, buf in super(AndrewPipeline, self).get_images(response, request, info):
            key = self.set_filename(key, response)
            yield key, image, buf
    '''
class AndrewPipeline2(FilesPipeline):
    '''
    def file_path(self, request, response=None, info=None):
        #item=request.meta['item'] # Like this you can use all from item, not just url.
        image_guid = request.url.split('/')[-1]
        return 'full/PDF/%s' % (image_guid)

    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url, meta={'title': item['title']})
    '''
