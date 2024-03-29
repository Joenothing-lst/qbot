import re
import json
import codecs
from lxml import etree
from typing import List, Union, Optional
from src.utils.util import async_request, get_loop_and_run
from nonebot.adapters.cqhttp.message import Message, MessageSegment

###
import requests

headers = {
    'authority': 'nhentai.net',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    # Requests sorts cookies= alphabetically
    'cookie': 'cf_chl_2=1579ada695f30b6; cf_chl_prog=x13; cf_clearance=HXtWYDkNp56WGdq_Zs7KBpGxwswpB59IjFevFd6.7zI-1652859641-0-150; csrftoken=3v7ZND7BsFGKijakyTGjzxSusXwmTGDkhvsY1tmj9kGtKl75nP5RP32dulHrEZcu',
    'pragma': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
}
###


class Page:
    book_id: int
    media_id: int
    page_num: int
    url: str
    image_url: str
    image_type: str

    def __init__(self, book_id: Union[int, str], media_id: Union[int, str], page_num: Union[int, str] = 0,
                 image_type: str = 'jpg'):
        self.book_id = int(book_id)
        self.media_id = int(media_id)
        self.page_num = int(page_num)
        self.image_type = image_type
        self.url = f'https://nhentai.net/g/{self.book_id}/{self.page_num + 1}'
        self.image_url = f'https://i.nhentai.net/galleries/{self.media_id}/{self.page_num + 1}.{self.image_type}'


class Book:
    book_id: int
    url: str
    author: str
    page: int
    media_id: int
    tags: List[str]
    upload_date: int
    cover: str

    def __init__(self, id_or_url: Union[int, str]):
        if isinstance(id_or_url, int) or id_or_url.isdigit():
            self.book_id = int(id_or_url)
            self.url = f'https://nhentai.net/g/{self.book_id}/'
        else:
            match = re.findall(r'/g/d+', id_or_url)
            if match:
                self.book_id = int(match[0])
                self.url = f'https://nhentai.net/g/{self.book_id}/'
            else:
                raise Exception('Error book id_or_url')

        # get_loop_and_run(self.__get_book())
        self.__get_book()

    @property
    def pages(self):
        return [Page(self.book_id, self.media_id, num, self.image_type) for num in range(self.page)]

    # async def __get_book(self):
    def __get_book(self):
        # try:
            # res = await async_request('get', self.url)
        res = request('get', self.url, headers=headers, timeout=5)
        # except:
        #     raise Exception('Error network')
        match = re.findall('''JSON\.parse\(["'](.+?)["']\)''', res.text)
        if match:
            data = json.loads(codecs.decode(match[0], 'unicode_escape'))
            self.media_id = data.get('media_id', 0)
            self.upload_date = data.get('upload_date', 0)
            self.tags = [tag.get('name', '') for tag in data.get('tags', [])]
            self.title = data.get('title', {}).get('japanese', '')
            self.page = data.get('num_pages', 0) or len(data.get('images', {}).get('pages', []))
            image_type = data.get('images', {}).get('cover', {}).get('t', '')
            if image_type == 'p':
                self.image_type = 'png'
            elif image_type == 'j':
                self.image_type = 'jpg'
            else:
                self.image_type = ''
            self.cover = f'https://t.nhentai.net/galleries/{self.media_id}/cover.{self.image_type}'
        else:
            raise Exception('Parse error')


def request(method: str, url: str, **kwargs):
    if method.upper() == 'GET':
        return requests.get(url, **kwargs)
    elif method.upper() == 'POST':
        return requests.post(url, **kwargs)


async def search_r18book(keywords: str, page=1, limit=5):
    keyword = '+'.join(keywords.split())
    res = await async_request('get', f'https://nhentai.net/search/?q={keyword}&page={page}')
    html = etree.HTML(text=res.text)
    el = html.xpath('//div[@class="gallery"]/a')
    books = []
    for i in el[:limit]:
        book = {}
        book['link'] = 'https://nhentai.net' + i.xpath('./@href')[0]
        match = re.findall(r'\/g\/(\d+)', book['link'])
        if match:
            book['book_id'] = int(match[0])
        book['cover'] = i.xpath('./img/@data-src')[0]
        book['title'] = i.xpath('./div/text()')[0]
        books.append(book)

    return books


def gen_forward_message(msg_list, user_id):
    msg_temp = []
    for msg in msg_list:
        node = {
            "type": "node",
            "data": {
                "name": "NM$L-bot",
                "uin": str(user_id),
                "content": Message(msg),
                # "content": {
                #     "type": "text",
                #     "data": {
                #         "text": msg
                #     }
                # }
            }
        }
        msg_temp.append(node)

    return msg_temp


HOST = 'https://www.cilitiantang2031.xyz'


async def search_mag(kw):
    url = f'{HOST}/search/{kw}_ctime_1.html'
    res = await async_request('get', url)
    html = etree.HTML(text=res.text)

    items = html.xpath('//div[@class="col-md-8"]/div[@class="panel panel-default"]/div[@class="panel-body"]')

    results = []
    for item in items:
        result = {}
        result['title'] = ''.join(item.xpath('.//a//text()'))
        result['link'] = HOST + item.xpath('.//a/@href')[0]
        result['date'], result['size'], result['hot'] = [i for i in item.xpath('string(.//table)').split('\n') if i]
        results.append(result)

    return results


async def get_mag(url):
    if not url.startswith('http'):
        url = HOST + url
    res = await async_request('get', url)
    html = etree.HTML(text=res.text)

    mag = html.xpath('//textarea[@id="MagnetLink"]/text()')[0]
    return mag


if __name__ == '__main__':
    import asyncio

    # def main():
    #     book = Book(356462)
    #     print(book.pages)

    loop = asyncio.get_event_loop()

    book = Book(356462)




    # print(book.pages)
    get_loop_and_run(book.get_book)
    print(book.pages)

    loop.run_forever()


    # r = search_r18book('[観用少女(こもた)]:Connect-少女は触手と愛をつむぐ- [中国翻訳]')
    # print(r)
