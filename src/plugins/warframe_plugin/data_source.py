from src.utils.util import async_request

HOST = 'nymph.rbq.life:3000'

wf_api = 'http://{}/wf/robot/{}'
wm_api = 'http://{}/wm/robot/{}'
rm_api = 'http://{}/rm/robot/{}'
wiki_api = 'http://{}/wiki/robot/{}'

dic = {
    '服务器时间': 'timestamp',
    '新闻': 'news',
    '活动': 'events',
    '警报': 'alerts',
    '突击': 'sortie',
    '地球赏金': 'Ostrons:',
    '金星赏金': 'Solaris',
    '火卫二赏': 'EntratiSyndicate:',
    '裂缝': 'fissures',
    '促销商品': 'flashSales',
    '入侵': 'invasions',
    '奸商': 'voidTrader',
    '达尔沃': 'dailyDeals',
    '小小黑': 'persistentEnemies',
    '地球': 'earthCycle',
    '地球平原': 'cetusCycle',
    '舰队': 'constructionProgress',
    '金星平原': 'vallisCycle',
    '电波': 'nightwave',
    '仲裁': 'arbitration',
    '火卫二平原': 'cambionCycle'
}

async def get_wf_item(msg):
    item = dic.get(msg)
    if item:
        url = wf_api.format(HOST, item)
        results = await async_request('get', url)
        return results.text
    else:
        return f'未找到【{msg}】，请从下列选项中选择查询：\n' + '\n'.join(i for i in dic.keys())


async def get_wm_item(item):
    url = wm_api.format(HOST, item)
    results = await async_request('get', url)
    return results.text


async def get_rm_item(item):
    url = rm_api.format(HOST, item)
    results = await async_request('get', url)
    return results.text


async def get_wiki_item(item):
    url = wiki_api.format(HOST, item)
    results = await async_request('get', url)
    return results.text
