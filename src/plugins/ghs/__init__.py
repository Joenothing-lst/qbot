# import time

# from nonebot import on_command
# from nonebot.adapters.cqhttp.bot import Bot
# from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent

# from .data_source import search_r18book


# message_cache = {}

# r18book = on_command('搜本子')

# @r18book.handle()
# async def _(bot: Bot, event: MessageEvent):
#     params = str(event.message)
#     books = search_r18book(params)
#     msg = f'找到关键词 【{params}】的本子：'
#     msg = msg + '\n'.join(f"\n名称：{book['name']}\n链接：{book['link']}\n封面：{book['faceimg']}" for book in books)
#     msg_id = await bot.send(event, msg)

#     if isinstance(event, GroupMessageEvent):
#         group_id = str(event.group_id)
#         if message_cache.get(group_id, []):
#             message_cache[group_id].append((msg_id, time.time()))
#         else:
#             message_cache[group_id] = [(msg_id, time.time())]



# delete_msg = on_command('撤回！', aliases={'撤回!',})

# @delete_msg.handle()
# async def _(bot: Bot, event: GroupMessageEvent):
#     global message_cache

#     try:
#         msg_id, int_time = message_cache[str(event.group_id)].pop()

#         if (time.time()-int_time) < 180:

#             await bot.call_api('delete_msg', message_id=int(msg_id['message_id']))
#             await bot.send(event, message='你吼辣么大声干嘛！')
#     except Exception as e:
#         pass