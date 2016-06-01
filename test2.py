from requests import async
from lxml import html








#
# urls = ['https://en.wikipedia.org/wiki/Python_(programming_language)','https://en.wikipedia.org/wiki/Space_exploration']
#
# def send_requests(urls):
#     return async.map( [ async.get(url) for url in urls ] )
#
# results = send_requests(urls)
#
# for response in results:
#     tree = html.fromstring(response.content)
#     title = tree.xpath('//*[@id="firstHeading"]/text()')
#     links = tree.xpath('//*[@id="mw-content-text"]//a')
#     print 'extacted - ', title
#
#     next_links = []
#     for link in links:
#         next_link = link.xpath('.//@href')[0]
#
#         if next_link[0:6] == '/wiki/' and next_link[-4:-3] != '.':
#             print(next_link)
#             next_links.append('https://en.wikipedia.org' + next_link)
#
#
#     r = send_requests(next_links)
#
#     for resp in r:
#         tree = html.fromstring(resp.content)
#         title = tree.xpath('//*[@id="firstHeading"]/text()')
#         links = tree.xpath('//*[@id="mw-content-text"]//a')
#         print('extacted - ',title)
