from nonebot.adapters.cqhttp.bot import Bot

async def get_group_id_list(bot: Bot):
    group_list = await bot.get_group_list()
    return [i['group_id'] for i in group_list]