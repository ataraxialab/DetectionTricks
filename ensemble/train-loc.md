# 基于ImageNet训练RPN

### 代码

1. 在包 `rcnn/symbol` 下面定义网络代码，推荐一个网络一个文件。在这部分代码当中需要定义两个函数： `get_网络名字_rpn` 和 `get_网络名字_rpn_test`，分别返回rpn网络代码，和测试的rpn网络代码。其中，`网络名字` 是指定义好的网络的名称，比如 `resnet` `vgg` 。
2. 包 `rcnn/symbol` 导出 *1* 中新添加的函数。

参考文件： `rcnn/symbol/symbol_resnet.py，rcnn/symbol/__init__.py`。

### 训练

```bash
#!/usr/bin/env bash
# 网络： resnet
# 数据集：ILSVRC 2017 的分类测试数据
LOG=loc_train_loc_2017.log

rm -rf ${LOG}

export MXNET_CUDNN_AUTOTUNE_DEFAULT=0
export PYTHONUNBUFFERED=1

# 注意：--dataset_path 不需要改
nohup python -m rcnn.tools.train_rpn --network resnet                       \
                                  --dataset imagenet_loc_2017               \
                                  --image_set train                         \
                                  --root_path /disk2/data/imagenet_loc_2017 \
                                  --dataset_path ILSVRC                     \
                                  --prefix model/imagenet_loc_2017          \
                                  --gpu 0,1                                 \
                                  >${LOG} 2>&1 &
```

### 测试

```shell
#!/usr/bin/env bash
# 网络模型：resnet训练的第1轮epoch的结果
# 测试数据：ILSVRC 2017 分类的val数据集
LOG=loc_test_loc_2017.log

rm -rf ${LOG}

export MXNET_CUDNN_AUTOTUNE_DEFAULT=0
export PYTHONUNBUFFERED=1

# 注意：--dataset_path 不需要改
nohup python -m rcnn.tools.test_rpn --network resnet                        \
                                  --dataset imagenet_loc_val_2017           \
                                  --image_set val                           \
                                  --root_path /disk2/data/imagenet_loc_2017 \
                                  --dataset_path ILSVRC                     \
                                  --prefix model/imagenet_loc_2017          \
                                  --gpu 3                                   \
                                  --epoch 1                                 \
                                  >${LOG} 2>&1 &
```

### ILSVRC2017数据集

#### KIRK源

数据集放在目录 `/disk2/data/imagenet_loc_2017` 上面，所以启动镜像的时候需要挂载相关的NFS。

#### 构造

##### 清洗数据

代码

```python
# repo: https://github.com/ataraxialab/mxnet
# branch: master
# file: example/rcnn/loc_train/clean.py
```

命令

```shell
# 生成测试数据集，生成的train.txt文件
python mxnet/example/rcnn/loc_train/clean.py train /the/path/of/ILSVRC2017/ILSVRC

# 生成验证数据集，生成的val.txt文件
python mxnet/example/rcnn/loc_train/clean.py val /the/path/of/ILSVRC2017/ILSVRC
```

##### ILSVRC2017数据集

1. 清洗数据

2. 把清洗以后生成的 `train.txt` 重命名成 `train_loc.txt`

3. 构造目录结构

   ```shell
   rootpath
   |
   +---ILSVRC
   |      |
   |      +--- Annotations
   |      |
   |      +--- Data
   |      |
   |      +--- ImageSets
   |      |
   |      +--- devkit
   +--- train_loc.txt # 清洗以后生成的文件
   |
   +--- val.txt # 清洗以后生成的文件
   ```