import re

from nonebot import require, on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent
from nonebot.adapters.cqhttp.utils import unescape, escape
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from src.utils.util import safe_send
from .data_source import PcrWatching, get_name

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


pcr_id_cmd = on_command('查id', aliases={'cid', })

@pcr_id_cmd.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = str(event.message)
    result = re.findall('\d{9}', msg)
    if result:
        uid = result[0]
    else:
        return None

    result = re.findall('\D([\d一二三])\D', msg)
    if result:
        if not result[0].isdigit():
            if result[0] == '二':
                cid = 2
            elif result[0] == '三':
                cid = 3
            elif result[0] == '四':
                cid = 4
            else:
                cid = 1
        else:
            cid = int(result[0])
    else:
        cid = 1

    data = await get_name(uid, cid)

    if data['status'] == 'error':
        res = data['msg']
    else:
        res = f"您查询的角色id是{uid}\n游戏名称是{data['userName']}"


    await bot.send(event, Message(res))
