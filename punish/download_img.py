import requests
from lxml import etree
import os
import pandas as pd
from urllib.request import urlopen, Request
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.46',
    'cookie': '_SID=b96843b9-7c96-4585-9d7e-6918c55b7f70',
    'Referer': 'https://credit.dl.gov.cn/credit-portal/dl/publicity/record/punish_publicity',
}
num=0
def download(image_url):
    global num
    # -*- coding:utf-8 -*-
    name = "pic/{}.jpg".format(num)
    # 保存文件时候注意类型要匹配，如要保存的图片为jpg，则打开的文件的名称必须是jpg格式，否则会产生无效图片
    image_url=Request(image_url, headers=headers)
    conn = urlopen(image_url)
    f = open(name, 'wb')
    f.write(conn.read())
    f.close()
    print('Pic Saved!')
    num+=1

data = pd.read_csv(r'all_img.csv', header=None).values
data = data.flatten()
for i in data:
    download(i)
    print(i)