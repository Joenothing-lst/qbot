from asyncio import sleep
from typing import Any


async def set_async_delay(func: Any, delay: int=15, **kwargs):
    await sleep(delay)
    await func(**kwargs)