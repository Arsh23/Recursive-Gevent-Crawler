from lxml import html
import time
from twisted.internet import reactor
import twisted.internet.defer
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent

urls = ['https://en.wikipedia.org/wiki/Python_(programming_language)','https://en.wikipedia.org/wiki/Space_exploration']

def getDummyData(inputData):
    print 'getDummyData called'
    deferred =twisted.internet.defer.Deferred()
    x=0
    while x<1000:
        print x
        time.sleep(1)
        x=x+1

    # reactor.callLater(2, deferred.callback, inputData * 3)
    return deferred

# class PrinterClient(Protocol):
#     def __init__(self, whenFinished):
#         self.whenFinished = whenFinished
#
#     def dataReceived(self, bytes):
#         # print '##### Received #####\n%s' % (bytes,)
#         tree = html.fromstring(bytes)
#         title = tree.xpath('//*[@id="firstHeading"]/text()')
#         links = tree.xpath('//*[@id="mw-content-text"]//a')
#         print 'extacted - ', title
#
#
#     def connectionLost(self, reason):
#         print 'Finished:', reason.getErrorMessage()
#         self.whenFinished.callback(None)

class SimpleReceiver(Protocol):
    def __init__(self, d):
        self.buf = ''; self.d = d

    def dataReceived(self, data):
        print 'getting data'
        self.buf += data

    def connectionLost(self, reason):
        print 'got data'
        self.d.callback(self.buf)


def parse(htmlcode):
    tree = html.fromstring(htmlcode)
    title = tree.xpath('//*[@id="firstHeading"]/text()')
    links = tree.xpath('//*[@id="mw-content-text"]//a')
    print 'extacted - ', title

    for link in links:
            next_link = link.xpath('.//@href')[0]

            if next_link[0:6] == '/wiki/' and next_link[-4:-3] != '.':
                pass
                # print next_link

def handleResponse(r):
    # print "version=%s\ncode=%s\nphrase='%s'" % (r.version, r.code, r.phrase)
    # for k, v in r.headers.getAllRawHeaders():
        # print "%s: %s" % (k, '\n  '.join(v))
    whenFinished = twisted.internet.defer.Deferred()
    whenFinished.addCallbacks(parse)
    r.deliverBody(SimpleReceiver(whenFinished))

    return whenFinished

def handleError(reason):
    reason.printTraceback()
    reactor.stop()

def getPage(url):
    print "Requesting %s" % (url,)
    d = Agent(reactor).request('GET', url, None, None)
    d.addCallbacks(handleResponse, handleError)
    return d



semaphore = twisted.internet.defer.DeferredSemaphore(32)
dl = list()

for url in urls:
    dl.append(semaphore.run(getPage, url))
dl = twisted.internet.defer.DeferredList(dl)
dl.addCallbacks(lambda x: reactor.stop(), handleError)


# deferred = getDummyData(3)
# deferred.addCallback(cbPrintData)


reactor.run()
