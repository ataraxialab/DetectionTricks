## Install MXNET
1.按照官网指示安装mxnet依赖：[Installing MXNet](http://mxnet.io/get_started/install.html). (选择**Linux-Python-GPU-Build from source**.)  

2.下载ataraxialab/RCNN:

```
$ cd MXNET_ROOT/example
$ git clone https://github.com/ataraxialab/RCNN.git  
```
然后编译：

``` 
$ cd MXNET_ROOT/example/RCNN     
$ bash script/additional_deps.sh      
``` 

3.验证安装是否成功：
打开python terminal。  

``` 
$ python
```  
以一个自己定义的symbol为例子查看是否注册成功。  

```
>>> import mxnet as mx
>>> mx.symbol.ROIAlign
```

若出现`<function ROIAlign at xxxx>`注册成功则说明安装成功，否则查看上述步骤是否确已完成。 

注意：以后都使用MXNET_ROOT/example/RCNN文件夹，我们的代码都在这里；不是MXNET_ROOT/example/rcnn文件夹，这是mxnet官方的rcnn实现。

## Data Prepare
### Data Prepare for imagenet\_CLS\_LOC_2017 dataset 
1.下载imagenet\_cls\_loc_2017数据集，构造其目录结构为：

```
imagenet_loc_rootpath
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
```

2.清洗数据：   

```
# 生成训练数据集，生成的train.txt文件
python mxnet/example/rcnn/data_clean.py train /the/path/to/ILSVRC2017/ILSVRC CLS_LOC
```
把清洗以后生成的`train.txt`重命名成`train_loc.txt`.  

3.完成data prepare后的目录结构为：  

```
imagenet_loc_rootpath
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
+--- val.txt # 原验证集list
```

4.将数据链接到mxnet中，便于使用。 

```
$ cd mxnet
$ cd example/rcnn
$ mkdir data
$ ln -s imagenet_loc_rootpath data/
```

### Data Prepare for imagenet\_DET_2017 dataset 
1.下载imagenet\_DET_2017数据集，构造其目录结构如下:

```
imagenet_DET_rootpath
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
```

2.清洗数据：   

```
# 生成训练数据集，生成的train.txt文件
python mxnet/example/rcnn/data_clean.py train /the/path/to/ILSVRC2017/ILSVRC DET
```
 

3.完成data prepare后的目录结构如下，和CLS_LOC略有不同：  

```
imagenet_DET_rootpath
|
+---ILSVRC
|      |
|      +--- Annotations
|      |
|      +--- Data
|      |
|      +--- ImageSets
|      |		 |	
|      |		 +--- train.txt  # 清洗以后生成的文件
|      |		 |	
|      |		 +--- val.txt    # 原验证集list
|      |
|      +--- devkit
```

4.将数据链接到mxnet中，和CLS_LOC略有不同。 

```
$ cd mxnet
$ cd example/rcnn
$ mkdir data
$ mkdir data/imagenet
$ ln -s imagenet_rootpath/ILSVRC data/imagenet/DET
```

## Model Prepare
1. 将所需要的模型链接到mxnet中，便于使用。模型可以从这里下载: [mxnet model zoo](http://mxnet.io/model_zoo/)

```
$ cd mxnet
$ cd example/rcnn
$ mkdir model
$ ln -s your_model_path model/
```

## Train Imagenet LOC
```
$ cd mxnet
$ cd example/rcnn
$ bash script/resnet_imagenet_loc.sh 0,1  # 0,1表示gpu id
```
关于tricks:  
1. **global context:** 可以直接在`script/resnet_imagenet_loc.sh`添加`--use_global_context`. 目前global context仅支持resnet系列模型。   
2. **data augmentation:** 可以直接在`script/resnet_imagenet_loc.sh`添加`--use_data_augmentation`.  
3. **roi align:** 可以直接在`script/resnet_imagenet_loc.sh`添加`--use_roi_align`.  
4. **multiscale training:** 在rcnn/config.py中将  

```
config.SCALES = [(600, 1000)]
```
改成你想要用的multiscale，如：   

```
config.SCALES = [(600, 1000), (800,1333), (1000,1667)]
```

5.**constrained positive/negative ratio:** 在rcnn/config.py中将    

```
# rpn anchors batch size
config.TRAIN.RPN_BATCH_SIZE = 256
# rpn anchors sampling params
config.TRAIN.RPN_FG_FRACTION = 0.5
```
改为：

```
# rpn anchors batch size
config.TRAIN.RPN_BATCH_SIZE = 256
# rpn anchors sampling params
config.TRAIN.RPN_FG_FRACTION = 0.5
```
