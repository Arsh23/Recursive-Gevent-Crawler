import asyncio
import aiohttp
from lxml import html

@asyncio.coroutine
def get(url):
    response = yield from aiohttp.request('GET', url, compress=True)
    return (yield from response.text())

queue = asyncio.Queue()
queue.put_nowait('https://en.wikipedia.org/wiki/Python_(programming_language)')
queue.put_nowait('https://en.wikipedia.org/wiki/List_of_HTTP_status_codes')

print(queue)

urls = ['https://en.wikipedia.org/wiki/Python_(programming_language)','https://en.wikipedia.org/wiki/List_of_HTTP_status_codes']

@asyncio.coroutine
def print_result(work_queue,recursion_level):
    # while not work_queue.empty():
    global urls
    url = yield from work_queue.get()
    print('start - ',url)
    # url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
    page = yield from get(url)
    # urls.append('https://en.wikipedia.org/wiki/Ruby_(programming_language)')
    tree = html.fromstring(page)
    title = tree.xpath('//*[@id="firstHeading"]/text()')
    links = tree.xpath('//*[@id="mw-content-text"]//a')
    print('extacted - ',title)
    # print(links)

    # if recursion_level == 1:
    #     print(title)
    #     return

    # next_links = []
    # for link in links:
    #     next_link = link.xpath('.//@href')
    #
    #     if next_link[0:6] == '/wiki/' and next_link[-4:-3] != '.':
    #         # print(next_link)
    #         next_links.append(next_link)


loop = asyncio.get_event_loop()
# tasks = [asyncio.async(print_result(queue,0))]
# loop.create_task(asyncio.async(print_result(queue,0)))
f = asyncio.async(print_result(queue,0))
loop.run_until_complete(f)
# loop.run_forever()
