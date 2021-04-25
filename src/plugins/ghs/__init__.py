from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent
from nonebot.adapters.cqhttp.utils import unescape, escape
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from src.utils.util import call_api_delay
from .data_source import search_r18book, Book, gen_forward_message


r18book_search = on_command('搜本子', aliases={'找本子',})

@r18book_search.handle()
async def _(bot: Bot, event: MessageEvent):
    params = unescape(str(event.message))
    
    books = search_r18book(params)
    msg = f'找到关键词 【{params}】的本子：'
    msg = msg + '\n'.join(f"\nid：{book['book_id']}\n名称：{book['title']}" for book in books)

    msg_id = await bot.send(event, msg)

    await call_api_delay(api='delete_msg', delay=30, message_id=msg_id.get('message_id'))


r18book_view = on_command('看本子')

@r18book_view.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    params = unescape(str(event.message))
    book = Book(params)
    msg = gen_forward_message([MessageSegment.image(file=page.image_url) for page in book.pages],
                              event.sender.user_id)

    await bot.call_api('send_group_forward_msg', group_id=event.group_id, messages=Message(msg))
