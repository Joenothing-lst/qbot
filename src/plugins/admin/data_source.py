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


def gentracker(randnum: float, type: int=0) -> str:
    if type == 1:
        return f'[CQ:json,data={{"config":{{"height":0&#44;"ctime":1145141919810&#44;"forward":1&#44;"width":0&#44;"token":"1968c4a19912e09af1e9331f9c3b8209"&#44;"type":"normal"&#44;"autoSize":0}}&#44;"prompt":"&#91;QQ小程序&#93;群援交"&#44;"app":"com.tencent.miniapp_01"&#44;"ver":"0.0.0.1"&#44;"view":"view_8C8E89B49BE609866298ADDFF2DBABA4"&#44;"meta":{{"detail_1":{{"shareTemplateData":{{}}&#44;"scene":1036&#44;"appid":""&#44;"desc":"群主开启了群援交，快来一起加入吧！"&#44;"preview":"http:\/\/159.75.88.21\/download\/20180619050109.jpg"&#44;"title":"群援交"&#44;"shareTemplateId":"8C8E89B49BE609866298ADDFF2DBABA4"&#44;"icon":"https:\/\/img.yanlutong.com\/uploadimg\/ico\/2020\/0923\/1600845864171401.png?q={randnum}"&#44;"url":"y.music.163.com\/m\/song\/561493928\/?userid=1584345022&amp;app_version=8.0.00"}}}}&#44;"desc":"群援交"}}]'

    return f'[CQ:music,type=custom,audio=http://music.163.com/song/media/outer/url?id=1809741562,image=http://159.75.88.21/download/jpg1.jpg?q={randnum},title=YOASOBI-優しい彗星 (TV动画《BEASTARS》第二季片尾曲)]'