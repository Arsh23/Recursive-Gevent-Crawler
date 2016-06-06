from gevent import monkey
monkey.patch_all()

from lxml import html
import time
import requests
import gevent.pool
import gevent.queue

startTime = time.time()

class HtmlItem():

    def __init__(self,id,url):
        self.id = id
        self.parent_id = 0
        self.url = url
        self.title = ''
        self.recursion_level = 0

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
        self.requests_sent = 0
        self.id_count = 0
        self.max_recursion_level = 2
        # add dict to store values

        self.root = HtmlItem(0,start_url)
        self.unfinished_links_queue.put_nowait(self.root)
        greenlet_thread = self.workers_pool.spawn(self.add_new_links)
        self.id_count += 1
        self.workers_pool.start(greenlet_thread)
        self.workers_pool.join()

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def request_html(self,url):
        print 'Request sent for - '+url
        self.requests_sent +=1
        try:
            response = self.session.get(url)
        except Exception as e:
            print 'Request for '+url+' failed, will try later : ',e.message
            return None
        if response.status_code == 200:
            return response.text
        else:
            return None

    def parse(self):
        tempitem = self.unfinished_links_queue.get_nowait()
        url = tempitem.url

        html_code = self.request_html(url)
        if html_code is None:
            return []

        tree = html.fromstring(html_code)
        try:
            title = tree.xpath('//*[@id="firstHeading"]/text()')[0]
        except Exception as e:
            print 'Error parsing title : ',e.message
            self.unfinished_links_queue.put_nowait(tempitem) #maybe unwise
            return []

        print 'Parsed - ', title
        try:
            return [ (tempitem, x.xpath('.//@href')[0]) for x in tree.xpath('//*[@id="mw-content-text"]//a') ]
        except Exception as e:
            print 'Error parsing <a> tags : ',e.message

    def check_url(self,url):
        #convert this to regex
        if url[0:6] == '/wiki/' and url[-4:-3] != '.':
            return 'good'
        return 'bad'

    def add_new_links(self):
        valid_links = [ (x[0],self.domain + x[1]) for x in self.parse() if self.check_url(x[1]) == 'good' ]
        # add error handling here

        for link in valid_links:
            self.pages_processsed += 1
            tempitem = HtmlItem(self.id_count,link[1])
            self.id_count += 1
            tempitem.parent_id = link[0].id
            if link[0].recursion_level + 1 < self.max_recursion_level:
                # add dp/repition check here
                tempitem.recursion_level = link[0].recursion_level + 1
                self.unfinished_links_queue.put_nowait(tempitem)
                # add some way to store these objects

    def crawl(self):
        while not self.unfinished_links_queue.empty() and not self.workers_pool.full():
            for x in xrange(0, min(self.unfinished_links_queue.qsize(), self.workers_pool.free_count())):
                greenlet_thread = self.workers_pool.spawn(self.add_new_links)
                self.workers_pool.start(greenlet_thread)

        self.workers_pool.join()


c = RecursiveCrawler('https://en.wikipedia.org/wiki/Python_(programming_language)','https://en.wikipedia.org',32)
c.crawl()

print 'Items Processed : ', c.pages_processsed
print 'Requests Made : ', c.requests_sent
print ('The script took {0} second !'.format(time.time() - startTime))
