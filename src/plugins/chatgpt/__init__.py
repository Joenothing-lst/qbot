from nonebot import on_message
# from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.adapters.cqhttp.utils import unescape

from .data_source import chat, is_user_living, set_user_living, clean_context

chatgpt = on_message(priority=98, block=False)


@chatgpt.handle()
async def _(bot: Bot, event: MessageEvent):
    token = bot.config.personal_api_key
    uid = event.user_id
    msg = unescape(str(event.message))
    if event.to_me and any(i in msg for i in ['assistant', 'vanilla', 'makise', 'pcr_kokoro']):
        # 创建用户/角色
        reply = chat(token, uid, msg)
        await bot.send(event, Message(reply))

    elif '结束对话' in msg:
        # 结束用户的对话
        if clean_context(token, uid) == 'success':
            await bot.send(event, 'OK~')

    elif event.to_me or is_user_living(token, uid):
        reply = chat(token, uid, msg)
        if event.to_me:
            set_user_living(token, uid)
        reply_msg = MessageSegment.text(reply)
        if event.message_type == 'group':
            reply_msg = MessageSegment.reply(event.message_id) + reply_msg
        await bot.send(event, reply_msg)
