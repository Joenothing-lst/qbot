from lxml import etree

# from src.utils.util import async_request

###
import requests
###


def request(method: str, url: str, **kwargs):
    if method.upper() == 'GET':
        return requests.get(url, **kwargs)
    elif method.upper() == 'POST':
        return requests.post(url, **kwargs)


def search_r18book(keywords: str, page=1, limit=5):
    keyword = '+'.join(keywords.split())
    res = request('get', f'https://nhentai.net/search/?q={keyword}&page={page}')
    html = etree.HTML(text=res.text)
    el = html.xpath('//div[@class="gallery"]/a')
    books = []
    for i in el[:limit]:
        book = {}
        book['link'] = 'https://nhentai.net' + i.xpath('./@href')[0]
        book['faceimg'] = i.xpath('./img/@data-src')[0]
        book['name'] = i.xpath('./div/text()')[0]
        books.append(book)

    return books




