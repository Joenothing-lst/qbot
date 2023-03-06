from nonebot import on_message
# from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent
from nonebot.adapters.cqhttp.utils import unescape, escape
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from .data_source import chat



chatgpt = on_message()


@chatgpt.handle()
async def _(bot: Bot, event: MessageEvent):
    if event.to_me:
        print(bot.config.__dict__)
        token = bot.config.personal_api_key
        uid = event.user_id
        msg = unescape(str(event.message))
        print(token, uid, msg)
        reply = chat(token, uid, msg)
        # await bot.send(event, Message(reply))

