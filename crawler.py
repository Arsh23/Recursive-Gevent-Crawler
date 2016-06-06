from gevent import monkey
monkey.patch_all()

import time
import requests
import gevent.pool
import gevent.queue

from lxml import html
import gevent

startTime = time.time()



class HtmlItem():

    def __init__(self,url):
        self.url = url
        self.title = ''
        self.links = []

    def __repr__(self):
        pass

    def __str__(self):
        pass

class RecursiveCrawler():

    def __init__(self,start_url,domain,max_workers):
        self.unfinished_links_queue = gevent.queue.Queue()
        self.workers_pool = gevent.pool.Pool(max_workers)
        self.max_workers = max_workers
        self.domain = domain
        self.session = requests.Session()
        self.start_url = start_url
        self.pages_processsed = 0

        self.root = HtmlItem(start_url)
        #parse this

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def request_html(self):
        pass

    def parse(self):
        pass

    def check_url(self):
        pass

    def crawl(self):
        pass


print ('The script took {0} second !'.format(time.time() - startTime))
