import requests


def chat(token, uid, str):
    url = f"http://127.0.0.1/OpenaiApi/chatgpt/chat?token={token}&uid={uid}&message={str}"
    res = requests.get(url).json()

    if res['code'] == 200:
        return res['data']['message']
    else:
        return res['msg']


def is_user_living(token, uid):
    url = f"http://127.0.0.1/OpenaiApi/chatgpt/is_user_living?token={token}&uid={uid}"
    res = requests.get(url).json()

    if res['code'] == 200:
        return res['data']['is_user_living']
    else:
        return res['msg']


def set_user_living(token, uid):
    url = f"http://127.0.0.1/OpenaiApi/chatgpt/set_user_living?token={token}&uid={uid}&is_living=1"
    res = requests.get(url).json()

    if res['code'] == 200:
        return res['msg']
    else:
        return res['msg']


def clean_context(token, uid):
    url = f"http://127.0.0.1/OpenaiApi/chatgpt/clean_context?token={token}&uid={uid}"
    res = requests.get(url).json()

    if res['code'] == 200:
        return res['msg']
    else:
        return res['msg']
