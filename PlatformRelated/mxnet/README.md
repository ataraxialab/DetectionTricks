
# 在MXNet上运行RCNN

* 安装依赖
apt-get update && apt-get install -y vim git lrzsz python-tk libopencv-dev python-opencv
pip install easydict scikit-image matplotlib Cython
bash script/additional_deps.sh

* 下载VOC和pretrained model
bash script/get_voc.sh
bash script/get_pretrained_model.sh

* 修改
from __future__ import print_function 移到第一行

* 训练
bash script/vgg_voc07.sh 0,1

## 基础镜像
ataraxia/ava-training-mxnet-det:opencv3-py27-cuda8-cudnn5
包含了启动bash scripts/vgg_voc07.sh 0,1的依赖
使用姿势：将model 和 data ln 过来 即可
