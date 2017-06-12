# 用MSRA版本的RCNN进行训练

## 安装
* 使用自有的MXNet基础镜像：ataraxia/ava-training-mxnet:gpu
* git clone https://github.com/msracver/Deformable-ConvNets.git
* 安装需要的软件

  pip install Cython easydist
  apt-get update && apt-get install python-yaml zip -y

* 编译
  * 在Deformable-ConvNets目录下执行 sh ./init.sh
  * copy ./rfcn/operator_cxx to $(YOUR_MXNET_FOLDER)/src/operator/contrib
  * 重新编译MXNet：用AVA的Dockerfile里的编译命令，不要用MXNet官方的命令：

  cd $MXNET_ROOT
  make -j"$(nproc)" USE_DIST_KVSTORE=1 USE_CUDA=1 USE_CUDA_PATH=/usr/local/cuda USE_CUDNN=1 USE_OPENCV=1 \
    EXTRA_OPERATORS=${MXNET_ROOT}/example/rcnn/operator

现在，应该可以开始正常使用MSRA版本的RCNN了

## 训练



## 测试


