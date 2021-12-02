# encoding: utf-8

import json
import requests



def search(q):
    res = requests.get(f'https://so.m.sm.cn/api/rest?method=Subscribe.list&format=json&q={q}')
    data = json.loads(res.text)
    if data.get('wemedias'):
        if any(i['name'] == f"<em>{q}</em>" for i in data['wemedias']):
            count, url = detail(data['wemedias'][0]['wm_id'])
            print(q, count, url)
    else:
        print(q, '无')

def detail(uid):
    res = requests.get(f'https://bigsubs-api.uc.cn/api/bigsubs/{uid}/frontpage?sub_type=wm&ut=AAQuLl0WSFNXJwCIgccPZnizKN9OiLo2pkPjd5oIoq2jnA%3D%3D&app=ucweb&b_version=0.4')
    data = json.loads(res.text)
    return data['data']['total_article_cnt'], data['data']['homepage_url']

def parse(string):
    return [i.strip() for i in string.strip().split('\n')]

def main(s):
    l = parse(s)
    print(l)
    for v in l:
        search(v)


# 把列表复制粘贴到下面的空行↓
string="""
锵锵文史局
星小耀
果姐说电影
减肥的卡萨了
寒冬号角
小剑剑动漫
愚记谈娱乐
"""

main(string)