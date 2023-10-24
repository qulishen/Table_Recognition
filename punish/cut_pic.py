##裁剪处罚报告并且去除水印

import cv2
import os
num=0
from itertools import product
from PIL import Image

def cut_pic(file_path):
    global num
    # file_path = "pic/14.jpg"
    out_file_name = "opp"
    im = cv2.imread(file_path)
    im = im[80:,0:]
    save_path = "cut_remove/"
    save_path_file = os.path.join(save_path,str(num)+".jpg")
    num+=1
    cv2.imwrite(save_path_file,im)
    remove_shuiyin(save_path_file)

def remove_shuiyin(file_path):
    img = Image.open(file_path)
    width, height = img.size
    for pos in product(range(width), range(height)):
        if sum(img.getpixel(pos)[:3]) > 500:
            img.putpixel(pos, (255, 255, 255))
    img.save(file_path)

#cut_pic("./pic/14.jpg")