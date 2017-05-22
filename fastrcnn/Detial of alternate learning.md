# MxNet 分步骤训练详细介绍
## 原框架分步骤训练流程
1. 利用ImageNet 初始化训练 RPN 
2. 生成训练完的模型生成RPN框
3. 利用 `2` 生成的RPN和ImangeNet的初始化训练RCNN
4. 利用 `3` 生成的模型初始化训练新的RPN
5. 生成新的RPN框
6. 将 `4` 的模型和 `3` 的模型合并为新的模型
7. 用 `6` 的模型训练新的RCNN 模型
8. 合并 `7` 和 `4` 的模型作为最终的模型

### 流程详细介绍
####利用ImageNet 初始化训练 RPN 

* 固定 `config.py` 设置的 `FIXED_PARAMS` 中的layers，随机初始化 rpn相关的`rpn_conv_3x3_weight`,`rpn_conv_3x3_bias`，`rpn_cls_score_weight`,`rpn_cls_score_bias`，`rpn_bbox_pred_weight`,`rpn_bbox_pred_bias` 的权值

####生成PRN的框

* 利用训练完成的RPN网络调用`core/tester` 中的 `core／tester.generate_proposals`函数生成`pkl` 文件
训练RCNN 模型
* 固定 `config.py` 设置的 `FIXED_PARAMS` 中的layers，随机初始化 `cls_score_weight`,`cls_score_bias`,`bbox_pred_weight`,`bbox_pred_weight`的权值
* 通过`train_rcnn` -> `tools/load_proposal_roidb` -> `dataset/imdb.load_rpn_data`读取对应的pkl 文件

####第二轮训练RPN

* 固定 `config.FIXED_PARAMS_SHARED` 中的layers ，继续随机初始化rpn相关layers 得到新的RPN模型

####第二轮训练RCNN
* 将第二轮训练的到的RPN 与 第一轮训练的到RCNN ，利用 `tools／combine_model` 进行合并，合并原则是RPN的前面的layers 加上 RCNN 后面的layers
* 固定 `config.FIXED_PARAMS_SHARED` 中的layers ，初始化相关layers 进行训练
* 由于设置在 `config.FIXED_PARAMS_SHARED` 中的layers包括了所有的RPN相关的前面的所有layers 所以利用简单合并的原则就可以最终的模型

### Inceptionv3 模型从新训练
####我们的想法：
* 简单 `fine-tune` 检测用的 `inceptionv3` 模型效果不佳，需要重新训练，只用RPN训练会导致效果不佳，需要添加 `cls_label` 提升训练质量

####步骤 ：
1. LOC 数据集 Pretrain RPN 模型：利用两种 `loss`
2. 生成RPN框
3. 合并RPN 和 ImageNet 模型
4. 利用合并模型训练RCNN模型
5. 利用 `4` 中训练的模型作为新的 `inecptionv3` 模型进行 `fine-tune` 

#### ToDolist
1. 为了保证效果 LOC PreTrain 需要两类loss ，需要写一个新的 `symbol`
2. 训练RPN
3. 生成RPN `pkl` 文件 
4. 合并 `Pretrain` 和 `imagenet` 模型
5. End2End `finetune`
6. 获得 `mAP` 




