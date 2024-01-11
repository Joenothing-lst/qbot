import nonebot
import requests
from nonebot import on_command
from nonebot import require
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent

from src.utils.util import safe_send

scheduler = require('nonebot_plugin_apscheduler').scheduler
get_stock_cmd = on_command('get_stock', aliases={'看看基金', '看看基', '看看鸡'})


@get_stock_cmd.handle()
async def async_get_stock(bot: Bot, event: MessageEvent):
    msg = get_stock(bot)
    await bot.send(event, msg)


# 每天早上10点45、下午2点45、下午3点45发送
@scheduler.scheduled_job('cron', hour='10,14,15', minute='45', id='A_stock')
async def _():
    bot = nonebot.get_bot()
    msg = get_stock(bot)

    await safe_send('private', 912871833, msg)


def get_stock(bot):
    stock_code = '161725'
    token = bot.config.personal_api_key
    url = f"http://127.0.0.1/AStock/get_stock?token={token}&stock_code={stock_code}"
    res = requests.get(url).json()

    # 成本金额
    cb = 60000
    # 成本净值
    cbjz = 0.96
    # 持有份额
    fe = cb / cbjz
    # 当前市值
    sz = float(res['data']['zxj']) * fe
    # 当前盈亏
    yk = sz - cb
    # 当前盈亏比例
    ykbl = yk / cb * 100
    # 今日收益
    jrsy = ykbl * cb / 100

    string_list = []
    string_list.append(f"最新净值: {res['data']['zxj']}")
    string_list.append(f"今日涨跌幅: {res['data']['zdf']}%")
    string_list.append(f"今日预计收益: {jrsy:.3f}")
    string_list.append('===============')
    string_list.append(f"成本金额: {cb}")
    string_list.append(f"持有份额: {fe}")
    string_list.append(f"当前市值: {sz:.3f}")
    string_list.append(f"成本净值: {cbjz:.3f}")
    string_list.append(f"持有收益: {yk:.3f}")
    string_list.append(f"持有收益率: {ykbl:.3f}%")
    string_list.append('===============')
    string_list.append(f"涨跌额: {res['data']['zde']}")
    string_list.append(f"最高净值: {res['data']['zg']}")
    string_list.append(f"最低净值: {res['data']['zd']}")
    string_list.append(f"今日开盘: {res['data']['jk']}")
    string_list.append(f"昨日收盘: {res['data']['zs']}")
    return '\n'.join(string_list)
