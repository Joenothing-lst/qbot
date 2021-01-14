import httpx

from nonebot import get_bots


def get_bot():
    if get_bots():
        return list(get_bots().values())[0]


async def async_request(method: str, url: str, **kwargs):
    async with httpx.AsyncClient() as client:
        result = await client.request(method.upper(), url, **kwargs)
        return result