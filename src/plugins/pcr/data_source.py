from lxml import etree

from src.utils.util import async_request

TW_URL = 'http://www.princessconnect.so-net.tw'
JP_URL = ''

TEMP = "\n{title}\n{img}\n{detail}\n{link}"

class PcrWatching:
    urls_cache: list = []

    def __init__(self, watch_type: str = "tw", **kwargs):
        """
        提供简单的 rss 监控及格式化功能

        :param watch_type: 服务器
        :param kwargs: 请求参数
        """
        self.host = TW_URL if watch_type == 'tw' else JP_URL
        self.watch_url = self.host + '/news'
        self.kwargs = kwargs

    async def get_news_list(self):
        res = await async_request('get', self.watch_url, **self.kwargs)
        html = etree.HTML(text=res.text)

        urls = html.xpath('//article[@class="news_con"]/dl/dd/a/@href')

        return urls

    def check_url(self, urls):
        if not self.urls_cache:
            self.urls_cache = urls

        diff_urls = [f"{self.host}{url}" for url in urls if url not in self.urls_cache]

        if diff_urls:
            self.urls_cache = urls

        return diff_urls

    async def get_news_detail(self, url):
        res = await async_request('get', url, **self.kwargs)
        html = etree.HTML(text=res.text)

        item = {'link': url}

        item['title'] = html.xpath('//article[@class="news_con"]//h3/text()')[0]

        img = html.xpath('//article[@class="news_con"]//img/@src')

        if img:
            item['img'] = f'[CQ:image,file={img[0]}]'
        else:
            item['img'] = ''

        detail = html.xpath('//article[@class="news_con"]//p/text()') + html.xpath('//article[@class="news_con"]//div/text()')

        item['detail'] = '\n'.join(i for i in detail if i.strip())[:120] + '...'

        return TEMP.format(**item)

    async def get_msg(self, url_list):
        news_list = []

        for url in url_list:
            temp = await self.get_news_detail(url)
            news_list.append(temp)

        return '\n'.join(news_list)

    async def checking_rss(self):
        urls = await self.get_news_list()

        diff_urls = self.check_url(urls)

        if diff_urls:
            msg = await self.get_msg(diff_urls)
            return msg
