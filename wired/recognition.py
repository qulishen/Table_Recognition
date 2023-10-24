from paddleocr import PaddleOCR, draw_ocr

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
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
## 遍历一个文件夹下的所有图像 
def bianli_pics(path):
    import os
    img_folder = path
    img_list = [os.path.join(nm) for nm in os.listdir(img_folder) if nm[-3:] in ['jpg', 'png', 'gif']]
    ## print(img_list) 将所有图像遍历并存入一个列表
    ## ['test_14.jpg', 'test_15.jpg', 'test_9.jpg', 'test_17.jpg', 'test_16.jpg']
    all_img=[]
    for i in img_list:
        paths=os.path.join(path,i)
        ## print(path)
        ## ./input/test_14.jpg
        ## ./input/test_15.jpg
        #print(paths)
        all_img.append(paths)
        all_img.sort(key=lambda x: int(x.split('\\')[-1][:-4]))
    return all_img
def recognize(a):
    all_txts=[]
    for i in range(len(a)):
        path="./part/"+str(i+1)
        imgs_path=bianli_pics(path)
        #print(imgs_path)
        txts=[]
        for i in imgs_path:
            txt=shibie(i)
            txts.append(txt)
        all_txts.append(txts)
    return all_txts