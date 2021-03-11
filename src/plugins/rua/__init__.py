import re

from nonebot import require, on_command, on_message, on_keyword, on_shell_command, on_request
from nonebot.rule import command
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State, T_Handler
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.adapters.cqhttp.event import MessageEvent, GroupRequestEvent
from nonebot.adapters.cqhttp.permission import PRIVATE, GROUP
from nonebot.adapters.cqhttp.utils import unescape, escape

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

    await bot.send(event, message=Message(MessageSegment.image(file=output)))
