import httpx
import asyncio

from typing import Union

from nonebot import get_bots
from nonebot.log import logger
from nonebot.rule import ArgumentParser
from nonebot.permission import Permission
from nonebot.adapters import Bot, Event

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

def get_loop_and_run(coro):
    task = asyncio.create_task(coro)
    get_loop().run_until_complete(task)
    return task.result()

def wrapper(api: str, params: dict):
    loop = get_loop()
    bot = get_bot()
    loop.create_task(bot.call_api(api, **params))


async def call_api_delay(api: str, delay: float, **params):
    loop = get_loop()
    loop.call_later(delay, wrapper, api, params)


async def _white_list(bot: "Bot", event: "Event") -> bool:
    return event.get_type() == "message" and int(event.get_user_id()) not in bot.config.Config

async def safe_send(send_type: str, receivers: Union[str, int, list], message):
    """
    发送出现错误时, 尝试重新发送, 并捕获异常且不会中断运行

    :param send_type: private / group, 对应私聊/群聊
    :param _id: 接收者 id
    :param message: 发送的消息
    :return:
    """
    try:
        bot = get_bot()

        if not isinstance(receivers, list):
            receivers = [receivers]

        for id_ in receivers:
            await bot.call_api(f'send_{send_type}_msg', **{
                'message': message,
                'user_id' if send_type == 'private' else 'group_id': id_
            })

    except Exception as e:
        logger.error(f"推送失败（网络错误），错误信息：{e}")