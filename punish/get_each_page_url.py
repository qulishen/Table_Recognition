##用来获取首页中，每一页的具体的url，一共只有5页，每页10条，共50条，最后把url保存为 page_url.csv

import requests
from lxml import etree
import os
import pandas as pd
next_url="https://credit.dl.gov.cn/credit-portal/dl/publicity/metadata/record/detail/PUNISH/0/"

url="https://credit.dl.gov.cn/credit-portal/dl/api/publicity/record/PUNISH/0"
list_name=[]
def get_refer(a):
    start=0
    global list_name
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.46',
        'cookie': '_SID=b96843b9-7c96-4585-9d7e-6918c55b7f70',
        'Referer': 'https://credit.dl.gov.cn/credit-portal/dl/publicity/record/punish_publicity',
    }
    cond={'deptId': "", 'keyWord': "", 'openStyle': "2"}
    mydata={'condition':cond,'currentPage': a,'linesPerPage': 10,'listSql': ""}
    content=requests.post(url,headers=headers,json=mydata).text
    # print(content)
    while True:
        begin=content.find("zzbh",start)
        if begin==-1:
            break
        end=content.find("ID",begin)

        print(content[begin+7:end-3])
        list_name.append(next_url+content[begin+7:end-3])
        start=begin+2

for i in range(1,11):
    get_refer(i)
    test = pd.DataFrame(data=list_name)
    test.to_csv('page_url.csv',index=False,header=False)

