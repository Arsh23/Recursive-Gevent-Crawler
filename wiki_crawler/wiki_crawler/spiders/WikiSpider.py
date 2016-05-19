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

    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath('//*[@id="mw-content-text"]//a')
        link_name = sel.xpath('//*[@id="firstHeading"]/text()').extract()[0]

        if 'num' not in response.meta:
            num = 1
        else:
            num = response.meta['num']

        item = LinkItem()
        for link in links:
            next_link = link.xpath('.//@href').extract()[0]

            if next_link[0:6] == '/wiki/' and next_link[-4:-3] != '.':
                item['url'] = next_link
                item['name'] = link_name
                yield item

                request = Request('https://en.wikipedia.org' + next_link,callback=self.parse)
                request.meta['num'] = num+1

                if num < 2:
                    pass
                    yield request
