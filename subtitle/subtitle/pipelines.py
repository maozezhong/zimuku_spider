# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

class SubtitlePipeline(object):
    def process_item(self, item, spider):
        url = item['url']
        fold_name = './result'
        if not os.path.exists(fold_name):
            os.mkdir(fold_name)
        file_name_download = fold_name+'/'+item['filename']+'.download'
        file_name = fold_name+'/'+item['filename']
        if os.path.exists(file_name):
            return item
        with open(file_name_download, 'wb') as f:
            f.write(item['body'])
        os.rename(file_name_download,file_name)
        return item
