from nonebot import get_driver, require
from src.utils import util
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

scheduler = require('nonebot_plugin_apscheduler').scheduler


@scheduler.scheduled_job('cron', hour='*/2') # = UTC+8 1445
async def get_up():
    try:
        bot = util.get_bot()
        await bot.send_private_msg(user_id='912871833', message='lst抱着你在你耳边说：再不做ppt就操你')
    except:
        pass
