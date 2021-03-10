import time

from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent

from .data_source import get_wm_item, get_rm_item, get_wiki_item

message_cache = dict()

wm_plugin = on_command('wm')
rm_plugin = on_command('rm')
wiki_plugin = on_command('wiki')


@wm_plugin.handle()
async def _(bot: Bot, event: MessageEvent):
    item = str(event.message).strip()
    if item:
        msg = await get_wm_item(item)
        msg_id = await bot.send(event, message=msg)

        if isinstance(event, GroupMessageEvent):
            group_id = str(event.group_id)
            if message_cache.get(group_id, []):
                message_cache[group_id].append((msg_id, time.time()))
            else:
                message_cache[group_id] = [(msg_id, time.time())]

    else:
        await bot.send(event, message='指令格式：wm 物品名')


@rm_plugin.handle()
async def _(bot: Bot, event: MessageEvent):
    item = str(event.message).strip()
    if item:
        msg = await get_rm_item(item)
        msg_id = await bot.send(event, message=msg)

        if isinstance(event, GroupMessageEvent):
            group_id = str(event.group_id)
            if message_cache.get(group_id, []):
                message_cache[group_id].append((msg_id, time.time()))
            else:
                message_cache[group_id] = [(msg_id, time.time())]
    else:
        await bot.send(event, message='指令格式：rm 物品名')


@wiki_plugin.handle()
async def _(bot: Bot, event: MessageEvent):
    item = str(event.message).strip()

    if item:
        msg = await get_wiki_item(item)
        msg_id = await bot.send(event, message=msg)

        if isinstance(event, GroupMessageEvent):
            group_id = str(event.group_id)
            if message_cache.get(group_id, []):
                message_cache[group_id].append((msg_id, time.time()))
            else:
                message_cache[group_id] = [(msg_id, time.time())]
    else:
        await bot.send(event, message='指令格式：wiki 物品名')


delete_msg = on_command('撤回！', aliases={'撤回!',}, priority=10)

@delete_msg.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    global message_cache
    try:
        msg_id, int_time = message_cache[str(event.group_id)].pop()

        if (time.time()-int_time) < 180:

            await bot.call_api('delete_msg', message_id=int(msg_id['message_id']))
            await bot.send(event, message='你吼辣么大声干嘛！')
    except:
        pass
    # else:
    #     await bot.send(event, message='三分钟了，撤回不了了！')
