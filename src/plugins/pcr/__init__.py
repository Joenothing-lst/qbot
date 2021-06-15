from nonebot import require, on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent
from nonebot.adapters.cqhttp.utils import unescape, escape
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from src.utils.util import safe_send
from .data_source import PcrWatching

scheduler = require('nonebot_plugin_apscheduler').scheduler
pcr_news = PcrWatching()

@scheduler.scheduled_job('cron', minute='*', id='pcr')
async def _():
    rss_dic = {
        pcr_news: {'id': [856911915, 697475156], 'send_type': 'group', 'name': '台服新闻'},
    }

    for rss, config in rss_dic.items():
        diff_items = await rss.checking_rss()
        if diff_items:
            msg = f"{config['name']}更新辣！！！" + diff_items
            await safe_send(config['send_type'], config['id'], Message(msg))

pcr_cmd = on_command('台服新闻')

@pcr_cmd.handle()
async def _(bot: Bot, event: MessageEvent):
    urls = await pcr_news.get_news_list()
    msg = await pcr_news.get_msg([f"{pcr_news.host}{url}" for url in urls])
    await bot.send(event, Message(msg))