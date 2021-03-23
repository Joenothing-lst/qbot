from nonebot import require

from .data_source import RssHub
from .utils import safe_send

scheduler = require('nonebot_plugin_apscheduler').scheduler

headers1 = {
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

headers2 = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://www.galgamezs.net/bbs/forumdisplay.php?fid=8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

temp = "\n【{tags}】{title}\n{link}"

rss_chouti = RssHub('https://dig.chouti.com/feed.xml', temp, headers=headers1)
rss_chouti_hot = RssHub('https://rsshub.app/chouti/hot', temp)
rss_agree = RssHub(
    'http://www.galgamezs.net/bbs/rss.php?fid=8&auth=7922Wq3mDt%2FPddHPHDb%2BMHiWp%2FP3Xj9Uv56wSMHEoFweHME5gOzqdH08cXQCV1k',
    headers=headers2
)

@scheduler.scheduled_job('cron', minute='*', id='rsshub')
async def _():
    rss_dic = {
        rss_chouti: {'id': 175039192, 'send_type': 'group', 'name': '抽屉'},
        rss_chouti_hot: {'id': 175039192, 'send_type': 'group', 'name': '抽屉热榜'},
        rss_agree: {'id': [816888439], 'send_type': 'group', 'name': '黑丸同人区'},
    }

    for rss, config in rss_dic.items():
        diff_items = await rss.checking_rss()
        if diff_items:
            msg = f"{config['name']}更新辣！！！" + diff_items
            await safe_send(config['send_type'], config['id'], msg)
