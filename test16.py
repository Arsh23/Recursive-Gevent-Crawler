from gevent import monkey
monkey.patch_all()

import time

startTime = time.time()

import requests
from gevent import pool, queue
from lxml import html

import gevent
jobs = []
urls2 = []
# links = []
p = pool.Pool(32)
q = queue.Queue()
s = requests.Session()

started = 0
completed = 0


q.put('https://en.wikipedia.org/wiki/Python_(programming_language)')
pages = 0

def get_links(r):
    # print q
    global started, completed
    started = started + 1
    url = q.get_nowait()
    print 'request sent for - ',url
    global pages
    r = s.get(url)

    if r.status_code == 200:
        tree = html.fromstring(r.text)
        title = tree.xpath('//*[@id="firstHeading"]/text()')
        links = tree.xpath('//*[@id="mw-content-text"]//a/@href')
        print 'extacted - ', title, 'pages scraped =  ',pages
        pages = pages + 1
        # next_links = []
        for link in links:
            print link
            # next_link = link.xpath('.//@href')[0]

            # if next_link[0:6] == '/wiki/' and next_link[-4:-3] != '.':
                # if p.full():
                #     print 'skipped - ' + 'https://en.wikipedia.org' + next_link
                #     continue
                # q.put_nowait('https://en.wikipedia.org' + next_link)
                # p.spawn(get_links, 'https://en.wikipedia.org' + next_link ,0)
    # q.task_done()
    completed = completed + 1

#
# for url in urls:
#     p.spawn(get_links, url,0)
# print p
g = p.spawn(get_links,0)
p.start(g)
p.join()

# print p
# while not q.empty() and not p.full():
#     # if started == completed:
#         for x in xrange(0, min(q.qsize(), p.free_count())):
#             g = p.spawn(get_links,0)
#             p.start(g)
#             print 'queue',q.qsize(),'pool',p.free_count()
#     # else:
#         # print 'skip !!!'
#         # print 'started',started,'completed',completed
#         # break
#
# p.join()
print ('The script took {0} second !'.format(time.time() - startTime))
