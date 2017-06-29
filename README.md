# ImageNet Detection Tricks

## ATLAB ImageNet leaderboard
| model | mAP | eval method | Training set | PreTrain set | Training Log | Eval Log | Base Module| config |
| ----- |---|---|---|---|---|---|---|---|
| 【ALL】= resnet101 (multiscale) + resnet101\_ratio4 (multiscale) + resnet101\_scale4 (multiscale) + resnet152 (multiscale) + inceptionv3 (multiscale) + rcnn_dcn (multiscale) | 0.5295 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENS1】=【ALL】 - dcn\_rcnn (scale1000, mAP=0.4231) | 0.5301 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENS2】=【ENS1】 - dcn\_rcnn (scale400, mAP=0.4249) | 0.5297 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENS3】=【ENS2】 - inceptionv3 (scale400, mAP=0.4257)| 0.5289 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENS4】=【ENS3】 - resnet152 (scale400, mAP=0.4318)  - resnet101\_ratio4 (scale400, mAP=0.4350) - resnet101\_scale4 (scale400, mAP=0.4375)| 0.5289 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENS5】=【ALL】 - resnet152 (scale400, mAP=0.4318)  - resnet101\_ratio4 (scale400, mAP=0.4350) - resnet101\_scale4 (scale400, mAP=0.4375)| 0.5298 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENS6】=【ENS1】 + dcn\_rfcn (scale600, mAP=0.4695) | 0.5305 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENS7】=【ENS6】 - resnet101 (scale400, mAP=0.4456) | 0.5295 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENS8】=【ENS7】 - resnet101 (scale1000, mAP=0.4532) | 0.5301 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENS9】=【ENS8】 - resnet101\_scale4 (scale1000, mAP=0.4555) | 0.5296 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENS10】=【ENS9】 - dcn\_rcnn (scale800, mAP=0.4597) | 0.5292 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENS11】=【ENS10】 - resnet152 (scale1000, mAP=0.4655) | 0.5284 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENS12】=【ENS11】 - resnet101_ratio4 (scale1000, mAP=0.4656) | 0.5288 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENS13】=【ENS12】 - dcn\_rcnn (scale600, mAP=0.4681) | 0.5287 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| 【ENS14】=【ENS13】 - inceptionv3 (scale1000, mAP=0.4751) | 0.5271 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
|【ENS15】 = resnet101 (scale400,600,800) + resnet101 ratio\_4 (scale600,800) + resnet101\_scale4 (scale600,800,1000) + resnet152 (scale600,800,1000) + inceptionv3 (scale400,600,800,1000) + rcnn\_dcn (scale400,600,800) + dcn\_rfcn (scale 600) | 0.5311 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
|【ENS16】 = 【ENS15】- resnet101\_ratio4 (scale600, 0.4817) | 0.5311 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
|【ENS17】 = 【ENS16】- resnet101 (scale600, 0.482) | 0.5299 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
|【ENS18】 = 【ENS17】- resnet101\_scale4 (scale800, 0.4824) | 0.5299 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
|【ENS19】 = 【ENS18】- resnet101\_scale4 (scale600, 0.4839) | 0.5298 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
|【ENS20】 = 【ENS19】- resnet101\_ratio4 (scale800, 0.4860) | 0.5299 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
|【ENS21】 = 【ENS20】- resnet152 (scale600, 0.4873) | 0.5301 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
|【ENS22】 = 【ENS21】- resnet152 (scale800, 0.4874) | 0.5310 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
|【ENS23】 = 【ENS22】- inceptionv3 (scale600, 0.4892) | 0.5279 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
|【ENS24】 = 【ENS23】- resnet101 (scale800, 0.4898) | 0.5247 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
|【ENS25】 = 【ENS24】- inceptionv3 (scale800, 0.4928) | 0.5224 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
|【ENS26】 = resnet101 (scale400,600,800) + resnet101\_scale4 (scale600,1000) + resnet152 (scale1000) + inceptionv3 (scale400,600,800,1000) + rcnn\_dcn (scale400,600,800) + dcn\_rfcn (scale 600) | 0.5305 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
|【ENS27】 = 【ENS15】将rcnn_dcn 5epoch(scale400,600,800)替换成7epoch | 0.5314 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
|【ENS28】 = 【ENS27】+ rcnn_dcn (scale1000)| 0.5326 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
|【ENS29】 = 【ENS28】+ resnet101\_ratios4\_alltricks (scale600) - resnet101\_ratios4 (scale600)| 0.5326 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
|【ENS30】 = 【ENS29】+ rcnn_dcn (scale800) | 0.5319 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| resnet101(multiscale) +resnet152 +inceptionv3 | 0.5222 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| resnet101(multiscale) +deepmask +resnet152 +inceptionv3 | 0.5213 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| resnet101(multiscale) +deepmask +resnet152|0.5141 |nms+box voting | Imagenet all|-|-|-|-|NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
| resnet101(multiscale) +deepmask | 0.5090 | [nms+box voting](https://github.com/ataraxialab/DetectionTricks/blob/dev/ensemble/BoxVoting.md) | Imagenet all | - | - | - | -| NMS＝0.5 IoU_Thresh=0.5 score_Thresh=0.1 |
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


