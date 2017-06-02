### rpneval 
使用mxnet rcnn 框架中 testrpn代码，输入的参数为
|参数|含义|
|----|----|
|--network|输入的模型类型比如resnet|
|--dataset|测试的样本类型voc,coco或者imagenet 一般为imagenet|
|--image_set|表示测试集train val 或者test，一般为val|
|--prefix|模型文件的前缀|
|--epoch|表示第几个epoch|
|--gpu|gpuid|
|--thresh|rpn最低的score阈值|

log中可以查看average recall等情况，同时会保存一个pkl文件在xxx路径下

### 读取rois pkl 计算recalls
另外写一个工具 输入参数定义如下
|参数|含义|
|----|----|
|--pklfile|输入的pkl文件|
|--dataset|测试的样本类型voc,coco或者imagenet 一般为imagenet|
|--image_set|表示测试集train val 或者test，一般为val|

同样在log中查看average recall等信息

### rcnn eval
使用mxnet rcnn框架中的testrcnn代码，输入参数为：
|参数|含义|
|----|----|
|--network|输入的模型类型比如resnet|
|--dataset|测试的样本类型voc,coco或者imagenet 一般为imagenet|
|--image_set|表示测试集train val 或者test，一般为val|
|--prefix|模型文件的前缀|
|--epoch|表示第几个epoch|
|--gpu|gpuid|
|--thresh|rcnn最低的score阈值|

默认读取xxx路径下的rois的pkl文件
log中可以查看mAP等情况，同时会保存最终的检测结果的一个pkl文件在xxx路径下

### post processing
另外写一个后处理的工具，读取一个或者多个检测结果的pkl文件，做融合或者boxvoting。输入参数为：
|参数|含义|
|----|----|
|--pklfileIn|输入的pkl文件列表，用 `，`分割|
|--pklfileOut|输出的pkl文件名|
|--dataset|测试的样本类型voc,coco或者imagenet 一般为imagenet|
|--image_set|表示测试集train val 或者test，一般为val|

log中可以查看mAP等情况，同时会保存最终的检测结果的一个pkl文件在pklfileOut路径下