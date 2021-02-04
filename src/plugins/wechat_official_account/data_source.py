import json
import re
import os
import time
import datetime
import random
import hashlib
import pickle
import httpx
import asyncio
from lxml import etree


class WeChat(object):
    """
    获取需要爬取的微信公众号的推文链接
    """
    def __init__(self):
        """
        初始化参数
        Parameters
        ----------
        username: str
            用户账号
        password: str
            用户密码
        token : str
            登录微信公众号平台之后获取的token
        cookie : str
            登录微信公众号平台之后获取的cookie
        Returns
        -------
            None
        """
        # self.session = requests.session()
        self.session = httpx.AsyncClient()
        self.headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
        }
        self.params = {
            "lang": "zh_CN",
            "f": "json",
        }
        self.dir_path = os.path.abspath(os.path.join(__file__, "..", "data"))
        self.cookies_path = os.path.join(self.dir_path, "cookies/")
        self.qrcode_path = os.path.join(self.dir_path, "login.png")
        self.is_login = False
        # # 手动输入cookie和token登录
        # if (cookie != None) and (token != None):
        #     self.__verify_str(cookie, "cookie")
        #     self.__verify_str(token, "token")
        #     self.headers["Cookie"] = cookie
        #     self.params["token"] = token
        # # 扫描二维码登录
        # elif (username != None) and (password != None):
        #     self.username = self.__verify_str(username, "username")
        #     self.password = self.__verify_str(password, "password")
        #     # 暂不支持cookie缓存
        # else:
        #     print("please check your params")
        #     raise SystemError

    async def get_login_qrcode(self, username, password):
        img = await self.__startlogin_official(username, password)

        if self._save_login_qrcode(img.content):
            return self.qrcode_path

    async def login(self, username):
        if self.is_login:
            return
        else:
            await self.__login_official(username)

    def __verify_str(self, input_string, param_name):
        """
        验证输入是否为字符串
        Parameters
        ----------
        input_string: str
            输入
        param_name: str
            需要验证的参数名
        Returns
        ----------
            None
        """
        if not isinstance(input_string, str):
            raise TypeError("{} must be an instance of str".format(param_name))
        else:
            return input_string

    def _save_login_qrcode(self, img: bytes):
        """
        存储和显示登录二维码
        Parameters
        ----------
        img: str
            获取到的二维码数据
        Returns
        -------
            None
        """
        # from PIL import Image
        # 存储二维码
        with open(self.qrcode_path, "wb+") as fp:
            fp.write(img)
        return True
        # open_image("login.png")
        # 显示二维码， 这里使用plt的原因是： 等待用户扫描完之后手动关闭窗口继续运行；否则会直接运行
        # try:
        #     # img = Image.open("login.png")
        #     self.email.send("您的二维码失效了，请重新验证", "<img src='cid:login.png'>", receivers=['912871833@qq.com'], img="login.png")
        #     # img.show()
        # except Exception:
        #     raise TypeError(u"账号密码输入错误，请重新输入")

    def __save_cookie(self, username):
        """
        存储cookies, username用于文件命名
        Parameters
        ----------
        username: str
            用户账号
        Returns
        -------
            None
        """
        cookies_file = '{}{}.cookies'.format(self.cookies_dir_path, username)
        directory = os.path.dirname(cookies_file)

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(cookies_file, 'wb') as f:
            pickle.dump(self.session.cookies, f)


    def __read_cookie(self):
        """
        从本地加载Cookie

        Parameters
        ----------
        username: str
            用户账号
        Returns
        -------
            None
        """
        cookies_file = ''
        if not os.path.exists(self.cookies_dir_path):
            return False
        for name in os.listdir(self.cookies_dir_path):
            if name.endswith(".cookies"):
                cookies_file = '{}{}'.format(self.cookies_dir_path, name)
                break
        if cookies_file == '':
            return False
        with open(cookies_file, 'rb') as f:
            local_cookies = pickle.load(f)
        self.set_cookies(local_cookies)

    def set_cookies(self, cookies):
        self.session.cookies.update(cookies)

    def __md5_passwd(self, password):
        """
        微信公众号的登录密码需要用md5方式进行加密
        Parameters
        ----------
        password: str
            加密前的字符串
        Returns
        -------
        str：
            加密后的字符串
        """
        m5 = hashlib.md5()
        m5.update(password.encode('utf-8'))
        pwd = m5.hexdigest()
        return pwd

    async def __startlogin_official(self, username, password):
        """
        开始登录微信公众号平台，获取Cookies

        Parameters
        ----------
        username: str
            用户账号
        password: str
            用户密码
        Returns
        -------
            None
        """
        # 进行md5加密，一些post的参数
        pwd = self.__md5_passwd(password)
        data = {
            "username": username,
            "userlang": "zh_CN",
            "token": "",
            "pwd": pwd,
            "lang": "zh_CN",
            "imgcode": "",
            "f": "json",
            "ajax": "1"
        }

        # 增加headers的keys
        self.headers["Host"] = "mp.weixin.qq.com"
        self.headers["Origin"] = "https://mp.weixin.qq.com"
        self.headers["Referer"] = "https://mp.weixin.qq.com/"

        # 账号密码post的url
        bizlogin_url = "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=startlogin"
        # 获取二维码的url
        qrcode_url = "https://mp.weixin.qq.com/cgi-bin/loginqrcode?action=getqrcode&param=4300&rd=928"

        # 账号密码登录，获取二维码，等待用户扫描二维码，需手动关闭二维码窗口
        await self.session.post(bizlogin_url, headers=self.headers, data=data)
        img = await self.session.get(qrcode_url)
                # 去除之后不用的headers的key
        self.headers.pop("Host")
        self.headers.pop("Origin")

        return img


    async def __login_official(self, username, retry=10):
        """
        正式登录微信公众号平台，获取token
        Parameters
        ----------
        username: str
            用户账号
        retry: int
            重试次数
        Returns
        -------
            None
        """
        # 设定headers的referer的请求
        referer = f"https://mp.weixin.qq.com/cgi-bin/bizlogin?action=validate&lang=zh_CN&account={username}"
        self.headers["Referer"] = referer

        # 获取token的data
        data = {
            "userlang": "zh_CN",
            "token": "",
            "lang": "zh_CN",
            "f": "json",
            "ajax": "1",
        }
        # 获取token的url
        bizlogin_url = "https://mp.weixin.qq.com/cgi-bin/bizlogin?action=login"
        res = await self.session.post(bizlogin_url, data=data, headers=self.headers)
        res = json.loads(res.text)
        if retry > 0:
            try:
                # 截取字符串中的token参数
                token = res["redirect_url"].split("=")[-1]
                print(token)
                self.params["token"] = token
                # self.__save_cookie(username)  # 只有 cookies 似乎还不行，必须要带 token
                self.headers.pop("Referer")
                self.is_login = True
            except Exception:
                # 获取token失败，重新扫码登录
                print("登录失败，将在 3s 后重试")
                await asyncio.sleep(3)
                await self.__login_official(username, retry-1)


    async def search_official(self, name: str, **kwargs):
        url = "https://mp.weixin.qq.com/cgi-bin/searchbiz"
        param = {"action": "search_biz",
                "begin": "0",
                "count": "5",
                "query": name,
                "token": self.params['token'],
                "lang": "zh_CN",
                "f":    "json",
                "ajax": "1"}
        for i,j in kwargs.items():
            param[i] = j
        res = await self.session.get(url, params=param, headers=self.headers)
        result = json.loads(res.text).get('list', [])
        if result:
            return result
        else:
            print(f'查询失败：{res.text}')

    async def get_article(self, fakeid: str, begin=0, **kwargs):
        url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
        param = {
            "token": self.params['token'],
            "lang": "zh_CN",
            "f": "json",
            "ajax": "1",
            "action": "list_ex",
            "begin": str(begin),
            "count": "5",
            "query": "",
            "fakeid": fakeid,
            "type": "9",
        }
        for i, j in kwargs.items():
            if i in param.keys():
                param[i] = j
            else:
                raise AttributeError(f'无效参数：{i}')
        res = await self.session.get(url, params=param, headers=self.headers)
        result = json.loads(res.text).get('app_msg_list', [])
        if result:
            return result
        else:
            print(f'查询失败：{res.text}')

    async def get_firsts_official_atc(self, name: str, keywords='', **kwargs):
        data = await self.search_official(name)
        if data:
            atc_list = await self.get_article(data[0].get('fakeid'), **kwargs)
            item_list = list()
            if keywords:
                keywords = keywords.split()
            else:
                keywords = ['']
            for i in atc_list:
                item = dict()
                item['title'] = i.get('title', '')
                item['digest'] = i.get('digest', '')
                if any(keyword in (item['title'] + item['digest']) for keyword in keywords):
                    item['link'] = i.get('link', '')
                    item['create_time'] = time.strftime("%Y-%m-%d %A %X", time.localtime(i.get('create_time', 0)))
                    item['update_time'] = time.strftime("%Y-%m-%d %A %X", time.localtime(i.get('update_time', 0)))
                    item_list.append(item)
            return {'articles': item_list, 'keywords': keywords, 'total': len(item_list)}
        else:
            return '查询失败'

    async def download_article_images(self, urls:list, base_path=r"/usr/local/web/download"):
        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        query_path = os.path.join(base_path, now)

        async def downloader(session, urls, query_path, headers=None):
            for url in urls:
                res = await session.get(url, headers=headers)
                html = etree.HTML(text=res.text)
                title = html.xpath('//h2[@class="rich_media_title"]/text()')
                if title:
                    title = title[0].strip()
                atc_type = 'unknow'
                if '壁纸' in title:
                    atc_type = 'wallpaper'
                elif '背景' in title:
                    atc_type = 'background'
                links = html.xpath('//img/@data-src')
                for i in range(len(links)):
                    tp = re.findall('wx_fmt=(.*?)&', links[i])
                    if tp:
                        type_ = tp[0]
                    else:
                        type_ = 'png'
                    res = await session.get(links[i], headers=headers)
                    save_path = os.path.join(query_path, atc_type, title)
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                    with open(os.path.join(save_path, f'图{i+1}.{type_}'), 'wb') as f:
                        f.write(res.content)

        await downloader(self.session, urls, query_path, self.headers)
        cmd = f'cd {base_path} && zip -rm {now}.zip {now}'
        os.system(cmd)
        return f'http://159.75.88.21/download/{now}.zip'


def open_image(image_file):
    if os.name == "nt":
        os.system('start ' + image_file)  # for Windows
    else:
        if os.uname()[0] == "Linux":
            if "deepin" in os.uname()[2]:
                os.system("deepin-image-viewer " + image_file)  # for deepin
            else:
                os.system("eog " + image_file)  # for Linux
        else:
            os.system("open " + image_file)  # for Mac

