# -*- coding: utf8 -*-

# --------------------------------------------------------
# 12306-captcha
# Copyright (c) 2017
# Written by ruifengshan
# --------------------------------------------------------

# 功能: 用于下载12306的验证码图片

import cookielib
import hashlib
import random
import threading
import time
import urllib2

from src.config import cfg
from cut_image import thread_main

"下载指定地方的验证码图片"

# 'http格式封装'
agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
login = 'https://kyfw.12306.cn/otn/login/init'
domain = 'kyfw.12306.cn'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh - CN, zh;q = 0.8',
    'Cache-Control': 'no - cache',
    'Connection': 'keep-alive',
    'Host': domain,
    'User-aget': agent,
    'Referer': login
}


def download_image(download_dir=cfg.ROOT + '/data/download/all'):
    def get_url():
        const_url = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&'
        random_token = random.uniform(0, 1)
        img_url = const_url + urllib2.quote(str(random_token))
        print img_url
        return img_url

    try:
        cookie_j = cookielib.CookieJar()
        op = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_j))
        op.add_handler = [('User-agent', agent)]
        op.add_handler = [('Host', domain)]
        op.open(login)
        # '获取cookie'
        cookies = ''
        for Cookie in enumerate(cookie_j):
            ck = Cookie[1]
            cookies += ck.name + '=' + ck.value + ";"
        headers['Cookie'] = cookies

        # 下载30次
        for _ in range(random.randint(50, 200)):
            request = urllib2.Request(get_url(), cookies, headers=headers)
            raw = urllib2.urlopen(request).read()
            "采用十进制的md5命名文件名称"
            fn = hashlib.md5(raw).hexdigest()
            with open(download_dir + "/%s.jpg" % fn, 'wb') as fp:
                fp.write(raw)

            time.sleep(1)
    except Exception, e:
        print str(e)


if __name__ == '__main__':
    while True:
        try:
            download_image()
        except Exception, e:
            print 'error', str(e)
