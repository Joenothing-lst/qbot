import re


def parse_at(msg:str) -> str:
    return re.sub('at(\d+)', r'[CQ:at,qq=\1]', msg)

def parse_cmd(pattern, msg:str) -> list:
    return re.findall(pattern, msg, re.S)

