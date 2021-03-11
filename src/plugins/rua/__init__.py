import re

from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from .data_source import get_avatar, generate_gif


rua_cmd = on_command('rua', aliases={'搓', })


@rua_cmd.handle()
async def creep(bot: Bot, event: MessageEvent):
    creep_id = event.user_id

    match = re.findall(r'\[CQ:at,qq=(.+?)\]', event.raw_message)
    if match:
        creep_id = match[0]

    avatar = await get_avatar(creep_id)

    output = generate_gif(avatar)

    await bot.send(event, message=Message(MessageSegment.image(file='file://' + output)))
