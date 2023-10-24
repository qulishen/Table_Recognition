#这个是获取每个页面中的img的url

import requests
from lxml import etree
import os
import pandas as pd
num=0

img_url=[]
def get_imgurl(refer):
    global img_url
    start=0
    #https://credit.dl.gov.cn/credit-portal/dl/img_resource/publicity_detail/20230415/2c9180816f3756b2016f3bbb1e700240/0/50533.png
    img_orgin="https://credit.dl.gov.cn/credit-portal/dl/img_resource"
    url = 'https://credit.dl.gov.cn/credit-portal/dl/api/credit_service/page/detail'
    # 爬取到页面源码数据
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.46',
        'cookie': '_SID=b96843b9-7c96-4585-9d7e-6918c55b7f70',
        'Referer': refer
    }
    tt=refer.find("PUNISH")
    objectID=refer[tt+9:]
    print(objectID)
    cond = {'publicityTag': "PUNISH", 'objectType': "0", 'objectId': objectID}
    mydata = {'condition': cond, 'currentPage': 1, 'linesPerPage': 10}
    res = requests.post(url, headers=headers, json=mydata).text
    while True:
        begin=res.find("imageUrl",start)
        if begin==-1:
            break
        end=res.find("png",begin)
        print(res[begin+11:end+3])
        start=begin+3
        img_url.append(img_orgin+res[begin+11:end+3])
if __name__ == '__main__':

    ##这里读入，每一个页面的url的csv文件，可用get_each_page_url获取
    data = pd.read_csv(r'page_url.csv', header=None).values
    data = data.flatten()
    for i in data:
        get_imgurl(i)
    data = pd.read_csv(r'dalian.csv', header=None).values
    data=data.flatten()
    for i in data:
        get_imgurl(i)
    print(img_url)
    test = pd.DataFrame(data=img_url)
    test.to_csv('all_img.csv', index=False, header=False)
