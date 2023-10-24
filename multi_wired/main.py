import os
import cv2
from paddleocr import PPStructure,draw_structure_result,save_structure_res
from PIL import Image
import save_pic
from recognition import recognize
img_num=7

# def savePic(a,path):
#     for i in range(len(a)):
#         if os.path.exists("./input_images/"):
#             pass
#         else:
#              os.mkdir("./input_images/")
#         imgPath = "./input_images/" + str(i+1) + ".jpg"  #notes: 图片的扩展名要一致
#         im = Image.open(path)
#         im = im.crop((a[i][0],a[i][1],a[i][2],a[i][3]))  # 对图片进行切割 im.crop(top_x, top_y, bottom_x, bottom_y)
#         im.save(imgPath)


def BanMian(img_path,save_folder='./output1'):
    table_engine = PPStructure(show_log=True,layout_model_dir='https://paddleocr.bj.bcebos.com/ppstructure/models/layout/picodet_lcnet_x1_0_fgd_layout_table_infer.tar',download=True)

    #table_engine = PPStructure(show_log=True,layout_model_dir='https://paddleocr.bj.bcebos.com/ppstructure/models/layout/picodet_lcnet_x1_0_fgd_layout_cdla_infer.tar',download=True)
    #table_engine = PPStructure(show_log=True,layout_model_dir='https://paddleocr.bj.bcebos.com/ppstructure/models/layout/picodet_lcnet_x1_0_fgd_layout_infer.tar',download=True)

    # save_folder = './output'
    # img_path = './origin_img/22.jpg'
    img = cv2.imread(img_path)
    result = table_engine(img)
    save_structure_res(result, save_folder,os.path.basename(img_path).split('.')[0])
    # for line in result:
    #     line.pop('img')
    #     print(line)
    a=[]
    for res in result:
        print(res)
        if res['type']== 'text':
            a.append(res['bbox'])
    # savePic(a,img_path)
    # location=save_pic.save(a)
    # res=recognize(a)
    # dic_txt_loc=[]
    # for i in range(len(location)):
    #     aa=location[i]
    #     txts=res[i]
    #     for j in range(len(aa)):
    #         dic_txt_loc.append([txts[j],aa[j]])
    return a
    # return dic_txt_loc
import cv2
import os
from itertools import product
from PIL import Image
def remove_shuiyin(file_path):
    img = Image.open(file_path)
    width, height = img.size
    for pos in product(range(width), range(height)):
        if sum(img.getpixel(pos)[:3]) > 500:
            img.putpixel(pos, (255, 255, 255))
    img.save(file_path)
res=[]
for i in range(1,img_num+1):
    remove_shuiyin('./img/{}.jpg'.format(str(i)))
    res0=BanMian('./img/{}.jpg'.format(str(i)))
    res.append(res0)
for i in range(len(res)):
    res[i].sort(key=lambda x:(x[1]+x[0]))
##这一步很关键
if os.path.exists('./part_table'):
    pass
else:
    os.mkdir('./part_table')
def cut_table(aa):
    for i in range(len(aa)):
        for j in range(len(aa[i])):
            if os.path.exists('./part_table/'+str(i+1)):
                pass
            else:
                os.mkdir('./part_table/'+str(i+1))
            SavePath='./part_table/'+str(i+1)+'/'+str(j+1)+'.jpg'
            im = Image.open('./img/'+str(i+1)+'.jpg')
            im = im.crop((aa[i][j][0],aa[i][j][1],aa[i][j][2],aa[i][j][3]))  # 对图片进行切割 im.crop(top_x, top_y, bottom_x, bottom_y)
            im.save(SavePath)
cut_table(res)
from paddleocr import PaddleOCR, draw_ocr

def shibie(name):
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
    img_path = name
    result = ocr.ocr(img_path, cls=True)
    # for idx in range(len(result)):
    #     res = result[idx]
    #     for line in res:
    #         print(line)

    # 显示结果
    # 如果本地没有simfang.ttf，可以在doc/fonts目录下下载
    from PIL import Image
    result = result[0]
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    print(txts)
    scores = [line[1][1] for line in result]
    allstring=""
    for i in txts:
        allstring+=i
    return allstring
ans_char=[]
num=0
pin_num=1
page_lian=[]
for i in range(len(res)):
    for j in range(len(res[i])):
        if j==len(res[i])-1 and i< len(res)-1:
            this_pic=res[i][j]
            next_pic=res[i+1][0]
            ##最后一张表格的下边界开始裁剪，如果剩余的部分除了页码还有其他的文字，就说明肯定不会链接在一起
            im_this=Image.open('./img/{}.jpg'.format(str(i+1)))
            this_remain_pic=im_this.crop((this_pic[0],this_pic[3],im_this.size[0],im_this.size[1]))
            this_remain_pic.save('test.jpg')
            this_char=shibie('test.jpg')
            if len(this_char)>1:
                print("说明剩下的部分还有文字，说明下一页肯定不是切断的表格")
                now=Image.open('./part_table/'+str(i+1)+'/{}.jpg'.format(j+1))
                now.save('./pinjie/{}.jpg'.format(pin_num))
                pin_num+=1
            else:
                #这一页的表格是页面的末尾，这个时候就需要考虑下一页的头部了
                im_next=Image.open('./img/{}.jpg'.format(str(i+2)))
                next_remain_pic=im_next.crop((0,0,next_pic[3],next_pic[1]))
                next_remain_pic.save('test.jpg')
                next_char=shibie('test.jpg')
                if len(next_char) >=2:
                    now=Image.open('./part_table/'+str(i+1)+'/{}.jpg'.format(j+1))
                    now.save('./pinjie/{}.jpg'.format(pin_num))
                    pin_num+=1
                    print('说明下一页肯定不是切断的表格，因为之前还有文字')
                else:
                    #这样的话，多半就能判断下一页和上一页是同一个表格了，因此可以将二者合并
                    #那要如何合并呢？暂时先不管共同表头合并试试，之后再删除共同表头
                    page_lian.append(i+1)
                    this_pic_old_path='./part_table/'+str(i+1)+'/{}.jpg'.format(str(j+1))
                    next_pic_old_path='./part_table/'+str(i+2)+'/1.jpg'
                    img1 = Image.open(this_pic_old_path)
                    img2 = Image.open(next_pic_old_path)
                    result = Image.new(img1.mode, (img1.size[0],img1.size[1]+img2.size[1]))
                    result.paste(img1, box=(0, 0))
                    result.paste(img2, box=(0,img1.size[1]))
                    result.save("./pinjie/{}.jpg".format(str(pin_num)))
                    pin_num+=1

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
table_recognition = pipeline(Tasks.table_recognition, model='damo/cv_dla34_table-structure-recognition_cycle-centernet')

location1=[]
location2=[]
pin_num=1
for i in range(len(res)):
    for j in range(len(res[i])):
        path='./part_table/{}/'.format(str(i+1))+'{}.jpg'.format(str(j+1))

        if  j==len(res[i])-1 and page_lian.count(i+1)!=0:

            next_path='./part_table/{}/1.jpg'.format(str(i+2))

            if page_lian.count(i)!=0 and len(res[i])==1:
                img1=Image.open(path)
                img2=Image.open(next_path)
                result = Image.new(img1.mode, (img1.size[0],img1.size[1]+img2.size[1]))
                result.paste(img1, box=(0, 0))
                result.paste(img2, box=(0,img1.size[1]))
                if len(res[i + 1])==1:
                    result.save(next_path)
                else:
                    result.save("./pinjie_removehead/{}.jpg".format(str(pin_num)))
                    pin_num+=1
                continue

            result1 = table_recognition(path)
            #就说明，这一张表后面还跟着一张表
            result2 = table_recognition(next_path)
            #然后对两个表识别出来的结果，如果有公共表头，则删去第二张表的公共表头
            #这里还没有写完，由于modelscope效果不好
            after_res=[]
            for k in result1['polygons']:
                #print(k)
                if abs(k[0]-k[4])<10:
                    continue
                temp=[int(k[0]),int(k[1]),int(k[4]),int(k[5])]
                after_res.append(temp)
            location1.append(after_res)
            after_res=[]
            for k in result2['polygons']:
                #print(k)
                if abs(k[0]-k[4])<10:
                    continue
                temp=[int(k[0]),int(k[1]),int(k[4]),int(k[5])]
                after_res.append(temp)
            location2.append(after_res)
            location1[0].sort(key=lambda x:(x[1]+x[0]))
            location2[0].sort(key=lambda x:(x[1]+x[0]))
            ##这里非常的美妙，按照xy之和排序，因为会有一到二的偏差，如果按x再按y排序的话，还会有几率后面的到前面来

            res1_first=location1[0][0]
            res2_first=location2[0][0]
            img1=Image.open(path)
            img2=Image.open(next_path)
            img1_first=img1.crop(res1_first)
            img2_first=img2.crop(res2_first)
            img1_first.save("./temp1.jpg")
            img2_first.save("./temp2.jpg")
            string1=shibie("./temp1.jpg")
            string2=shibie("./temp2.jpg")
            os.remove("./temp1.jpg")
            os.remove("./temp2.jpg")
            if string1!="" and string2==string1:
                ##这个时候两个表头就是相同的
                print(string1,string2)
                print("yes!")
                ##开始裁剪第二张表格的表头
                img2_cut=img2.crop((res2_first[0],res2_first[3],img2.size[0],img2.size[1]))
                #img2_cut.save('./test.jpg')
                result = Image.new(img1.mode, (img1.size[0],img1.size[1]+img2_cut.size[1]))
                result.paste(img1, box=(0, 0))
                result.paste(img2_cut, box=(0,img1.size[1]))
            else:
                ##这个时候表格是不相同的，因此直接拼接即可
                result = Image.new(img1.mode, (img1.size[0],img1.size[1]+img2.size[1]))
                result.paste(img1, box=(0, 0))
                result.paste(img2, box=(0,img1.size[1]))
            if len(res[i + 1])==1 and page_lian.count(i+2)!=0:
                result.save(next_path)
            else:
                result.save("./pinjie_removehead/{}.jpg".format(str(pin_num)))
                pin_num+=1
        else:
            if j!=0 or page_lian.count(i)==0:
                result1=Image.open(path)
                result1.save("./pinjie_removehead/{}.jpg".format(str(pin_num)))
                pin_num+=1