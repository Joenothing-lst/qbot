from functools import reduce

import requests
from nonebot import require

from src.utils.util import safe_send

scheduler = require('nonebot_plugin_apscheduler').scheduler

headers = {
    'Host': 'www.apple.com.cn',
    'accept': '*/*',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac',
    # 'referer': 'https://servicewechat.com/wx09dd4aff96ba65c1/104/page-frame.html',
    'accept-language': 'zh-CN,zh-Hans;q=0.9',
}


def getitem(a, b):
    if isinstance(b, list):
        return a[b[0]]
    else:
        return a[b]


def lookup(data, keys, default=None):
    """
    根据路径查找对象

    :param data: 需要被查找的对象
    :param keys: 索引列表
    :param default: 默认结果
    :return:
    """
    try:
        r = reduce(getitem, keys, data)
    except KeyError:
        r = default
    except IndexError:
        r = default
    except TypeError:
        r = default

    return r or default


def main(model):
    stores = {
        'R471': '西湖店',
        'R532': '万象店'
    }

    for store in stores:
        url = f'https://www.apple.com.cn/shop/fulfillment-messages?pl=true&mt=compact&parts.0={model}&store={store}'
        response = requests.get(url, headers=headers)
        data = response.json()
        pickup_message = lookup(data, ['body', 'content', 'pickupMessage'])
        store_stock = lookup(pickup_message, ['stores', [0], 'partsAvailability', model,
                                    'pickupSearchQuote'])
        model_name = lookup(pickup_message, ['stores', [0], 'partsAvailability', model, 'messageTypes', 'compact', 'storePickupProductTitle'])
        if store_stock != '暂无供应':
            yield f'【{lookup(pickup_message, ["pickupLocation"], "")}】-「{model_name}」有货, {store_stock}'
        # else:
        #     yield f'【{lookup(pickup_message, ["pickupLocation"], "")}】-「{model_name}」{store_stock}'


@scheduler.scheduled_job('cron', second='*/2', id='iphone_monitor')
async def _():
    # iPhone 14 Pro Max 256G 暗夜紫
    model = 'MQ8A3CH/A'

    for msg in main(model):
        await safe_send('private', 912871833, msg)
