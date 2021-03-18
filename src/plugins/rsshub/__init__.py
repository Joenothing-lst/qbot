from nonebot import require

from .data_source import RssHub
from .utils import safe_send

scheduler = require('nonebot_plugin_apscheduler').scheduler

rss = RssHub('https://dig.chouti.com/feed.xml')
headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

rss_temp = """\n{title}
{link}"""

@scheduler.scheduled_job('cron', minute='*', id='rss_chouti')
async def _():
    rss_dict = await rss.parse_rss(headers=headers)
    diff_items = rss.check_rss(rss_dict, ['entries'])
    if diff_items:

        msg = f'更新辣！！！ 一共{len(diff_items)}条消息' + rss.gen_msg_from_temp(diff_items, rss_temp)
        await safe_send('group', 175039192, msg)

