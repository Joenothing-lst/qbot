from lxml import etree

from src.utils.util import async_request

TW_URL = 'http://www.princessconnect.so-net.tw/'
JP_URL = ''

TEMP = "\n{title}\n{img}\n{detail}\n{link}"

class PcrWatching:
    links_cache: list = []

    def __init__(self, watch_type: str = "tw", **kwargs):
        """
        提供简单的 rss 监控及格式化功能

        :param watch_type: 服务器
        :param kwargs: 请求参数
        """
        self.host = TW_URL if watch_type == 'tw' else JP_URL
        self.watch_url = self.host + 'news'
        self.kwargs = kwargs

    async def get_news_list(self):
        res = await async_request('get', self.watch_url, **self.kwargs)
        html = etree.HTML(text=res.text)

        links = html.xpath('//article[@class="news_con"]/dl/dd/a/@href')

        if not self.links_cache:
            self.links_cache = links

        diff_links = [f"{self.host}{link}" for link in links if link not in self.links_cache]

        if diff_links:
            self.links_cache = links

        return diff_links

    async def get_news_detail(self, url):
        res = await async_request('get', url, **self.kwargs)
        html = etree.HTML(text=res.text)

        item = {'link': url}

        item['title'] = html.xpath('//article[@class="news_con"]//h3/text()')[0]

        img = html.xpath('//article[@class="news_con"]//img/@src')

        if img:
            item['img'] = f'[CQ:image,url={img[0]}]'
        else:
            item['img'] = ''

        detail = html.xpath('//article[@class="news_con"]//p/text()') + html.xpath('//article[@class="news_con"]//div/text()')

        item['detail'] = '\n'.join(i for i in detail if i.strip())[:120] + '...'

        return TEMP.format(**item)

    async def checking_rss(self):
        diff_items = await self.get_news_list()

        if diff_items:
            msg = '\n\n'.join(await self.get_news_detail(url) for url in diff_items)
            return msg
