##版面分析代码，调用BanMian 传入图片地址即可处理为多张表格到 input_images中，并且调用分割函数，能够直接把切割好的表格放到part1-n中
##将原始图片处理成多张表格
import os
import cv2
from paddleocr import PPStructure,draw_structure_result,save_structure_res
from PIL import Image
import save_pic
from recognition import recognize
def savePic(a,path):
    for i in range(len(a)):
        if os.path.exists("./input_images/"):
            pass
        else:
             os.mkdir("./input_images/")
        imgPath = "./input_images/" + str(i+1) + ".jpg"  #notes: 图片的扩展名要一致
        im = Image.open(path)
        im = im.crop((a[i][0],a[i][1],a[i][2],a[i][3]))  # 对图片进行切割 im.crop(top_x, top_y, bottom_x, bottom_y)
        im.save(imgPath)
        
def BanMian(img_path,save_folder='./output'):
    table_engine = PPStructure(show_log=True,layout_model_dir='https://paddleocr.bj.bcebos.com/ppstructure/models/layout/picodet_lcnet_x1_0_fgd_layout_table_infer.tar',download=True)
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
        if(res['type']=='text'):
            a.append(res['bbox'])
    savePic(a,img_path)
    location=save_pic.save(a)
    res=recognize(a)
    dic_txt_loc=[]
    for i in range(len(location)):
        aa=location[i]
        txts=res[i]
        for j in range(len(aa)):
            dic_txt_loc.append([txts[j],aa[j]])
    # font_path = 'doc/fonts/simfang.ttf' # PaddleOCR下提供字体包
    # image = Image.open(img_path).convert('RGB')
    # im_show = draw_structure_result(image, result,font_path=font_path)
    # im_show = Image.fromarray(im_show)
    # im_show.save('result.jpg')
    return dic_txt_loc
#返回值是版面的坐标，如
#[[2, 8, 1622, 399],[x,x,x,x]]
from PIL import Image

# font_path = 'doc/fonts/simfang.ttf' # PaddleOCR下提供字体包
# image = Image.open(img_path).convert('RGB')
# im_show = draw_structure_result(image, result,font_path=font_path)
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')