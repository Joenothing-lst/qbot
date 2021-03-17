from src.utils.util import async_request

HOST = 'nymph.rbq.life:3000'

wf_api = 'http://{}/wf/robot/{}'
wm_api = 'http://{}/wm/robot/{}'
rm_api = 'http://{}/rm/robot/{}'
wiki_api = 'http://{}/wiki/robot/{}'

dic = {
    '服务器时间': 'cambionCycle',
    '新闻': 'cambionCycle',
    '活动': 'cambionCycle',
    '警报': 'cambionCycle',
    '突击': 'cambionCycle',
    '地球赏金': 'cambionCycle',
    '金星赏金': 'cambionCycle',
    '火卫二赏': 'cambionCycle',
    '裂缝': 'cambionCycle',
    '促销商品': 'cambionCycle',
    '入侵': 'cambionCycle',
    '奸商': 'cambionCycle',
    '达尔沃': 'cambionCycle',
    '小小黑': 'cambionCycle',
    '地球': 'cambionCycle',
    '地球平原': 'cambionCycle',
    '舰队': 'cambionCycle',
    '金星平原': 'cambionCycle',
    '电波': 'cambionCycle',
    '仲裁': 'cambionCycle',
    '火卫二平原': 'cambionCycle'
}

async def get_wf_item(msg):
    item = dic.get(msg)
    if item:
        url = wf_api.format(HOST, item)
        results = await async_request('get', url)
        return results.text
    else:
        return '未找到【{msg}】，请从下列选项中选择查询：\n' + '\n'.join(i for i in dic.values())

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
