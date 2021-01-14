from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent

from .data_source import get_wm_item, get_rm_item, get_wiki_item

wm_plugin = on_command('wm')
rm_plugin = on_command('rm')
wiki_plugin = on_command('wiki')

@wm_plugin.handle()
async def _(bot: Bot, event: MessageEvent):
    item = str(event.message).strip()
    if item:
        msg = await get_wm_item(item)
        await bot.send(event, message=msg)
    else:
        await bot.send(event, message='指令格式：wm 物品名')

@rm_plugin.handle()
async def _(bot: Bot, event: MessageEvent):
    item = str(event.message).strip()
    if item:
        msg = await get_rm_item(item)
        await bot.send(event, message=msg)
    else:
        await bot.send(event, message='指令格式：rm 物品名')

@wiki_plugin.handle()
async def _(bot: Bot, event: MessageEvent):
    item = str(event.message).strip()
    if item:
        msg = await get_wiki_item(item)
        await bot.send(event, message=msg)
    else:
        await bot.send(event, message='指令格式：wiki 物品名')

