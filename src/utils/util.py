import httpx
import asyncio

from nonebot import get_bots
from nonebot.rule import ArgumentParser


def get_bot():
    if get_bots():
        return list(get_bots().values())[0]


async def async_request(method: str, url: str, **kwargs):
    async with httpx.AsyncClient() as client:
        result = await client.request(method.upper(), url, **kwargs)
        return result


base_parser = ArgumentParser(add_help=False)

base_parser.add_argument('-f', dest='finish', action='store_const', const=True, default=False)
base_parser.add_argument('-h', dest='help', action='store_true', default=False)


def gen_parser():
    return ArgumentParser(add_help=False, parents=[base_parser])


def get_loop():
    return asyncio.get_running_loop()


def wrapper(api: str, params: dict):
    loop = get_loop()
    bot = get_bot()
    loop.create_task(bot.call_api(api, **params))


async def call_api_delay(api: str, delay: float, **params):
    loop = get_loop()
    loop.call_later(delay, wrapper, api, params)