import random
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


def gentracker(randnum: float) -> str:
    return f'[CQ:music,type=custom,audio=http://music.163.com/song/media/outer/url?id=1809741562,image=http://159.75.88.21/download/jpg1.jpg?q={randnum},title=YOASOBI-優しい彗星 (TV动画《BEASTARS》第二季片尾曲)]'