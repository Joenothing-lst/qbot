from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent
import re
from nonebot.log import logger

fuck = on_command('fake', aliases={'伪造'}, permission=SUPERUSER, priority=5)

@fuck.handle()
async def handle_first_receive(bot: Bot, event: MessageEvent, state: dict):
    if not isinstance(event, GroupMessageEvent):
        await fuck.send('仅在群聊中有效！')
        return
    args = str(event.message).strip()
    if args:
        state["fuck"] = args  # 如果用户发送了参数则直接赋值



@fuck.got("fuck")
async def handle_RssAdd(bot: Bot, event: MessageEvent, state: dict):
    if not isinstance(event, GroupMessageEvent):
        await fuck.send('仅在群聊中有效！')
        return
    msg_info = state["fuck"]
    try:
        msg = await fuck_forward(msg_info, event.group_id, bot)
        await bot.call_api('send_group_forward_msg', group_id=msg['group_id'], messages=msg['messages'])
    except Exception as e:
        await fuck.send('参数有误！E: {}'.format(e))
        logger.error('参数有误！E: {}'.format(e))

# 仅仅在群聊中有效
# 触发：(bot昵称)|(@bot) fuck
# 使用方法: (QQ号)|(@某人) [自定义昵称]%第一条消息[~第二条消息]
# % 后表示消息
# 消息用 ~ 分割
async def fuck_forward(message, group_id, bot):
    msg = []
    message = message.replace("&amp;", "&") \
        .replace("&#91;", "[") \
        .replace("&#93;", "]") \
        .replace("&#44;", ",")
    message_list = message.split('$', 1)
    contents = re.findall('^(?:\[CQ:at,qq=)?(\d{5,})(?:])?([^|]+)?', message_list[0]) #=([^|]+)(?:\|)?$

    for con in contents:
        user=int(con[0])
        try:
            info = await bot.call_api('get_group_member_info',group_id=group_id,user_id=user,no_cache=True)
        except:
            info=await bot.call_api('get_stranger_info',user_id=user,no_cache=True)
        if not con[1].strip() or con[1]=='':
            nickname=info['nickname']
            try:
                if info['card']:
                    nickname=info['card']
            except:
                pass
        else:
            nickname=con[1].strip()
        content = message_list[1]
        msg_list = content.split('&')
        for msg_tmp in msg_list:
            node = {"type": "node",
                    "data": {"name": nickname,
                             "uin": str(user),
                             "content": msg_tmp
                             }
                    }
            msg.append(node)
    if msg:
        return {'group_id': group_id,
                'messages': msg
                }
    else:
        return None