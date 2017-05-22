# fpn

## 原理

参考 https://github.com/ataraxialab/DetectionTricks/blob/dev/ensemble/FPN.md

## 数据集

修改要点：针对resnet每层输出的 feature map分别输出不同的标签的训练数据。总共4个feature map，数据一样，标签不一样，每个feature map的标签包含标签的名字为：label**i**,bbox_target**i**,bbox_weight**i**，**i** 表示feature map的下标。这样在网络结构中就可以分别取到不同feature map对应的标签数据，并用于计算loss。

修改代码：

1. [生成anchor测试数据的代码](https://github.com/zjykzk/mxnet/blob/9cb83d6fa63139dd3a3e57691b50fb9ee4c13107/example/rcnn/rcnn/core/loader.py)
2. [生成anchor的gt信息](https://github.com/zjykzk/mxnet/blob/9cb83d6fa63139dd3a3e57691b50fb9ee4c13107/example/rcnn/rcnn/io/rpn.py#L68)

## 网络模型

修改要点：

1. 在mxnet框架下面通过共享RPN网络、faster rcnn网络参数来实现fpn的网络结构。
2. 针对2 * topdown + lateral 的操作，自定义mxnet中的operator来实现

修改代码：

1. [网络结构](https://github.com/zjykzk/mxnet/blob/9cb83d6fa63139dd3a3e57691b50fb9ee4c13107/example/rcnn/rcnn/symbol/symbol_resnet_fpn.py)

## metric

修改要点：不同的feature map计算loss的标签数据不一样，在打印日志的时候输出的loss值和精度也不同。重新定义输出的数据。

修改代码：

1. [fpn metric](https://github.com/zjykzk/mxnet/blob/9cb83d6fa63139dd3a3e57691b50fb9ee4c13107/example/rcnn/rcnn/core/metric_fpn.py)
2. [配置网络](https://github.com/zjykzk/mxnet/blob/9cb83d6fa63139dd3a3e57691b50fb9ee4c13107/example/rcnn/rcnn/config.py#L139)

## 启动训练

修改要点：

1. 取出每层feature map的符号(symbol)，传入 `FPNAnchorLoader` 用于计算训练数据中的标签数据，具体来说就是anchor和gt的对应关系。
2. 初始化权重、偏置参数，以及一些辅助参数(auxiliary params)

修改代码：

1. [启动脚本](https://github.com/zjykzk/mxnet/blob/9cb83d6fa63139dd3a3e57691b50fb9ee4c13107/example/rcnn/fpn/train.sh)
2. [训练入口脚本](https://github.com/zjykzk/mxnet/blob/9cb83d6fa63139dd3a3e57691b50fb9ee4c13107/example/rcnn/train_end2end_fpn.py)