from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
table_recognition = pipeline(Tasks.table_recognition, model='damo/cv_dla34_table-structure-recognition_cycle-centernet')
result = table_recognition('https://modelscope.oss-cn-beijing.aliyuncs.com/test/images/table_recognition.jpg')
print(result)