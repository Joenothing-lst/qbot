import asyncio
from typing import Any

from src.utils.util import get_bot

bot = get_bot()


async def wrapper(api: str, params: dict):
    await bot.call_api(api, **params)

async def call_api_delay(api: str, delay: float, **params):
    loop = asyncio.get_running_loop()
    loop.call_later(delay, wrapper, api, params)

async def set_async_delay(func: Any, delay: int=15, **kwargs):
    await sleep(delay)
    return await func(**kwargs)