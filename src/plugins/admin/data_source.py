from nonebot.adapters.cqhttp.bot import Bot


async def get_group_id_list(bot: Bot):
    group_list = await bot.get_group_list()
    return [i['group_id'] for i in group_list]


def gen_qq(msg: str):
    data = msg.lstrip().split(' ', 1)
    while data[0].isdigit() and 6 < len(data[0]) < 12:
        yield int(data[0])
        data = data[1].lstrip().split(' ', 1)
    yield ' '.join(data)
