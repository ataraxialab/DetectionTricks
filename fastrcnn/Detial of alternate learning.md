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
#### 利用ImageNet 初始化训练 RPN 

* 固定 `config.py` 设置的 `FIXED_PARAMS` 中的layers，随机初始化 rpn相关的`rpn_conv_3x3_weight`,`rpn_conv_3x3_bias`，`rpn_cls_score_weight`,`rpn_cls_score_bias`，`rpn_bbox_pred_weight`,`rpn_bbox_pred_bias` 的权值

#### 生成PRN的框

* 利用训练完成的RPN网络调用`core/tester` 中的 `core／tester.generate_proposals`函数生成`pkl` 文件
训练RCNN 模型
* 固定 `config.py` 设置的 `FIXED_PARAMS` 中的layers，随机初始化 `cls_score_weight`,`cls_score_bias`,`bbox_pred_weight`,`bbox_pred_weight`的权值
* 通过`train_rcnn` -> `tools/load_proposal_roidb` -> `dataset/imdb.load_rpn_data`读取对应的pkl 文件

#### 第二轮训练RPN

* 固定 `config.FIXED_PARAMS_SHARED` 中的layers ，继续随机初始化rpn相关layers 得到新的RPN模型

#### 第二轮训练RCNN
* 将第二轮训练的到的RPN 与 第一轮训练的到RCNN ，利用 `tools／combine_model` 进行合并，合并原则是RPN的前面的layers 加上 RCNN 后面的layers
* 固定 `config.FIXED_PARAMS_SHARED` 中的layers ，初始化相关layers 进行训练
* 由于设置在 `config.FIXED_PARAMS_SHARED` 中的layers包括了所有的RPN相关的前面的所有layers 所以利用简单合并的原则就可以最终的模型

### Inceptionv3 模型从新训练

#### 我们的想法：
* 简单 `fine-tune` 检测用的 `inceptionv3` 模型效果不佳，需要重新训练，只用RPN训练会导致效果不佳，需要添加 `cls_label` 提升训练质量

#### 步骤 ：
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
 
#### MutilTask 详细实现
`symbol` 流程图如下：
1. metric 更新流程：
	`rcnn.core.module.bind()` -> `mxnet.module.module.init()` -> `mxnet.module.excutor_group.update_metric()` -> `mx.metric.EvalMetric.update_dict()` -> `update()` 

2. 添加一种新的loss步骤：
	生成一个带新的loss 的 symbol 文件，输入参数写在最前面，网络结构中实现计算loss的方法,并将loss `group` 到最终的输出中：
	
	[symbol](https://github.com/likelyzhao/mxnet/blob/dev-faster-rcnn/example/rcnn/rcnn/symbol/symbol_inceptionv3.py#L391-L456) 
	
	添加一个新的dataloader：
	`rcnn/core` 中的 dataloader 是继承自 `mx.io.DataIter` 的，需要修改里面的 `get_batch` 函数添加你要添加的新的label或者input ，再在 `self.label_name` 变量数组中添加该变量，注意这里用到的变量的名字应与symbol 中变量的名字保持一致。 此外在 `infer_shape` 中添加label的大小的信息
	
	[dataloader](https://github.com/likelyzhao/mxnet/blob/dev-faster-rcnn/example/rcnn/rcnn/core/loader.py#L397-L586)
	
	添加监控使用的`metric` : 在 `get_rpn_name`列表的 `pred` 和 `label` 中增加你添加的变量名并保持 `pred` 变量顺序与symbol文件中输出的`group`的顺序一致，`label` 变量顺序与新的dataloader中的`self.label_name` 中顺序保持一致，并添加loss 计算逻辑
	
	[metric](https://github.com/likelyzhao/mxnet/blob/dev-faster-rcnn/example/rcnn/rcnn/core/metric.py#L71-L97)
	
	training 文件中添加新的dataloader 和 metric ，
   重新写一个训练用的python 文件，制定我们的symbol dataloader和metric 开始训练mutil task
   
   [training_file](https://github.com/likelyzhao/mxnet/blob/dev-faster-rcnn/example/rcnn/rcnn/tools/train_rpn_mutiltask.py)
   
   修改配置参数，重新设置哪些层次保持不变
   
   [set_config](https://github.com/likelyzhao/mxnet/blob/dev-faster-rcnn/example/rcnn/rcnn/config.py#L169)
   
   
	




