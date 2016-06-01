import asyncio
import aiohttp
from lxml import html

queue = asyncio.Queue()
queue.put_nowait('https://en.wikipedia.org/wiki/Python_(programming_language)')
queue.put_nowait('https://en.wikipedia.org/wiki/Ruby_(programming_language)')

@asyncio.coroutine
def request(url):
    response = yield from aiohttp.request('GET', url, compress=True)
    return (yield from response.text())

@asyncio.coroutine
def parse(task_name, work_queue):
    global queue
    while not work_queue.empty():
        url = yield from work_queue.get()
        print('{0} grabbed item: {1}'.format(task_name, url))
        # q.put_nowait(queue_item+10)
        # q.put_nowait(queue_item+10)
        # yield from asyncio.sleep(0.5)

        page = yield from request(url)
        tree = html.fromstring(page)
        title = tree.xpath('//*[@id="firstHeading"]/text()')
        links = tree.xpath('//*[@id="mw-content-text"]//a')

        # next_links = []
        for link in links:
            next_link = link.xpath('.//@href')[0]
            # print(next_link)
            if next_link[0:6] == '/wiki/' and next_link[-4:-3] != '.':
                queue.put_nowait('https://en.wikipedia.org' + next_link)
                # print(next_link)
                # next_links.append(next_link)


        print('extacted - ',title)
        print('processed - ',url)



# for x in range(20):
#     q.put_nowait(x)

# print(q)

loop = asyncio.get_event_loop()
tasks = [ asyncio.async(parse('task ' + str(x), queue)) for x in range(100) ]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
