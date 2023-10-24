### punish
为行政处罚表格识别
### wired
为有线表格识别（采用的方案是modelscope切割加paddleocr识别）
### multi_wired
为多张有线表格识别（需要结合paddle的版面分析模型）
### PaddleOCR
其中\punish-ocr-master\punish-ocr-master\PaddleOCR\tools\infer\predict_det.py __call__函数 注释部分为modelscope的表格分割代码，用于表格分割，返回同样的dt_boxs