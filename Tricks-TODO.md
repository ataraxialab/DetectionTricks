预处理技巧：

Data augmentation：Random crops, contrast and color jittering
pretrained on LOC + pretrained global context：在LOC上训练时，得到proposal以后，做roi pooling时，多出一支在roi周围加一圈background后再进行pooling.
基础模型：

identity-mapping: 更改了residual的部分的模型
训练技巧：

balanced sampling: 按类进行训练，在load data的时候从200类中选择一个类，再从这个类的图片中选择一张进行训练
multi-scale training: 短边600,800,1000的都训
OHEM：选择hard example(loss比较高的)重新丢入网络中进行训练，ref:http://blog.csdn.net/u012905422/article/details/52760669
RPN训练技巧：

cascade RPN:在faster rcnn alternate training中迭代训练几次RPN+fast rcnn，然后将RPN取出来使用？多个模型分别做这个操作，然后把rois拿出来一起输入到后面网络中
constrained neg/pos :1.5:1, minBatchSize=32,即将config中TRAIN.RPN_FG_FRACTION=0.5->0.4，TRAIN.RPN_BATCHSIZE=256->32
测试技巧：

box voting: 在测试时进行，多个box投票得出最终位置
model fusion：多个模型训练结果fusion
