import re


def parse_cmd(pattern, msg: str) -> list:
    return re.findall(pattern, msg, re.S)


def parse_at(msg: str) -> str:
    return re.sub(r'/at(\d+)', r'[CQ:at,qq=\1]', msg)


def parse_self(msg: str, **kwargs) -> str:
    return parse_at_self(re.sub(r'/self', str(kwargs.get('nickname', '')), msg), **kwargs)


def parse_at_self(msg: str, **kwargs) -> str:
    qq = kwargs.get('sender_id', '')
    if qq:
        return re.sub(r'/atself', f"[CQ:at,qq={qq}]", msg)
    else:
        return msg


def parse(msg, **kwargs):
    return parse_at(parse_self(msg, **kwargs))
