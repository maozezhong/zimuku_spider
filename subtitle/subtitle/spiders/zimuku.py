# -*- coding: utf-8 -*-
import scrapy
import re

from subtitle.items import SubtitleItem


class ZimukuSpider(scrapy.Spider):
    name = 'zimuku'
    allowed_domains = ['zimuku.cn']
    start_urls = ["http://www.zimuku.cn/newsubs?t=tv&ad=1&p=1",
            "http://www.zimuku.cn/newsubs?t=tv&ad=1&p=2"]
    detail_re = re.compile('^http://www.zimuku.cn/detail/\d+.html$')

    # def parse(self, response):
    #     hrefs = response.selector.xpath('//div[contains(@class, "persub")]/h1/a/@href').extract()
    #     for href in hrefs:
    #         url = response.urljoin(href)
    #         request = scrapy.Request(url, callback=self.parse_detail)
    #         yield request

    def parse(self, response):
        for url in response.selector.xpath('//a/@href').extract():
            if not url.startswith('http'):
                url = response.urljoin(url)
            isDetail=self.detail_re.match(url)
            if isDetail:
                yield scrapy.Request(url, callback=self.parse_detail)
            else:
                yield scrapy.Request(url, callback=self.parse)

    def parse_detail(self, response):
        url = response.selector.xpath('//li[contains(@class, "dlsub")]/div/a/@href').extract()[0]
        if not url.startswith('http'):
            url = response.urljoin(url)
        # f_name=response.selector.xpath('/html/body/div[2]/div/div[1]/div/div[1]/h1').extract()[0]
        print ("processing: ", url)
        request = scrapy.Request(url, callback=self.parse_file)
        yield request

    def parse_file(self, response):
        body = response.body
        item = SubtitleItem()
        item['url'] = response.url
        f = re.findall(r'attachment; filename="(.*)"', response.headers.get('Content-Disposition', '').decode('utf-8'))
        item['filename'] = f[0] if len(f) else ''
        item['body'] = body
        return item
