from paddleocr import PaddleOCR,draw_ocr
import cv2
import os
from itertools import product
from PIL import Image
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
ocr = PaddleOCR(use_angle_cls=True, lang='ch') # need to run only once to download and load model into memory
num=0
def ocr_fun(img_path):
    result = ocr.ocr(img_path, cls=True)
    # for idx in range(len(result)):
    #     res = result[idx]
    #     for line in res:
    #         print(line)

    # draw result
    from PIL import Image
    result = result[0]
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
    im_show = Image.fromarray(im_show)
    #im_show.save('./result'+'/'+ img_path.split('/')[-1])
    #print(result)
    return result

##裁剪
def get_token_list(path):
    result=ocr_fun(path)
    key_list=['组织名','社会信用代码','行政处罚','法人代表','违法行为类型','违法事实','处罚依据','处罚类别','处罚内容','罚款金额','财物的金额','暂扣或吊销','处罚决','处罚有效','公示截止期','处罚机关']
    key_index=0
    up_list=[]
    down_list=[]
    contents=[]
    for i in range(len(result)):
        #print(result[i][1][0])
        if result[i][1][0].find(key_list[key_index])!=-1:
            #print(result[i][0][0][1])
            up_list.append(result[i][0][0][1])
            down_list.append(result[i][0][2][1])
            contents.append(result[i][1][0])
            print(result[i][1][0])
            key_index+=1
            if key_index==16:
                break
    return up_list,down_list,contents,result
def cut_pic(file_path):
    global num
    out_file_name = "opp"
    up_list,down_list,_,_=get_token_list(file_path)
    im = cv2.imread(file_path)
    im = im[int(up_list[0]):,0:]
    save_path = "cut_remove/"
    save_path_file = os.path.join(save_path,str(num)+".jpg")
    num+=1
    cv2.imwrite(save_path_file,im)
def remove_shuiyin(file_path):
    img = Image.open(file_path)
    width, height = img.size
    for pos in product(range(width), range(height)):
        if sum(img.getpixel(pos)[:3]) > 500:
            img.putpixel(pos, (255, 255, 255))
    img = img.convert('RGB')
    img.save('remove_shuiyin'+'/'+file_path.split('/')[-1])
    #cut_left(file_path)
def cut_left(path):
    origin=cv2.imread(path)
    right=origin[0:,230:]
    left=origin[0:,0:230]
    cv2.imwrite('./cut_left'+'/'+path.split('/')[-1],right)
    cv2.imwrite('./cut_right'+'/'+path.split('/')[-1],left)
def get_dict(num):
    diction={}
    index=0
    key_list=['组织名称','统一社会信用代码','行政处罚决定文书号','法人代表人','违法行为类型','违法事实','处罚依据','处罚类别','处罚内容','罚款金额（万元）','没收违法所得、没收非法财物的金额（万元）','暂扣或吊销证照名称及编号','处罚决定日期','处罚有效期','公示截止期','处罚机关']
    left_path='./cut_right/{}.jpg'.format(str(num))
    right_path='./cut_left/{}.jpg'.format(str(num))
    left_up_list,left_down_list,left_contents,left_result=get_token_list(left_path)
    _,_,_,right_result=get_token_list(right_path)
    right_up_list=[]
    right_down_list=[]
    right_contents=[]
    print(left_result)
    for i in range(len(right_result)):
        #print(result[i][1][0])
        #print(result[i][0][0][1])
        right_up_list.append(right_result[i][0][0][1])
        right_down_list.append(right_result[i][0][2][1])
        right_contents.append(right_result[i][1][0])
    row=0
    while index<=15:
        key=key_list[index]
        value=""
        if row==len(right_up_list):
            break
        while index==15 or right_down_list[row]<left_up_list[index+1]:
            value+=right_contents[row]
            row+=1
            if row==len(right_down_list):
                break
        diction[key]=value
        index+=1

    return diction