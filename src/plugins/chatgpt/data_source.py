import requests


def chat(token, uid, str):
    url = f"http://127.0.0.1/OpenaiApi/chatgpt/chat?token={token}&uid={uid}&message={str}"
    res = requests.get(url).json()

    if res['code'] == 200:
        return res['data']['message']
    else:
        return res['msg']
