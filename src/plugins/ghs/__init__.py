from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent
from nonebot.adapters.cqhttp.utils import unescape, escape
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from src.utils.util import call_api_delay
from .data_source import search_r18book, Book, gen_forward_message, search_mag, get_mag

r18book_search = on_command('搜本子',
                            aliases={'找本子', },
                            permission=SUPERUSER
                            )


@r18book_search.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    params = unescape(str(event.message))

    books = search_r18book(params)
    msg = f'找到关键词【{params}】的本子'

    forward_msg = gen_forward_message(
        [msg] + [f"id：{book['book_id']}\n名称：{book['title']}\n{MessageSegment.image(file=book['cover'])}" for book in
                 books],
        event.sender.user_id)

    print(forward_msg)

    msg_id = await bot.call_api('send_group_forward_msg', group_id=event.group_id, messages=Message(forward_msg))

    await call_api_delay(api='delete_msg', delay=30, message_id=msg_id.get('message_id'))


r18book_view = on_command('看本子',
                          permission=SUPERUSER
                          )


@r18book_view.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    params = unescape(str(event.message))
    try:
        book = Book(params)
    except:
        await bot.send(event, message='没找到  爬')
        return

    msg_list = gen_forward_message([MessageSegment.image(file=page.image_url) for page in book.pages],
                              event.sender.user_id)

    msg = (msg_list[i:i+5] for i in range(0,len(msg_list),5))

    await bot.send(event, message='找到惹！请稍等')

    split = True

    try:
        if split:
            for i in msg:
                await bot.call_api('send_group_forward_msg', group_id=event.group_id, messages=Message(i))
        else:
            await bot.call_api('send_group_forward_msg', group_id=event.group_id, messages=Message(msg_list))
    except:
        await bot.send(event, message='歪日  被口了发不出来')


search_mag_cmd = on_command('搜番号', aliases={'找番号', '番号'})

@search_mag_cmd.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    params = unescape(str(event.message))

    r = await search_mag(params)
    l = len(r)

    if l == 0:
        await search_mag_cmd.finish(f'没找到{params}  爬')
    elif l == 1:
        msg = await get_mag(r[0].get('link'))
        await search_mag_cmd.finish(msg)
    else:
        state['results'] = r
        msg = '找到以下结果：' + '\n'.join(f"\n{i+1}、{r[i]['title']}\n热度【{r[i]['hot']}】\n日期：{r[i]['date']} 大小：{r[i]['size']}" for i in range(l))
        await bot.send(event, msg)


@search_mag_cmd.got('index', '是编号几？')
async def _(bot: Bot, event: MessageEvent, state: T_State):
    params = unescape(str(event.message))

    msg = await get_mag(state['index'][int(params)-1].get('link'))

    await bot.send(event, msg)
