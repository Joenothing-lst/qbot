from typing import Union
from feedparser import parse, FeedParserDict

from src.utils.util import async_request


class RssHub():

    def __init__(self, rss_url: str):
        self.rss_url = rss_url
        self.items_cache = []

    async def parse_rss(self, rss_url: str=None, **kwargs) -> FeedParserDict:
        """
        使用异步 get 请求解析 rss 链接，返回解析后的 FeedParserDict 对象

        :param rss_url: 默认使用初始化时的 rss 订阅链接，传入其他 rss 订阅链接时会替换掉初始化时的 rss 订阅链接
        :param kwargs: 请求使用的参数
        :return: FeedParserDict 对象
        """
        res = await async_request('get', rss_url or self.rss_url, **kwargs)
        rss_dict = parse(res.text)
        return rss_dict


    def check_rss(self, items: Union[FeedParserDict, list], path_to_items: list=None) -> list:
        """
        对比 items_cache 是否有新的 item 出现，有则返回新增的 item

        :param items: items 列表 或 解析后的 FeedParserDict 对象
        :param path_to_items: 解析出 items 的路径
        :return: 新增的 items 列表
        """
        if isinstance(items, FeedParserDict) and path_to_items:
            for path_ in path_to_items:
                items = items.get(path_, {})

        assert isinstance(items, list)

        diff_items = list(set(items).difference(set(self.items_cache)))

        if diff_items:
            self.items_cache = items

        return diff_items

    @staticmethod
    def gen_msg_from_temp(items: list, temp: str) -> str:
        """
        使用 items 填充模版(temp)，返回填充后的消息

        :param items: items 列表
        :param temp: 必须是可以 format 的模版字符串
        :return:
        """
        msg = '\n'.join(temp.format(**item) for item in items)
        return msg


