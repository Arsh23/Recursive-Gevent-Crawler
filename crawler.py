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
        self.unfinished_links_queue.put_nowait(self.root)
        greenlet_thread = self.workers_pool.spawn(self.add_new_links)
        self.workers_pool.start(greenlet_thread)
        self.workers_pool.join()

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def request_html(self):
        tempitem = self.unfinished_links_queue.get_nowait()
        url = tempitem.url
        print 'Request sent for - ',url

        try:
            response = self.session.get(url)
        except Exception as e:
            print 'Request for '+url+' failed, will try later'
            self.unfinished_links_queue.put_nowait(tempitem)
            return None

        if response.status_code == 200:
            return response.text
        else:
            return None

    def parse(self,html_code):
        tree = html.fromstring(html_code)
        try:
            title = tree.xpath('//*[@id="firstHeading"]/text()')[0]
        except Exception as e:
            print 'Error parsing'
            return []


        links = tree.xpath('//*[@id="mw-content-text"]//a')

        next_links = []
        for link in links:
            try:
                next_links.append(link.xpath('.//@href')[0])
            except Exception as e:
                pass # add something here


        print 'Parsed - ', title
        self.pages_processsed += 1

        return next_links

    def check_url(self,url):
        if url[0:6] == '/wiki/' and url[-4:-3] != '.':
            return 'good'
        return 'bad'

    def add_new_links(self):
        valid_links = [ self.domain + url for url in self.parse(self.request_html()) if self.check_url(url) == 'good' ]
        for link in valid_links:
            tempitem = HtmlItem(link)
            self.unfinished_links_queue.put_nowait(tempitem)

    def crawl(self):
        while not self.unfinished_links_queue.empty() and not self.workers_pool.full():
            for x in xrange(0, min(self.unfinished_links_queue.qsize(), self.workers_pool.free_count())):
                greenlet_thread = self.workers_pool.spawn(self.add_new_links)
                self.workers_pool.start(greenlet_thread)
                # print 'queue',q.qsize(),'pool',p.free_count()

        self.workers_pool.join()


c = RecursiveCrawler('https://en.wikipedia.org/wiki/Python_(programming_language)','https://en.wikipedia.org',32)
c.crawl()


print ('The script took {0} second !'.format(time.time() - startTime))
