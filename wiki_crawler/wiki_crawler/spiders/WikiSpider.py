from scrapy.selector import Selector
from scrapy.spider import Spider
from wiki_crawler.items import LinkItem

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

        item = LinkItem()
        for link in links:

            next_link = link.xpath('.//@href').extract()[0]

            if next_link[0:6] == '/wiki/' and next_link[-4:-3] != '.':
                item['name'] = next_link
                yield item
