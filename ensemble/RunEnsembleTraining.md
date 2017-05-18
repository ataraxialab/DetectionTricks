# Tutorial for Running ensumble training model

## Tricks Used
* Data Augment
  * contrast
  * brightness
  * color
https://github.com/ataraxialab/DetectionTricks/blob/dev/dataprocess/DataAugmentation.md

* Multi-Scale
https://github.com/ataraxialab/DetectionTricks/blob/dev/dataprocess/MultiscaleTraining.md

* Balanced Sampling
文档 - TODO

* Pos/Neg Constrain
constrained neg/pos :1.5:1, minBatchSize=32,即将config中TRAIN.RPN_FG_FRACTION=0.5->0.4，TRAIN.RPN_BATCHSIZE=256->32

* RoIAlign
https://github.com/ataraxialab/DetectionTricks/blob/dev/fastrcnn/ROIAlign.md

* Global Context
TODO

* FPN
Pending

* OHEM
TODO

* Cascade RPN
TODO

## Train End2End ImageNet
* 第一个参数是使用的GPU ID，只用一个也得填参数
bash script/vgg_imagenet.sh 0,1,2,3

## Pretrain on LOC
文档 - TODO

## Train RPN
文档 - TODO

## Train rcnn
文档 - TODO
