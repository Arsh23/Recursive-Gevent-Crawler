from scrapy.selector import Selector
from scrapy.spiders import Spider
from wiki_crawler.items import LinkItem
from scrapy.http import Request

import json
import os

start_page = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
end_page = 'https://en.wikipedia.org/wiki/Space_exploration'


class WikiSpider(Spider):
    dp = []
    name = "WikiCrawler"
    allowed_domains = ["wikipedia.org"]
    start_urls = [start_page]
    recursions = 0
    max_recursions = 2
    pages = 0

    def closed(self, reason):
        print '--------------------------------------------------------------------------------------------------------------'
        print 'Work time:', str(self.crawler.stats.get_stats()['finish_time'] - self.crawler.stats.get_stats()['start_time'])
        print 'Items stored:', self.crawler.stats.get_stats()['item_scraped_count']
        print 'Max Recursion level:', self.recursions
        print 'Pages Scraped: ', self.pages
        print '--------------------------------------------------------------------------------------------------------------'

    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath('//*[@id="mw-content-text"]//a')
        link_name = sel.xpath('//*[@id="firstHeading"]/text()').extract()[0]
        self.pages=self.pages+1

        if 'current_level' not in response.meta:
            current_level = 0
        else:
            current_level = response.meta['current_level']

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

                if next_link in self.dp:
                    continue;

                yield item

                self.dp.append(next_link)
                request = Request('https://en.wikipedia.org' + next_link,callback=self.parse)
                request.meta['current_level'] = current_level+1
                self.recursions = max(self.recursions,current_level + 1)
                request.meta['path'] = path

                if current_level < self.max_recursions - 1:
                    yield request
