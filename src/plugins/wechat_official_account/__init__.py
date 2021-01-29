from nonebot import require, on_command, on_message, on_keyword
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.adapters.cqhttp.event import MessageEvent
from nonebot.adapters.cqhttp.permission import PRIVATE, GROUP
from nonebot.adapters.cqhttp.utils import unescape, escape
from src.utils.argparse import gen_parser

from .data_source import WeChat

vx = WeChat()
vx_cmd = on_command('vx', permission=SUPERUSER)
vx_parser = gen_parser()
vx_parser.add_argument('-l', dest='login', action='store_true')
vx_parser.add_argument('-s', dest='search', action='store_true')
# vx_parser.add_argument('-g', dest='to_group', action='store_true')

@vx_cmd.handle()
async def first_receive(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if not state.get('vx'):
        state['vx'] = vx
    if msg:
        state['args'] = msg

@vx_cmd.got('args', )
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = state['args'].split(None, 1)
    if args[0] == state['_prefix']['raw_command']:
        args = args[1].split(None, 1)

    try:
        cmd = vx_parser.parse_args([args[0]])
    except Exception as e:
        await vx_cmd.finish('命令解析失败' + str(e))
        return

    if args[0] == args[-1]:
        await vx_cmd.reject('命令缺少[args,]\n' + __doc__)
    param = args[-1]

    vx:WeChat = state['vx']

    if cmd.h:
        await vx_cmd.reject(__doc__)
    elif cmd.f:
        await vx_cmd.finish('本次命令结束')

    if cmd.login:
        username, password = param.split(None, 1)
        img_path = await vx.get_login_qrcode(username, password)
        await bot.send(event, message=MessageSegment.image(file=f'file:///{img_path}'))
        await vx.login(username)
        await bot.send(event, message='登录成功')

    if cmd.search:
        if vx.is_login:
            res = await vx.get_firsts_official_atc(*param.split(None, 1))
            if isinstance(res, dict):
                msg = f"搜索到关键词{res['keywords']}"
                for article in res['articles']:
                    temp = f'''\n\n标题： {article['title']}
简介： {article['digest']}
日期： {article['create_time']}
链接： {article['link']}
'''
                    msg += temp
                await bot.send(event, message=msg)
            else:
                await bot.send(event, message=res)

        else:
            await bot.send(event, message='您还未登录！请使用以下命令扫码登录:\nvx -l 公众号账号 密码')
            await vx_cmd.finish()

    if cmd.download:
        if vx.is_login:
            url = await vx.download_article_images(param.split())
            await bot.send(event, message=f'下载完成：\n{url}')
        else:
            await bot.send(event, message='您还未登录！请使用以下命令扫码登录:\nvx -l 公众号账号 密码')
            await vx_cmd.finish()
