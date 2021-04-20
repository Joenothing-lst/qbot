from collections import Generator
from typing import Callable, Dict
import bs4
import httpx
from lxml import etree
from bs4 import BeautifulSoup, NavigableString, Tag


async def async_request(method: str, url: str, **kwargs):
    async with httpx.AsyncClient() as client:
        result = await client.request(method.upper(), url, **kwargs)
        return result


async def get_data(qid, name):
    data = {"_token": "FBNybh2cb2nn83ogt0x4doW8gGJu7XLme6SKwN9t", "name": name, "hiddenName": "名無しのV"}
    headers = {
        'authority': 'shindanmaker.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://shindanmaker.com',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': f'https://shindanmaker.com/a/{qid}',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': '_session=TJJSW6QBfNHys4GzRcZNvB6vtebUytZSz10mawI6; _ga=GA1.2.426144989.1618896363; _gid=GA1.2.1675492437.1618896365; __gads=ID=50a74152db78a0e9:T=1618898328:S=ALNI_MYkDQsm1yKeuZ-pcmfwI5WrFPUaRA; XSRF-TOKEN=eyJpdiI6Iko4ZE05ZUczV2JjZ1JDYkt0THIyb2c9PSIsInZhbHVlIjoiMWVNVDJ3Y3V4V3ExRXdBdnpBdmRacFBUblBKOHYvUDNJQThycWlWejlYYytvOW5CMndBUjk1VEFaUHg5YWdBZ2dDR3hDVDZrYW9NZDVENnI2RWNUN1Zib2JFcUpOSHVOYTl5OXNDeFQyRUJ4Um9BYlNKWlhZcGN4Q2ZUNWw0WVQiLCJtYWMiOiJkOTkzMmE0MzQxODc0ZmQ0YWEzMWM3ODkyZjc3ZjQyZWZhZGIyNDQ5MDlmN2Y3YWYwYjE1MDRhYzU2OTU3ZDhlIn0%3D; _gat_UA-19089743-2=1; _gat_UA-19089743-3=1; trc_cookie_storage=taboola%2520global%253Auser-id%3Dbb72cc0f-feef-4fa1-aa73-43028ccda49c-tuct609849b',
    }
    # headers["Host"] = "shindanmaker.com"
    # headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"
    # headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    # headers["Accept-Language"] = "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"
    # headers["Accept-Encoding"] = "gzip, deflate, br"
    # headers["Content-Type"] = "application/x-www-form-urlencoded"
    # headers["Content-Length"] = "102"
    # headers["Origin"] = "https://shindanmaker.com"
    # headers["Connection"] = "keep-alive"
    # headers["Referer"] = f"https://shindanmaker.com/a/{qid}"
    # headers[
    #     "Cookie"
    # ] = "XSRF-TOKEN=eyJpdiI6IlVkZXJNV1ZXNkpGWHVqVlRQZHAvckE9PSIsInZhbHVlIjoicmxTVnhoSE9UTE1LL3YwT0l2dGNCamVQU2hVNVhCeEhUS0RGSitLdWlkdG5TMFVKRHduMncvU1U4NTZuMnlyS2UwYWw5bmZjR05QZTNJZmVsTUdRdlNyN05uR2ZaUmQwZmRsRnZKc1NvVnVNdzNWZzY3a3BKeVlqVHVSMUROMFAiLCJtYWMiOiI4YTlhODBmZjc0NGFhNjNhNWFkZDFjZTRmNmFjODE2NmQ3N2JkYzQ1ZDc4ZjA5YjRjMDZiODAxZDk1NmNiMDkxIn0%3D; _session=5QhNu0DKq15EeKVFZLsbV45cw3DlSm0QfHypx6K6; _ga=GA1.2.225182219.1618683607; _gid=GA1.2.838180010.1618683607; name=eyJpdiI6ImxhMGFZNlZHb3RiakJ0bW9zZnRtb3c9PSIsInZhbHVlIjoiaXVIUHFKNHJmYk1GYzlYdG9EaVJYQnJiRHZlMTlKL3JoS3J6WkJaeDgxZ1BUV2VFeUtrZmZoSTByeE5xcDhwaEdzSHlJNVNWeXllT29PanRIbUp4dWc9PSIsIm1hYyI6IjljZmQwZTcyYzc5ZjRjZDg3YWM5NDFiYmEwOGU2NzU4NGUzNTMzNDZlNTQwZWRhYjhiNWNiOWYxOGM3MTU2YTUifQ%3D%3D; dui=eyJpdiI6IlFUTDdRZlRCcDdjZ0xRRzk3ZkFuYXc9PSIsInZhbHVlIjoiMStDOElQaWkxVXNkN3NPS0NPbHZkcitUMitvWW1yYmh3amRMNHBWTVpUVTVCSWF2RUQ3NkxHQ0pyWExvRWdvY3J2VDVid0F2MDlIRVVKSWVjZU1iSVlTdkg3KzB3U1NWeFF1UXMrek8ydFhSSmkxYVNtci9DRVE5OWlYanEzdFlnckgwQlJQSnZKQ1h2UUo5YXRtQ3p3PT0iLCJtYWMiOiI1OGU3YjMyMWY5ZTA4MjBjZTlmM2M0YzQwODhhMmY5ZTU4ZWM0MTc0OGFkYmI2YjVhZTlmMDA2Mzg3YWY4OWU5In0%3D; dsr=eyJpdiI6InM1cG11L2swUWxMUmFRYURodXQveVE9PSIsInZhbHVlIjoiWWhZb3daZUVIVHMyaVRZZ1FLem4wcFZHWHdGWWk4d00raXVIMGwwVjRodURKem1TTEpiS3Ryd2tPV25QdXJ2R3Y4UDlXc3ZQcmdmUjUwVWQ0RjNON0E9PSIsIm1hYyI6ImVjZWJjOTIzYjg5Y2Q2MzVjOTY2MzNkMjNkN2RiNGM2NzM2ZTVjNmRhNGVlOWJiODY2MThlZjg4OTg4YTk3NTgifQ%3D%3D; trc_cookie_storage=taboola%2520global%253Auser-id%3D5279da13-8125-43ec-a4d9-1adcb79ce929-tuct774ac5d; cto_bundle=C3o9Xl90M0hyaHdZT1J4eGs2T3J2dHlBREhab3pDU2N4VEJjb0FFZGFTcXk1VlAzRmZaJTJGdW5vMmxmWkhBaElPSmI2bVIwcWZ4UEdBTkRWSTQzOUJzcHBLSk5seW83RUclMkZkU0twSkJKNlAxVWZQcThEWnJNYmhuRXhWVlZhSTZCTDRxajZkSjlRZ3VsVUdpZEFqVlhURCUyRnhuMEElM0QlM0Q; _gat_UA-19089743-2=1; _gat_UA-19089743-3=1"
    # headers["Upgrade-Insecure-Requests"] = "1"
    # headers["TE"] = "Trailers"
    url = f"https://shindanmaker.com/{qid}"
    resp = await async_request('post', url, headers=headers, data=data, timeout=10)
    html = etree.HTML(text=resp.text)
    imgs = html.xpath('//div[@id="shindanResult"]//img/@src')
    text = '診断結果\n' + ' '.join(html.xpath('string(//span[@id="shindanResult"])').split())
    img_list = [each.replace("data:image/jpeg;base64,", "base64://") for each in imgs]

    return text, img_list


async def get_hot(top_index=0, name=""):
    # https://shindanmaker.com/list
    if top_index < 29:
        headers = {
            "cookie": "_ga=GA1.2.440539836.1618304269; trc_cookie_storage=taboola%20global%3Auser-id=93ee8d5f-c5f4-48c6-924e-77da1e414e4a-tuct648ba0b; dui=eyJpdiI6IlhzQjJ1WnVoVkNFZ1Y1OXBKNlg2WVE9PSIsInZhbHVlIjoiVVhtZ1NTZWYxV2sxaC9aVmRncXNuREo1NTlteGNtVnZGQ1cyNFY4OHcxNldudWV5ZlZBbHJLL2pZZkk3aVQ0dTJ0djl2a0ROSW5jc1NBMXVHUHphejdxVld3bnNvQmw4bTkwMmJxK0VhQ01FT3ArV1ZEUGdqdWNlMW83VGlKa29QT2JjRVZzaXhhT2hiN3ViZHpMTkd3PT0iLCJtYWMiOiI5YzliZTlhMTk3NmE5YjMxMDc4NjNhNWZkZmQ4ZGEzYTg3ZDNmMzUzOGJhOGFmYWJiMmVlZjFiZDZiNjliOWM0In0=; _session=Xx4quie6qLKs5fady8KHb1QEDQ4EB1E2njevwZm7; _gid=GA1.2.1163823230.1618686436; dsr=eyJpdiI6Ijk2ZUNsVzR0czNqVjAwZ0gwRW8wZEE9PSIsInZhbHVlIjoiRGtiQng4MXBLdzRBbWltZWkrWW9hYXdERkZ1cmJNVThzSzFXcTU5Y1pDNjBqREpnamx5MzdydFhNUkhOWXNyTWRqc2psVmVmL0YvYm1EOWR5TWswVnc9PSIsIm1hYyI6ImIzYjczMWEyNTRmMTBjYWVjN2JlM2NiOGI2MDAxMjA0NGZjNzFjNmJiNTU1NGFlYzY5ZjRmMDcyMmY0NzI2M2YifQ==; name=eyJpdiI6IkFBMnE1cTkva1NrV3dxSEJSeE9tblE9PSIsInZhbHVlIjoiYmRlV1Npamh4RnkyRWdDYUhCN3ZFWHVVYUFRQXZBMEVYK1dTRzhBWmwzMWgzT2JodkdnQ3pPK0pxSDZIZXB1MUhHSi9mTXFzTVJFRS9Faks2UEwrSmc9PSIsIm1hYyI6IjhlNDk0NjI4MWEyMjFiNjhmYTQ5YzkzZDU0MDc4OTE0YTI4MTllZTg3NTA3NzA3NDBhOTVkZWVlNjcxN2Q2MGMifQ==; __gads=ID=daef441bdb6bf998:T=1618690556:S=ALNI_MY5PC9DMGtCGddfsjZmX-qQwnJo7Q; XSRF-TOKEN=eyJpdiI6IjFTdDZ6YzN5UWlYeVlBZHBNbHVpM0E9PSIsInZhbHVlIjoiU01rd2tHSnJRUkVtL2NGa1ZOYVN4c0U5bEVNNmw4TjFzd2VmQ09CNTVySE91RXFhSWhiWnRldE5vMThReFIzbytVQ0djUXBPZjRGeCtqRVlEam5JZmpRN0t3bDFVL3IzR3pGK3crM3JVOGZsdW1KckZOdEFTTS9BNDE4QSs4c3giLCJtYWMiOiJhMGZjMTQyNWIxMGI5NzUxODcwZTFkMmQ5MDIyNzc2OTY3YWI3MmE4NGFkNjg4YWYwYWIwMGNjN2JlNzQ3YjZkIn0=",
        }
        resp = await async_request('get', url="https://shindanmaker.com/list", headers=headers)
        html = etree.HTML(text=resp.text)
        hot_test = html.xpath('//div[@id="shindan-index"]//a[@class="shindanLink"]/@href')[top_index-1]
        title = html.xpath('//div[@id="shindan-index"]//a[@class="shindanLink"]/text()')
        reply = f"当前热门测试：{title}\n"
        text, img_list = await get_data(hot_test["href"][25:], name)
    else:
        reply = ""
        text, img_list = await get_data(top_index, name)
    return reply + text, img_list


def process_text_list(text, name):
    temp = ""
    for each in text:
        if each != name:
            temp += each + "\n"
        else:
            temp += each
    return temp


def get_text(tag: bs4.Tag) -> str:
    _inline_elements = {
        "a",
        "span",
        "em",
        "strong",
        "u",
        "i",
        "font",
        "mark",
        "label",
        "s",
        "sub",
        "sup",
        "tt",
        "bdo",
        "button",
        "cite",
        "del",
        "b",
        "a",
        "font",
    }

    def _get_text(tag: bs4.Tag) -> Generator:

        for child in tag.children:
            if type(child) is Tag:
                # if the tag is a block type tag then yield new lines before after
                is_block_element = child.name not in _inline_elements
                if is_block_element:
                    yield "\n"
                yield from ["\n"] if child.name == "br" else _get_text(child)
                if is_block_element:
                    yield "\n"
            elif type(child) is NavigableString:
                yield child.string

    return "".join(_get_text(tag))