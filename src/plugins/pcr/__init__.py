from nonebot import require

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
            msg = f"{config['name']}更新辣！！！\n" + diff_items
            await safe_send(config['send_type'], config['id'], msg)