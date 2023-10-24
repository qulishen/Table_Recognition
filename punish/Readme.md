使用方式，运行main.py，便可以将csv存储的图片网址下载下来并且去除水印保存在 remove_shuiyin中。
然后会把识别结果保存在result中。

文字识别模型

```
1.augmented_easyocr （效果较差）
2.https://github.com/PaddlePaddle/PaddleOCR/blob/dygraph/doc/doc_ch/quickstart.md
```

关于爬取和下载图片

```
1.get_each_page_url.py
获取该网站前10页所有公司的跳转链接，并且保存在page_url.csv中
2.get_img_url.py
从page_url.csv中遍历每一个公司的页面，然后把所有img的url保存在all_img.csv中
3.download_img.py
将all_img.csv中的每一个图片下载保存下来到pic文件夹中
```

关于处理图片以及识别

```
ocr.ipynb
其中先是水印处理，处理完保存在remove_shuiyin
然后是动态切除表头（表头长度不一），处理完保存在cut_remove中
然后对切除了的表头，将其分成左右两部分，分别保存在cut_left ,cut_right中
然后分别用左右模型识别, 对左右坐标对应的字段拼成一个字典
最后把字典保存为csv文件，储存在csv目录中
```

