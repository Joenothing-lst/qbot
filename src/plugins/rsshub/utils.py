from typing import Union

from nonebot.log import logger
from src.utils.util import get_bot


async def safe_send(send_type: str, receivers: Union[str, int, list], message):
    """
    发送出现错误时, 尝试重新发送, 并捕获异常且不会中断运行

    :param send_type: private / group, 对应私聊/群聊
    :param _id: 接收者 id
    :param message: 发送的消息
    :return:
    """
    try:
        bot = get_bot()

        if not isinstance(receivers, list):
            receivers = [receivers]

        for id_ in receivers:
            return await bot.call_api(f'send_{send_type}_msg', **{
                'message': message,
                'user_id' if send_type == 'private' else 'group_id': id_
            })

    except Exception as e:
        logger.error(f"推送失败（网络错误），错误信息：{e}")
