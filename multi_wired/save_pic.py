#调用save函数，传入的参数是版面分析得到的二维数组，会自动在part文件夹下创建不同表格的单独文件，用来保存每个表格的单元格
import os
from PIL import Image
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
table_recognition = pipeline(Tasks.table_recognition, model='damo/cv_dla34_table-structure-recognition_cycle-centernet')
def save_single(aa,path,num):
    for i in range(len(aa)):
        SavePath='./part/'+num+'/'+str(i+1)+'.jpg'
        im = Image.open(path)
        #print(path)
        for k in range(4):
            print(aa[i][k])
            if aa[i][k]<0:
                aa[i][k]=0
        if aa[i][0]<aa[i][2] and aa[i][1]<aa[i][3]:
            im = im.crop((aa[i][0],aa[i][1],aa[i][2],aa[i][3]))  # 对图片进行切割 im.crop(top_x, top_y, bottom_x, bottom_y)
            ##print((aa[i][0],aa[i][1],aa[i][2],aa[i][3]))
            im.save(SavePath)
def save(a):
    location=[]
    if os.path.exists('./part/'):
        pass
    else:
        os.mkdir('./part/')
    for i in range(len(a)):
       
        if os.path.exists('./part/'+str(i+1)):
            pass
        else:
            os.mkdir('./part/'+str(i+1))
        path='./input_images/'+str(i+1)+'.jpg'
        result = table_recognition(path)
        after_res=[]
        for k in result['polygons']:
            for ki in range(len(k)):
                if k[ki]<0:
                    k[ki]=0
            temp=[int(k[0]),int(k[1]),int(k[4]),int(k[5])]
            after_res.append(temp)
        location.append(after_res)
        save_single(after_res,path,str(i+1))
    return location