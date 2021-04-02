from feedparser import parse, FeedParserDict
from typing import Union, Dict, Tuple

from src.utils.util import async_request


class RssHub:

    items_cache: list = []

    def __init__(self, rss_url: str, temp: str = "\n{title}\n{link}", **kwargs):
        """
        提供简单的 rss 监控及格式化功能

        :param rss_url: rss 订阅链接
        :param temp: 消息模版
        :param kwargs: 请求参数
        """
        self.rss_url = rss_url
        self.temp = temp
        self.kwargs = kwargs

    @staticmethod
    async def async_parse(rss_url: str = None, **kwargs) -> FeedParserDict:
        """
        使用异步 get 请求解析 rss 链接，返回解析后的 FeedParserDict 对象

        :param rss_url: 默认使用初始化时的 rss 订阅链接
        :param kwargs: 请求使用的参数
        :return: FeedParserDict 对象
        """
        res = await async_request('get', rss_url, **kwargs)
        rss_dict = parse(res)
        return rss_dict

    def check_rss(self, items: Union[FeedParserDict, list], path_to_items: str = 'entries') -> list:
        """
        对比 items_cache 是否有新的 item 出现，有则返回新增的 item

        :param items: items 列表 或 解析后的 FeedParserDict 对象
        :param path_to_items: 解析出 items 的路径
        :return: 新增的 items 列表
        """
        if isinstance(items, FeedParserDict):
            items = items.get(path_to_items, [])

        assert isinstance(items, list)

        if not self.items_cache:
            self.items_cache = items

        diff_items = [item for item in items if item not in self.items_cache]

        if diff_items:
            self.items_cache = items

        return diff_items

    def gen_msg_from_temp(self, items: list, temp: str = "\n{title}\n{link}") -> str:
        """
        使用 items 填充模版(temp)，返回填充后的消息

        :param items: items 列表
        :param temp: 必须是可以 format 的模版字符串，默认 "\n{title}\n{link}"
        :return:
        """
        return '\n'.join(self._format(item, temp) for item in items)

    @staticmethod
    def _format(item: dict, temp: str = "\n{title}\n{link}", list_format: Dict[str, Tuple[str, str]] = None):
        """
        对 item 里的一些列表处理成合适的字符串

        :param temp: 必须是可以 format 的模版字符串，默认 "\n{title}\n{link}"
        :param item: 单个 item 字典
        :param list_format: 需要处理的 index、key 和 间隔符
        :return:
        """
        list_format_dict = list_format or {
            'links': ('href', '\n'),
            'tags': ('term', '、'),
            'authors': ('name', '、')
        }

        _item = item.copy()

        for key, config in list_format_dict.items():
            index, fill = config
            _item[key] = fill.join(tag.get(index, '') for tag in item.get(key, []))

        return temp.format(**_item)

    async def checking_rss(self) -> str:
        """
        检查是否有新的 rss 并使用模版转换成消息

        :return:
        """
        rss_dict = await self.async_parse(self.rss_url, **self.kwargs)

        diff_items = self.check_rss(rss_dict)

        return self.gen_msg_from_temp(diff_items, self.temp)
