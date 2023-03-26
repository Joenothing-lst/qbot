from nonebot import on_message
# from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.adapters.cqhttp.utils import unescape

from .data_source import chat, is_user

chatgpt = on_message(priority=98, block=False)


@chatgpt.handle()
async def _(bot: Bot, event: MessageEvent):
    if event.to_me:
        token = bot.config.personal_api_key
        uid = event.user_id
        msg = unescape(str(event.message))
        if any(i in msg for i in ['assistant', 'vanilla', 'makise', 'pcr_kokoro']):
            reply = chat(token, uid, msg)
            await bot.send(event, Message(reply))

        elif is_user(token, uid):
            reply = chat(token, uid, msg)
            reply_msg = MessageSegment.text(reply)
            if event.message_type == 'group':
                reply_msg = MessageSegment.reply(event.message_id) + reply_msg
            await bot.send(event, reply_msg)
