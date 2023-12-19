# 来自 https://blog.csdn.net/user_from_future/article/details/130426876

import json
import time
import base64
# import execjs
import hashlib
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def translate_old(text):
    url = 'http://fanyi.youdao.com/translate'
    params = {
        'i': text,
        'doctype': 'json'
    }
    return requests.get(url, params=params).json()


session = requests.session()
lastModified = requests.get('https://fanyi.youdao.com/index.html').headers['last-Modified']
_nlmf = int(time.mktime(time.strptime(lastModified, "%a, %d %b %Y %H:%M:%S GMT")))
session.headers = {
    'Referer': 'https://fanyi.youdao.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}
session.get(f'https://rlogs.youdao.com/rlog.php?_npid=fanyiweb&_ncat=pageview&_ncoo=935962676.0432019&_nssn=NULL&_nver=1.2.0&_ntms={time.time()}&_nref=&_nurl=https%3A%2F%2Ffanyi.youdao.com%2Findex.html%23%2F&_nres=1920x1080&_nlmf={_nlmf}&_njve=0&_nchr=utf-8&_nfrg=%2F&/=NULL&screen=1920*1080')


def decrypt(text):
    key_md5 = hashlib.md5('ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl'.encode('utf-8')).digest()
    iv_md5 = hashlib.md5('ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4'.encode('utf-8')).digest()
    return unpad(AES.new(key=key_md5, mode=AES.MODE_CBC, iv=iv_md5).decrypt(base64.urlsafe_b64decode(text)), AES.block_size).decode('utf-8')


def translate(text, from_='auto', to=''):
    time_stamp = str(time.time())
    data = {
        'i': text,
        'from': from_,
        'to': to,
        'domain': '0',
        'dictResult': 'true',
        'keyid': 'webfanyi',
        'sign': hashlib.md5(f'client=fanyideskweb&mysticTime={time_stamp}&product=webfanyi&key=fsdsogkndfokasodnaso'.encode('utf-8')).hexdigest(),
        'client': 'fanyideskweb',
        'product': 'webfanyi',
        'appVersion': '1.0.0',
        'vendor': 'web',
        'pointParam': 'client,mysticTime,product',
        'mysticTime': time_stamp,
        'keyfrom': 'fanyi.web'
    }
    return json.loads(decrypt(session.post('https://dict.youdao.com/webtranslate', data=data).text))
