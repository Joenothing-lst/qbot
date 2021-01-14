import httpx


wm_api = 'http://nymph.rbq.life:3000/wm/robot/{}'
rm_api = 'http://nymph.rbq.life:3000/rm/robot/{}'
wiki_api = 'http://nymph.rbq.life:3000/wiki/robot/{}'


async def async_request(method: str, url: str, **kwargs):
    async with httpx.AsyncClient() as client:
        result = await client.request(method.upper(), url, **kwargs)
        return result

async def get_wm_item(item):
    url = wm_api.format(item)
    results = await async_request('get', url)
    return results.text

async def get_rm_item(item):
    url = rm_api.format(item)
    results = await async_request('get', url)
    return results.text

async def get_wiki_item(item):
    url = wiki_api.format(item)
    results = await async_request('get', url)
    return results.text