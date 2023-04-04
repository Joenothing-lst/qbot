from nonebot import on_message, on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.adapters.cqhttp.utils import unescape
from nonebot.permission import SUPERUSER

from .data_source import chat, is_user, is_user_living, set_user_living

PLUGIN_ON = False

chatgpt = on_message(priority=98, block=False)


@chatgpt.handle()
async def _(bot: Bot, event: MessageEvent):
    if PLUGIN_ON:
        token = bot.config.personal_api_key
        uid = event.user_id
        msg = unescape(str(event.get_plaintext()))
        if msg:
            if event.to_me and any(i in msg for i in ['assistant', 'vanilla', 'makise', 'pcr_kokoro']):
                # 创建用户/角色
                reply = chat(token, uid, msg)
                await bot.send(event, Message(reply))

            elif '结束对话' in msg:
                # 结束用户的对话
                if set_user_living(token, uid, False) == 'success':
                    await bot.send(event, 'OK~')

            elif is_user(token, uid):
                if event.to_me or is_user_living(token, uid):
                    reply = chat(token, uid, msg)
                    if event.to_me:
                        set_user_living(token, uid)
                    reply_msg = MessageSegment.text(reply)
                    if event.message_type == 'group':
                        reply_msg = MessageSegment.reply(event.message_id) + reply_msg
                    await bot.send(event, reply_msg)


chatgpt_turn = on_command('chatgpt', permission=SUPERUSER)


@chatgpt_turn.handle()
async def turn(bot: Bot, event: MessageEvent):
    global PLUGIN_ON
    msg = unescape(str(event.message))

    if 'on' in msg:
        PLUGIN_ON = True
        await bot.send(event, '插件已开启')
    elif 'off' in msg:
        PLUGIN_ON = False
        await bot.send(event, '插件已关闭')
