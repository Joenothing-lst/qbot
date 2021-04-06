import random

from nonebot import require, on_command, on_message, on_keyword, on_shell_command, on_request
from nonebot.rule import command
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State,T_Handler
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.message import Message
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent, GroupRequestEvent
from nonebot.adapters.cqhttp.permission import PRIVATE, GROUP
from nonebot.adapters.cqhttp.utils import unescape, escape

from src.utils.util import gen_parser
from .data_source import get_group_id_list, gen_qq, gentracker


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


request_cmd = on_request()


@request_cmd.handle()
async def request(bot: Bot, event: GroupRequestEvent):
    f_group = event.group_id
    f_user = event.user_id
    if event.sub_type == 'invite':

        result = request_cmd.new("message",
                                 permission=SUPERUSER,
                                 temp=True,
                                 priority=5)

        await bot.send_private_msg(user_id=912871833,
                                   message=f'有新的群邀请:\n群：{f_group}\n邀请人：{f_user}\n')

        request_event = event

        @result.handle()
        async def _(bot: Bot, event: MessageEvent):
            msg = 'reject'
            if 'y' or '1' in str(event.message):
                msg = 'approve'
                await request_event.approve(bot)
            else:
                await request_event.reject(bot)

            await result.finish(msg)


call_api = on_command('api', aliases={'call'}, permission=SUPERUSER)

@call_api.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = str(event.message).split()
    param = event.dict()

    if msg:
        api, *params = msg

        param.update(dict(i.split('=') for i in params))

        res = await bot.call_api(api, **param)
        if res:
            await call_api.finish(message=Message(str(res)))


iptracker = on_command('iptracker', permission=SUPERUSER)

@iptracker.handle()
async def _(bot: Bot, event: MessageEvent):
    type_ = str(event.message)
    randnum = random.random()
    await bot.send(event, message=str(randnum))
    await iptracker.finish(message=Message(gentracker(randnum, type=int(type_) if type_ else 0)))


show_me = on_keyword({'闪光弹', '照明弹'}, permission=SUPERUSER)

@show_me.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if 'reply' in event.raw_message:
        msg = event.reply.raw_message.replace(',type=flash', '')
        await bot.send(event, Message(msg))


temp = """<section style="text-align: center; line-height: 1.75em; margin-left: 8px; margin-right: 8px;">
    <section style="margin-right: auto;margin-left: auto;width: 100%;vertical-align: middle;display: inline-block;line-height: 0;box-sizing: border-box;">
        <section style="display: inline-block;width: 100%;vertical-align: top;background-position: 0% 0%;background-repeat: no-repeat;background-size: 100%;background-attachment: scroll;background-image: url(&quot;{url2}&quot;);-webkit-tap-highlight-color: transparent;">
            <svg enable-background="new 0 0 1080 435" space="preserve"
                style="display: inline-block;width: 100%;vertical-align: top;background-position: 0% 0%;background-repeat: no-repeat;background-size: 100%;background-attachment: scroll;background-image: url(&quot;{url1}&quot;);-webkit-tap-highlight-color:transparent;"
                version="1.1" viewBox="0 0 1080 435" x="0px" xlink="http://www.w3.org/1999/xlink" xml=""
                xmlns="http://www.w3.org/2000/svg" y="0px">
                <animate attributeName="opacity" begin="click" dur="0.5s" values="1;0" fill="freeze" restart="never"></animate>
            </svg>
        </section>
    </section>
</section>"""

merge_cmd = on_command('代码')

@merge_cmd.handle()
async def _(bot: Bot, event: MessageEvent):
    try:
        url1, url2 = event.message.__str__().split()
        await bot.send(event, message=temp.format(url1=url1, url2=url2))
    except:
        print('error')

# request_cmd = on_message(permission=PRIVATE)
#
#
# @request_cmd.handle()
# async def request(bot: Bot, event: MessageEvent):
#     # 接收私聊消息
#     f_user = event.user_id
#     if True:
#         # 创建临时 matcher
#         request_cmd.new("message",
#                         handlers=[decide],
#                         permission=SUPERUSER,
#                         temp=True)
#
#         await bot.send_private_msg(user_id=912871833,
#                                    message=f'{f_user}:\n{event.raw_message}')
#
#
# async def decide(bot: Bot, event: MessageEvent):
#     # 临时 matcher 响应事件
#     await request_cmd.send(message=event.message)
