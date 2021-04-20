import re
from datetime import datetime

from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from .data_source import get_data, get_hot


qid_dict = {"今天是什么少女": 162207, "异世界转生": 587874, "性格": 567341, "马娘相性": 1059404, "卖萌": 360578, "热门测试": 000000}
date = True  # 是否令日期影响结果（测试结果每天不一样）


shidan_cmd = on_command('shindan', aliases=set(qid_dict.keys()))

@shidan_cmd.handle()
async def on_input_new(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = event.raw_message
    match = re.findall(r'\[CQ:at,qq=(.+?)\]', msg)
    name = event.sender.card or event.sender.nickname

    if match:
        user = match[0]
        try:
            info = await bot.call_api('get_group_member_info', group_id=event.group_id, user_id=user, no_cache=True)
            name = info.get('card') or info.get('nickname')
        except:
            pass

    if date:
        now = datetime.now()
        rn = f"{name} {now.year}-{now.month}-{now.day}"
    else:
        rn = name

    if msg[:4] == "热门测试":

        top_index = int(msg[4:6]) if msg[4:] else 0

        text_list, b64s = await get_hot(top_index, name)

        remsg = Message(text_list.replace(rn, name))
        for item in b64s:
            remsg += MessageSegment.image(file=item)
        await bot.send(event, Message(remsg))

    elif msg in qid_dict:

        text_list, b64s = await get_data(qid_dict[msg], name)

        remsg = Message(text_list.replace(rn, name))
        for item in b64s:
            remsg += MessageSegment.image(file=item)
        await bot.send(event, Message(remsg))

