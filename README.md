# ImageNet Detection Tricks

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
