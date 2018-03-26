# -*- coding: utf-8 -*-
# @Time    : 18-3-26 下午8:25
# @Author  : pythonZhe
# @Email   : 18219111730@163.com
# @File    : spider.py
# @Software: PyCharm

import requests
from requests.exceptions import RequestException
from multiprocessing import Pool
import re
import json

# 获取单页的数据
def get_one_page(url):

    try:
        headers = {"user-agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        print(e.response)
        return None
# 解析页面数据中需要的数据
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'+'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'+'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    # print(items)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'star':item[3].strip()[3:],
            'time':item[4].strip()[5:],
            'score':item[5]+item[6]
        }

# 将解析的数据写入到文件中
def write2file(content):
    with open('maoyantop100.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()



def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write2file(item)


if __name__ == '__main__':
    # for i in range(10):
    #     main(i*10)

    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])






