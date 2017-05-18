# Baseline Models

* Machine Types

  | GPU | | Types | Best Practice |
  | ------| ------ | ------ | ------ |
  | K80	| 16 | 1,2,4,8 | ? |
  | M40	| 7/8	| 1,2,4,8 | ? |
  | P4	| 16	| 1,2,4,8 | ? |
  | P40	| 16	| 1,2,4,8	| ? |
  | P100	| 16	| 1,2,4,8	| ? |
  | CPU | ? | ? | ? |


## Results on VOC07
* 验证网络是否work，找GPUs的最佳实践

  | 网络 | Original | FPN | RoIAlign | FPN + RoIAlign | Identity Mapping | Pretrain on LOC | RPN | RCNN | Constrained Pos/Neg | Multiscale Training | DataAugmentation |
  | ------| ------ | ------ | ------ | ------| ------ | ------ | ------ | ------ | ------ | ------ | ------ |
  | VGG19	| mAP=0.7019 | | | | | | | | 	 	 	 	 
  | ResNet101 | mAP=0.7453 | | 2GPU(M40): 3.45samples/sec, mAP=0.7507 | | | | | | 2GPU(M40): 3.45samples/sec, mAP=0.7417 | 2GPU(M40): 3.45samples/sec, mAP=0.7609 | 2GPU(P100): 4.5samples/sec, mAP=0.7400 |
  | ResNet152	| mAP=0.7522(mxnet), mAP=0.439(pytorch) | mAP=0.283(pytorch)| | | | | | | | | |
  | ResNet200	| mAP=0.75 | | | | | | |  | | | |
  | ResNeXt50  | | | | | | | | | | | |
  | ResNeXt101 | | | | | | | | | | | |
  | ResNeXt200 | | | | | | | | | | | |
  | Inception-V3 | MAP=0.5956| | | | | | | | 	| | |
  | Inception-ResNet-V2	 | | | | | | | | | |  | | |
  | YOLO9000 | | | | | | | | | | | | |

## Results on ImageNet Sub
* 验证ImageNet闭环

  | 网络 | Original | FPN | RoIAlign | FPN + RoIAlign | Identity Mapping | Pretrain on LOC | RPN | RCNN |
  | ------| ------ | ------ | ------ | ------| ------ | ------ | ------ | ------ |
  | VGG19 | | | | | | | | |
  | ResNet101 | mAP=0.38 | @zenk | @baobao | | | | | |
  | ResNet152 | 4xP100:7img/s 0.3711| | | | | | | |
  | ResNet200 | | | | | | | | |
  | ResNeXt50 | | | | | | | | |
  | ResNeXt101 | | | | | | | | |
  | ResNeXt200 | | | | | | | | |
  | Inception-V3 | 4xP40:7img/s 0.2468 | | | | | 4xP4:9.5img/s Running|| | |
  | Inception-ResNet-V2 | | | | | | | | |
  | YOLO9000 | | | | | | | | |


## Results on ImageNet Full
训练Baseline，得到最终结果

  | 网络 | Original | FPN | RoIAlign | FPN + RoIAlign | Identity Mapping | Pretrain on LOC | RPN | RCNN |
  | ------| ------ | ------ | ------ | ------| ------ | ------ | ------ | ------ |
  | VGG19	| | | | | | | | | 	 	 	 	 
  | ResNet101 | mAP=0.482 | | | | | | | |
  | ResNet152 | @zzj | | | | | 1GPU(P40): 2.10samples/sec 2GPU(P40): 3.70samples/sec 4GPU(P40): 5.2samples/sec (running)|  | |
  | ResNet200	| | | | | | | |  |
  | ResNeXt50  | | | | | | | | | 	 	 	 	 	 	 	 	 
  | ResNeXt101 | | | | | | | | | 	 	 	 	 	 	 
  | ResNeXt200 | | | | | | | | |	 	 	 	 	 	 
  | Inception-V3 | | | | | | | | | 	 	 	 	 	 	 	 
  | Inception-ResNet-V2	 | | | | | | | | |
  | YOLO9000 | | | | | | | | | |


* ResNet-V2来源：
https://github.com/tornadomeet/ResNet

* pretrained on LOC + pretrained global context：在LOC上训练时，得到proposal以后，做roi pooling时，多出一支在roi周围加一圈background后再进行pooling.
* balanced sampling: 按类进行训练，在load data的时候从200类中选择一个类，再从这个类的图片中选择一张进行训练
* multi-scale training: 短边600,800,1000的都训
* OHEM：选择hard example(loss比较高的)重新丢入网络中进行训练，ref:http://blog.csdn.net/u012905422/article/details/52760669
* constrained neg/pos :1.5:1, minBatchSize=32,即将config中TRAIN.RPN_FG_FRACTION=0.5->0.4，TRAIN.RPN_BATCHSIZE=256->32
