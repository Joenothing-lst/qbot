from nonebot import require, on_command, on_message, on_keyword, on_shell_command
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.message import Message
from nonebot.adapters.cqhttp.event import MessageEvent
from nonebot.adapters.cqhttp.permission import PRIVATE, GROUP
from nonebot.adapters.cqhttp.utils import unescape, escape

from src.utils.util import gen_parser
from .data_source import get_group_id_list, gen_qq


__doc__ = '''to -[ugsabf] [args,]
-u: 私聊，args为 私聊对象qq号 消息
-g: 群聊，args为 群聊群qq号 消息
-s: 多个消息目标，args为 qq号 qq号 qq号 消息
-a: 以所有群聊为消息目标，args为 消息
-b: 只有-a时生效，以除了某群的所有群聊为消息目标，args为 qq号 消息
-f: 结束当前会话
'''

to_cmd = on_command('to', aliases={'转发'}, permission=SUPERUSER)

to_parser = gen_parser()
to_parser.add_argument('-u', dest='to_user', action='store_true')
to_parser.add_argument('-g', dest='to_group', action='store_true')
to_parser.add_argument('-s', dest='several', action='store_true')
to_parser.add_argument('-a', dest='all_group', action='store_true')
to_parser.add_argument('-b', dest='ban', action='store_true')


@to_cmd.handle()
async def first_receive(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state['args'] = msg


@to_cmd.got('args', __doc__)
async def _(bot: Bot, state: T_State):
    args = state['args'].split(None, 1)
    if args[0] == state['_prefix']['raw_command']:
        args = args[1].split(None, 1)

    try:
        cmd = to_parser.parse_args([args[0]])
    except Exception as e:
        await to_cmd.finish('命令解析失败' + str(e))
        return

    if args[0] == args[-1]:
        await to_cmd.reject('命令缺少[args,]\n' + __doc__)
    param = args[-1]

    if cmd.help:
        await to_cmd.reject(__doc__)
    elif cmd.finish:
        await to_cmd.finish('本次命令结束')

    if cmd.several:
        qq_list = list(gen_qq(param))
        if cmd.to_user:
            for qq in qq_list[:-1]:
                await bot.send_private_msg(user_id=qq, message=unescape(qq_list[-1]))
        elif cmd.to_group:
            for qq in qq_list[:-1]:
                await bot.send_group_msg(group_id=qq, message=unescape(qq_list[-1]))
    elif cmd.all_group:
        group_list = await get_group_id_list(bot)
        if cmd.ban:
            qq_list = list(gen_qq(param))
            for qq in (i for i in group_list if i not in qq_list):
                await bot.send_group_msg(group_id=qq, message=unescape(qq_list[-1]))
        else:
            for qq in group_list:
                await bot.send_group_msg(group_id=qq, message=unescape(param))
    elif cmd.to_user:
        params = param.split(None, 1)
        if params[0] == params[-1]:
            await to_cmd.reject('缺少需要发送的消息\n' + __doc__)
        else:
            await bot.send_private_msg(user_id=params[0], message=unescape(params[1]))
    elif cmd.to_group:
        params = param.split(None, 1)
        if params[0] == params[-1]:
            await to_cmd.reject('缺少需要发送的消息\n' + __doc__)
        else:
            await bot.send_group_msg(group_id=params[0], message=unescape(params[1]))

    await to_cmd.finish(Message('[CQ:face,id=124]'))
