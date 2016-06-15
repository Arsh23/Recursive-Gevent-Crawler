from gevent import monkey
monkey.patch_all()

from lxml import html
import time
import requests
import gevent.pool
import gevent.queue
from copy import deepcopy

class HtmlItem():

    def __init__(self,id,url):
        self.id = id
        self.parent_id = 0
        self.children_id = []
        self.url = url
        self.title = ''
        self.recursion_level = 0

    def __repr__(self):
        return 'HtmlItem(id=%i, url=%s)' % (self.id, self.url)

    def __str__(self):
        return '{%i} %s' % (self.id, self.url)

class RecursiveCrawler():

    def __init__(self,start_url,domain,max_recursion_level,max_workers):
        self.unfinished_links_queue = gevent.queue.Queue()
        self.workers_pool = gevent.pool.Pool(max_workers)
        self.max_workers = max_workers
        self.domain = domain
        self.session = requests.Session()
        self.start_url = start_url
        self.pages_processed = 0
        self.requests_sent = 0
        self.err_requests = 0
        self.cached_requests = 0
        self.id_count = 0
        self.max_recursion_level = max_recursion_level
        self.items = {}
        self.dp = {}
        self.structured_urls = {}
        self.start_time = time.time()
        self.end_time = time.time()

        for x in range(self.max_recursion_level+1):
            self.structured_urls[x] = []

        self.root = HtmlItem(0,start_url)
        self.items['0'] = deepcopy(self.root)
        self.id_count += 1

    def __repr__(self):
        return 'RecursiveCrawler(start_url=%s, domain=%s, max_recursion_level=%s, max_workers=%s)' % \
        (self.start_url, self.domain,self.max_recursion_level,self.max_workers)

    def __str__(self):
        pass

    def request_html(self,url):
        print 'Request sent for - '+url
        if url not in self.dp:
            self.requests_sent +=1
            try:
                response = self.session.get(url)
            except Exception as e:
                print 'Request for '+url+' failed, will try later : ',e.errno,e.message
                self.err_requests += 1
                return None
            if response.status_code == 200:
                self.dp[url] = response.text
                return response.text
            else:
                return None
        else:
            print 'URL already stored , using cached data'
            self.cached_requests += 1
            return self.dp[url]

    def parse(self):
        tempid = self.unfinished_links_queue.get_nowait()
        yield tempid

        url = self.items[tempid].url

        html_code = self.request_html(url)
        if html_code is None:
            yield []

        tree = html.fromstring(html_code)
        try:
            title = tree.xpath('//*[@id="firstHeading"]/text()')[0]
            self.items[tempid].title = title
        except Exception as e:
            print 'Error parsing title : ',e.message
            self.err_requests += 1
            # self.unfinished_links_queue.put_nowait(tempid) #maybe unwise
            yield []

        print 'Parsed - ', title
        try:
            yield [ x.xpath('.//@href')[0] for x in tree.xpath('//*[@id="mw-content-text"]//a') ]
        except Exception as e:
            print 'Error parsing <a> tags : ',e.message

    def check_url(self,url):
        #convert this to regex
        if url[0:6] == '/wiki/' and url[-4:-3] != '.':
            return 'good'
        return 'bad'

    def add_new_links(self):
        parser = self.parse()
        pid = next(parser)

        valid_links = [ self.domain + x for x in next(parser) if self.check_url(x) == 'good' ]
        # add error handling here

        for url in valid_links:
            # add dp/repition check here
            self.pages_processed += 1

            tempitem = HtmlItem(self.id_count,url)
            tempitem.parent_id = pid
            self.items[pid].children_id.append(self.id_count)
            tempitem.recursion_level = self.items[pid].recursion_level + 1

            self.items[str(self.id_count)] = deepcopy(tempitem)

            #limit recursion
            if self.items[pid].recursion_level + 1 < self.max_recursion_level:
                self.unfinished_links_queue.put_nowait(str(self.id_count))

            self.id_count += 1


    def crawl(self):
        self.start_time = time.time()
        self.unfinished_links_queue.put_nowait('0')
        self.workers_pool.start(self.workers_pool.spawn(self.add_new_links))
        self.workers_pool.join()

        while not self.unfinished_links_queue.empty() and not self.workers_pool.full():
            for x in xrange(0, min(self.unfinished_links_queue.qsize(), self.workers_pool.free_count())):
                self.workers_pool.start(self.workers_pool.spawn(self.add_new_links))

        self.workers_pool.join()
        self.end_time = time.time()

    def stats(self):
        print 'Items Processed : ', self.pages_processed
        print 'Requests Made : ', self.requests_sent
        print 'Errored Requests Made : ', self.err_requests
        print 'Cached Requests : ', self.cached_requests
        print 'The Crawler took {0} second !'.format(self.end_time - self.start_time)

    def recursive_struct(self,tempid,rec):
        self.structured_urls[rec].append(self.items[tempid].url)
        print '   |'*rec + '---' + str(self.items[tempid])
        if self.items[tempid].children_id != []:
            [ self.recursive_struct(str(x),rec+1) for x in self.items[tempid].children_id ]
            print '   |'*rec

    def structure_urls(self):
        self.recursive_struct('0',0)
        return self.structured_urls
#
# from crawler import RecursiveCrawler
# c = RecursiveCrawler('https://en.wikipedia.org/wiki/Python_(programming_language)','https://en.wikipedia.org',1,32)
# c.crawl()
# c.stats()
