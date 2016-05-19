from scrapy.selector import Selector
from scrapy.spider import Spider
from wiki_crawler.items import LinkItem
from scrapy.http import Request

import json
import os

start_page = 'https://en.wikipedia.org/wiki/Python_(programming_language)'

class WikiSpider(Spider):
    name = "WikiCrawler"
    allowed_domains = ["wikipedia.org"]
    start_urls = [start_page]

    def closed(self, reason):
        print '--------------------------------------------------------------------------------------------------------------'
        print 'Work time:', str(self.crawler.stats.get_stats()['finish_time'] - self.crawler.stats.get_stats()['start_time'])
        print 'Items stored : ', self.crawler.stats.get_stats()['item_scraped_count']
        print '--------------------------------------------------------------------------------------------------------------'

    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath('//*[@id="mw-content-text"]//a')
        link_name = sel.xpath('//*[@id="firstHeading"]/text()').extract()[0]

        if 'num' not in response.meta:
            num = 1
        else:
            num = response.meta['num']

        if 'path' not in response.meta:
            path = link_name
        else:
            path = response.meta['path'] + ' >> ' + link_name

        item = LinkItem()
        for link in links:
            next_link = link.xpath('.//@href').extract()[0]

            if next_link[0:6] == '/wiki/' and next_link[-4:-3] != '.':
                item['url'] = next_link
                item['name'] = link_name
                item['path'] = path
                yield item

                request = Request('https://en.wikipedia.org' + next_link,callback=self.parse)
                request.meta['num'] = num+1
                request.meta['path'] = path

                if num < 2:
                    # pass
                    yield request
