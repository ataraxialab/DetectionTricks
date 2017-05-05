网络设计完毕，在VOC数据集上跑一遍训练和评估，来验证模型网络是否有问题
调用这个脚本可以跑训练和评估
bash script/vgg_voc07.sh 0,1


## 各个网络在VOC07上的meanAP

| 网络模型 | GPUs | meanAP | 迭代速度 |
| ------| ------ | ------ | ------ |
| VGG16 | 4xP4 | 0.7 | ~8.5img/s |
| ResNet101 | 4xP100 | 0.74 | ~8.5img/s |
| ResNet200 | 4xP100 | ? | ~5.5img/s |

## 验证ResNet网络

训练ResNet200，修改ResNet152方法一致
1. 下载Pretrained model
http://data.dmlc.ml/mxnet/models/imagenet/resnet/200-layers/resnet-200-0000.params
2 改rcnn/config.py 中的https://github.com/dmlc/mxnet/blob/master/example/rcnn/rcnn/config.py#L130
此处的resnet-101改为resnet-200
3 改rcnn/symbol/symbol_resnet.py 中https://github.com/dmlc/mxnet/blob/master/example/rcnn/rcnn/symbol/symbol_resnet.py#L10
units = res_deps['101']
此处改为
units = res_deps['200']

然后运行bash script/resnet_voc07.sh 0,1 即可
