
from PIL import Image
def savePic(a,path):
    for i in range(len(a)):
        imgPath = "./input_images/" + str(i+1) + ".jpg"  #notes: 图片的扩展名要一致
        im = Image.open(path)
        im = im.crop((a[i][0],a[i][1],a[i][2],a[i][3]))  # 对图片进行切割 im.crop(top_x, top_y, bottom_x, bottom_y)
        im.save(imgPath)
