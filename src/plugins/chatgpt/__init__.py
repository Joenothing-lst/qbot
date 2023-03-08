from nonebot import on_message
# from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent
from nonebot.adapters.cqhttp.utils import unescape, escape
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from .data_source import chat



chatgpt = on_message(priority=98, block=False)


@chatgpt.handle()
async def _(bot: Bot, event: MessageEvent):
    if event.to_me:
        token = bot.config.personal_api_key
        uid = event.user_id
        msg = unescape(str(event.message))
        reply = chat(token, uid, msg)
        await bot.send(event, Message(reply))

