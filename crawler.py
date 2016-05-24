import asyncio
import aiohttp
from lxml import html

@asyncio.coroutine
def get(url):
    response = yield from aiohttp.request('GET', url, compress=True)
    return (yield from response.text())

@asyncio.coroutine
def print_result(url):
    # url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
    page = yield from get(url)
    urls.append('https://en.wikipedia.org/wiki/Ruby_(programming_language)')
    tree = html.fromstring(page)
    title = tree.xpath('//*[@id="firstHeading"]/text()')
    print(title)


urls = ['https://en.wikipedia.org/wiki/Python_(programming_language)','https://en.wikipedia.org/wiki/List_of_HTTP_status_codes']
loop = asyncio.get_event_loop()
f = asyncio.wait([print_result(x) for x in urls])
loop.run_until_complete(f)
