from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent

from .data_source import get_wf_item, get_wm_item, get_rm_item, get_wiki_item
from .util import set_async_delay, call_api_delay

wf_plugin = on_command('wf ')
wm_plugin = on_command('wm ')
rm_plugin = on_command('rm ')
wiki_plugin = on_command('wiki ')


@wf_plugin.handle()
async def _(bot: Bot, event: MessageEvent):
    item = str(event.message).strip()
    if item:
        msg = await get_wf_item(item)
        msg_id = await bot.send(event, message=msg + '\n消息将于15秒后撤回')

        await call_api_delay(api='delete_msg', delay=15, message_id=msg_id.get('message_id'))

        if isinstance(event, GroupMessageEvent):
            try:
                await bot.set_group_ban(group_id=event.group_id, user_id=event.sender.user_id, duration=5)
            except:
                pass

    else:
        await bot.send(event, message='指令格式：wf 要查询的世界状态')


@wm_plugin.handle()
async def _(bot: Bot, event: MessageEvent):
    item = str(event.message).strip()
    if item:
        msg = await get_wm_item(item)
        msg_id = await bot.send(event, message=msg + '\n消息将于15秒后撤回')

        await call_api_delay(api='delete_msg', delay=15, message_id=msg_id.get('message_id'))

        if isinstance(event, GroupMessageEvent):
            try:
                await bot.set_group_ban(group_id=event.group_id, user_id=event.sender.user_id, duration=5)
            except:
                pass

    else:
        await bot.send(event, message='指令格式：wm 物品名')


@rm_plugin.handle()
async def _(bot: Bot, event: MessageEvent):
    item = str(event.message).strip()
    if item:
        msg = await get_rm_item(item)
        msg_id = await bot.send(event, message=msg + '\n消息将于15秒后撤回')

        await call_api_delay(api='delete_msg', delay=15, message_id=msg_id.get('message_id'))

        if isinstance(event, GroupMessageEvent):
            try:
                await bot.set_group_ban(group_id=event.group_id, user_id=event.sender.user_id, duration=5)
            except:
                pass

    else:
        await bot.send(event, message='指令格式：rm 物品名')


@wiki_plugin.handle()
async def _(bot: Bot, event: MessageEvent):
    item = str(event.message).strip()
    if item:
        msg = await get_wiki_item(item)
        msg_id = await bot.send(event, message=msg + '\n消息将于15秒后撤回')

        await call_api_delay(api='delete_msg', delay=15, message_id=msg_id.get('message_id'))

        if isinstance(event, GroupMessageEvent):
            try:
                await bot.set_group_ban(group_id=event.group_id, user_id=event.sender.user_id, duration=5)
            except:
                pass

    else:
        await bot.send(event, message='指令格式：wiki 物品名')
