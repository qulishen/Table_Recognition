from PIL import Image, ImageDraw, ImageFont
import csv
from punish.other import remove_shuiyin,cut_pic,cut_left,ocr_fun,get_dict

# for i in range(0,1098):
#     remove_shuiyin('./pic/{}.jpg'.format(str(i)))
##把remove_shuiyin中去掉的水印之后，然后开始砍头
for i in range(0,1098):
    cut_pic('./remove_shuiyin/{}.jpg'.format(str(i)))
##砍完头之后，从砍完头之后的文件中，讲文件分成左右两部分
for i in range(0,1098):
    cut_left('./cut_remove/{}.jpg'.format(str(i)))

list_cant=[98,150,249,370,676,678,848]
##这个是识别不出来的一些数据集
for i in range(0,1098):
    if i not in list_cant:
        ans=get_dict(i)
        # header = ['name', 'age'] #数据列名
        # datas = [{'name': 'Tony', 'age': 17}, {'name': '李华', 'age': 21}] # 字典数据
        #print(ans.items())
        with open('./csv/{}.csv'.format(str(i)),'w',newline='',encoding="utf-8") as f:
            writer = csv.writer(f)
            for row in ans.items():
                writer.writerow(row)