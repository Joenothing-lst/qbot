import requests


def chat(token, uid, str):
    url = f"http://127.0.0.1/OpenaiApi/chatgpt/chat?token={token}&uid={uid}&message={str}"
    res = requests.get(url).json()

    if res['code'] == 200:
        return res['data']['message']
    else:
        return res['msg']


def is_user(token, uid):
    url = f"http://127.0.0.1/OpenaiApi/chatgpt/is_user?token={token}&uid={uid}"
    res = requests.get(url).json()

    if res['code'] == 200:
        return res['data']['is_user']
    else:
        return res['msg']
