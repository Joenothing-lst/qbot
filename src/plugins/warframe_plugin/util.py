import asyncio
from typing import Any

from src.utils.util import get_bot


def get_loop():
    return asyncio.get_running_loop()


def wrapper(api: str, params: dict):
    loop = get_loop()
    bot = get_bot()
    loop.create_task(bot.call_api(api, **params))


async def call_api_delay(api: str, delay: float, **params):
    loop = get_loop()
    loop.call_later(delay, wrapper, api, params)


async def set_async_delay(func: Any, delay: int=15, **kwargs):
    await asyncio.sleep(delay)
    return await func(**kwargs)