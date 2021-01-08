from nonebot import get_bots


def get_bot():
    if get_bots():
        return list(get_bots().values())[0]