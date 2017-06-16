# 用MSRA版本的RCNN进行训练

## 安装
* 使用自有的MXNet基础镜像：ataraxia/ava-training-mxnet:gpu
* git clone https://github.com/ElaineBao/Deformable-ConvNets.git        
(add imagenet dataset support)      
或    
git clone https://github.com/msracver/Deformable-ConvNets.git     
(官方的repo，没有imagenet dataset)
* 安装需要的软件
  ```
  apt-get update && apt-get install python-yaml zip -y
  ```

* 编译
  * 在Deformable-ConvNets目录下执行:
  ```
  sh ./init.sh
  ```
  * RFCN相关的extra operaters拷贝到mxnet中：
  ```
  cp -r ./rfcn/operator_cxx/*  $(YOUR_MXNET_FOLDER)/src/operator/contrib
  ```
  * 重新编译MXNet：用AVA的Dockerfile里的编译命令，不要用MXNet官方的命令：
  
  ```
  cd $MXNET_ROOT
  make -j"$(nproc)" USE_DIST_KVSTORE=1 USE_CUDA=1 USE_CUDA_PATH=/usr/local/cuda USE_CUDNN=1 USE_OPENCV=1 EXTRA_OPERATORS=${MXNET_ROOT}/example/rcnn/operator
  ```

现在，可以开始正常使用MSRA版本的RCNN了

## 训练
### 1. 下载模型和数据集，运行demo
按照[https://github.com/ElaineBao/Deformable-ConvNets/blob/master/README.md](https://github.com/ElaineBao/Deformable-ConvNets/blob/master/README.md)操作

### 2. 在imagenet上进行训练
- original faster rcnn:

首先在 `experiments/faster_rcnn/cfgs/resnet_v1_101_imagenet_rcnn_end2end.yaml`
中配置好参数，如gpu数等。    
然后运行：

```
python experiments/faster_rcnn/rcnn_end2end_train_test.py \
--cfg experiments/faster_rcnn/cfgs/resnet_v1_101_imagenet_rcnn_end2end.yaml
```

- deformable faster rcnn:

首先在 `experiments/faster_rcnn/cfgs/resnet_v1_101_imagenet_rcnn_dcn_end2end.yaml`
中配置好参数，如gpu数等。    
然后运行：

```
python experiments/faster_rcnn/rcnn_end2end_train_test.py \
--cfg experiments/faster_rcnn/cfgs/resnet_v1_101_imagenet_rcnn_dcn_end2end.yaml
```

- deformable rfcn:

首先在 `experiments/rfcn/cfgs/resnet_v1_101_imagenet_rfcn_dcn_end2end_ohem.yaml`
中配置好参数，如gpu数等。    
然后运行：

```
python experiments/rfcn/rfcn_end2end_train_test.py \
--cfg experiments/rfcn/cfgs/resnet_v1_101_imagenet_rfcn_dcn_end2end_ohem.yaml
```

## 训练速度测试
| config | dataset | method | speed |
|---|---|---|---|
|2卡，P100|imagenet|faster_rcnn| 6.8 samples/s|
|4卡，P100 |imagenet|faster_rcnn| 8.9 samples/s|
|1卡，P100 |voc | deformable faster_rcnn | 4 samples/s|
|1卡，P40 | voc | deformable faster_rcnn | 3.04 samples/s |
|2卡, M40 | voc|deformable faster_rcnn| 6.57 samples/s|
|1卡, M40|imagenet|deformable faster_rcnn |3.0samples/s|
|2卡, M40|imagenet| deformable faster_rcnn | 5.37samples/s |
|1卡, M40|voc|deformable rfcn+ohem | 2.7samples/s|
|2卡, M40|voc|deformable rfcn+ohem |4.86samples/s|
|2卡, M40|imagenet| deformable rfcn+ohem| 1.64samples/s|
|4卡，P100|imagenet| deformable rfcn+ohem |6.48samples/s|


