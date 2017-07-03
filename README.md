# ImageNet Detection Tricks

## ATLAB ImageNet leaderboard
| model | mAP | eval method | Training set | PreTrain set | Training Log | Eval Log | Base Module| config |
| ----- |---|---|---|---|---|---|---|---|
| 【inceptionv3 multiscale】| 0.5126(thresh=0.01)，0.5146(thresh=0.001)  |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【resnet152 multiscale】| 0.5055(thresh=0.01)  |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【resnet101 multiscale】| 0.5086(thresh=0.01)  |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【resnet101 series】= resnet101 multiscale+ resnet101\_scale4\_multiscale+ resnet101\_ratios4\_multiscale| 0.5101(thresh=0.01)  |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【dcn\_rcnn\_101 multiscale】| 0.5032(thresh=0.01)  |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【dcn\_rfcn\_101 multiscale】| 0.5162(thresh=0.01), 0.5176(thresh=0.001)  |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENSEMBLE #1】= resnet152 multiscale + resnet101 multiscale + inceptionv3 multiscale + dcn\_rcnn\_101 multiscale | 0.5325(thresh=0.01), 0.5319(thresh=0.02)  |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENSEMBLE #2】= resnet152 multiscale + resnet101 series + inceptionv3 multiscale + dcn\_rfcn\_101 multiscale | 0.5308(thresh=0.02) |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENSEMBLE #3】= resnet101 multiscale + inceptionv3 multiscale + dcn\_rfcn\_101 multiscale | 0.5301(thresh=0.02)  |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENSEMBLE #4】= resnet152 multiscale + resnet101 multiscale + inceptionv3 multiscale + dcn\_rfcn\_101 multiscale + dcn\_rcnn\_101 multiscale | 0.5310(thresh=0.02)  |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENSEMBLE #5】= resnet101 (scale400,600,800) + resnet101_ratios4 (scale600,800) + resnet101_scale4 (scale600,800,1000) + resnet152 (scale600,800,1000) + inceptionv3 multiscale + dcn\_rcnn multiscale + dcn\_rfcn (scale 600) | 0.5314(thresh=0.02), 0.5326(thresh=0.001)  |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
|[Resnet-101 std](http://op3uxikvk.bkt.clouddn.com/resnet-101-all.params)|0.4874|[test.py](https://github.com/likelyzhao/mxnet/blob/dev-faster-rcnn/example/rcnn/test.py)|ImageNet all|None|[Train](http://op3uxikvk.bkt.clouddn.com/resnet-101-all-train.log)|[Test](http://op3uxikvk.bkt.clouddn.com/resnet-101-all-test.log)|[Resnet-101 param](http://data.dmlc.ml/mxnet/models/imagenet/resnet/101-layers/resnet-101-0000.params) [Resnet 101 modeljson](http://data.dmlc.ml/mxnet/models/imagenet/resnet/101-layers/resnet-101-symbol.json)|[config](https://github.com/likelyzhao/mxnet/blob/dev-faster-rcnn/example/rcnn/rcnn/config.py)|
|[ResNet-101 smalldb](http://op3uxikvk.bkt.clouddn.com/resnet101-params)|0.3958|[test.py](https://github.com/likelyzhao/mxnet/blob/dev-faster-rcnn/example/rcnn/test.py)|ImageNet train_0| None |[Train](http://op3uxikvk.bkt.clouddn.com/Resnet101-smalldb-train.log)|[Eval](http://op3uxikvk.bkt.clouddn.com/Resnet101-smalldb-eval.log)|[Resnet-101 param](http://data.dmlc.ml/mxnet/models/imagenet/resnet/101-layers/resnet-101-0000.params) [Resnet 101 modeljson](http://data.dmlc.ml/mxnet/models/imagenet/resnet/101-layers/resnet-101-symbol.json)|[config](https://github.com/likelyzhao/mxnet/blob/dev-faster-rcnn/example/rcnn/rcnn/config.py)



## 基础模型
* [ResNet-101 Variants](http://op3uxikvk.bkt.clouddn.com/resnet101-params)

### 使用多个差异很大的CNN模型 - diversity matters!
* 7 * BN-Inception (32 Layers)
* 2 * MSRA-Net (22 Layers)
* ResNet, Identity Map

### 数据放大
* random crop
* multi-scale
* contrast jittering
* color jittering
* Pretrain on LOC !!

### 单个模型的改进
* Objectness loss
* Negative categories
* BBox Voting

## 训练技巧
* Balanced Sampling
* Multi-Scale Training
* Online Hard Sample Mining

### RPN Proposal
* Cascade RPN
* Constrained Neg/Pos Anchor Ratio

### Pretraining
* Pretrained Global Context


## 测试技巧
* Multi-Scale Testing
* HFlip
* Box Votinng


Tricks的实现划分在以下5个文件夹中：
* dataprocess
* regionproposal
* fastrcnn
* postprocess
* ensumble

上述代码尝试做成平台无关，与计算框架相关的代码都在*PlatformRelated*文件夹中


