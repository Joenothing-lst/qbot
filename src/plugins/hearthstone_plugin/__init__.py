import re

from nonebot import on_message, on_command
from nonebot.rule import Rule
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters import Event
from nonebot.adapters import Bot as BaseBot
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.message import Message
from nonebot.adapters.cqhttp.event import MessageEvent

from .data_source import HSHandle

hs = HSHandle()


def check_base64() -> Rule:
    async def _check_base64(bot: BaseBot, event: Event, state: T_State) -> bool:
        msg = str(event.get_message())
        p = '^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$'
        try:
            return True if re.match(p, msg) else False

        except Exception:
            return False

    return Rule(_check_base64)


hs_api = on_message(rule=check_base64(), permission=SUPERUSER)


@hs_api.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = str(event.message)
    try:
        data, hero, format_type = hs.get_deck_from_deckstring(msg)
        msg = f"{format_type}模式\n{hero}\n" + '\n'.join(f"{v} * {k}" for _, k, v in data)
        await bot.send(event, Message(msg))
    except:
        pass