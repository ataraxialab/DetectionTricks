# Overview
![](resources/overview.png)
this doc will focus on **Data Loading(IO)** part.

## 设计理念
一个IO系统包含两个部分：data preparation和data loading。数据准备通常是离线做的，而数据读入则会影响实时的性能。
### Data Preparation
数据准备是指将数据打包成想要的形式，用于之后的处理。对像imagenet这样的大型数据库进行数据准备，过程会很耗时，这时候我们需要考虑以下几点： 
  
- 将数据集打包成几个文件。一个数据集可能包含几百万的数据，将数据打包成几份能够方便地用于分布式。    
- 一次性打包。我们不希望每次更改一下run-time settings，比如使用机器的数目改变了，就需要重新进行打包。    
- 打包过程并行执行来节省时间。
- 能够容易地获取数据的任意部分。这对于分布式机器学习进行数据并行非常重要。理想的行为是：不管数据在物理上被打包成了多少份，它们在逻辑上能够被拆分成任意份。比如：我们将1000张图片打包成4个物理文件，那么每个文件包含250张图片。如果我们使用10台机器来训练一个DNN,那么我们需要在每台机器上load 100张图片。另外，有些机器可能需要从不同的物理文件中读取图片。   

### Data Loading
下一步需要考虑的是如何把打包的数据load到RAM里。我们的目标是读取数据越快越好。需要考虑以下几点：

- 读取的连续性：如果数据存在磁盘上的连续位置，我们可以读的更快。   
- 减少要读入的字节数：我们可以通过将数据保存成简洁的方式来实现这一点，比如把图片保存成JPEG格式。
- 读取和训练在不同的线程中进行：这样可以避免在读取数据的时候出现计算瓶颈。
- 节省RAM：明智地决定是否需要把所有的文件都读入RAM中。

## Data Format
由于训练DNN通常需要大量的数据，因此我们选择的数据格式应该是高效而简便的。为了实现这一点，我们需要将二值的数据打包成可拆分的形式。在MXNet中我们使用dmlc-core中实现的binary recordIO作为数据的主要格式。

### Binary Record

![](resources/baserecordio.jpg)

在MXNet的binary RecordIO中，我们将每个数据实例保存成一条记录。    
1. kMagic是一个魔数表示一条记录的起始位置。
> 魔数：很多类型的文件，其起始的几个字节的内容是固定的（或是有意填充，或是本就如此）。根据这几个字节的内容就可以确定文件类型，因此这几个字节的内容被称为魔数（magic number）。

2.Lrecord记录了长度和一个连续的flag。在Lrecord中， 
   
- cflag == 0:这是一条完整的记录     
- cflag == 1:这是多条记录的起始         
- cflag == 2:这是多条记录的中间位置     
- cflag == 3:这是多条记录的结尾    

3.Data是用来保存数据内容的空间。    
4.Pad是一个pad区域用来保证每条记录对齐到4个字节。

当我们打包了数据之后，每个文件就包含多条记录。然后，读取就可以是连续的了。这将避免读取磁盘上任意位置导致的低性能。   
通过记录来存储数据的一个优点在于每一条记录可以是不定长的。这可以使我们在保存数据上比较简洁，特别是在有好的压缩算法的时候，比如说，我们用JPEG来保存图片数据，那么这个打包的数据会比直接存储未经过压缩的像素的RGB值要小的多。    
以ImageNet_1K数据集为例。加入我们存储的数据是3\*256\*256的一个RGB值的矩阵，那么整个数据集将达到200G多。而如果我们使用JPEG对普片进行压缩，它们只需要在磁盘空间上占用35G左右。这将极大地减少从磁盘读入数据的时间。     
下图是一个binary recordIO的例子。我们首先将图片resize到256\*256，然后压缩成JPEG的形式。之后我们为图片增加一个header用来指示这张图片的index和label，然后存储在记录的Data区域。然后我们将几张图片一起打包成一个文件。 
![](resources/ImageRecordIO.jpg)

### Access Arbitrary Parts Of Data
data loader的一个比较理想的属性是：打包好的数据可以在逻辑上被切成任意份，不管在物理上数据被打包成了多少份。由于binary recordIO可以利用魔数容易地定位到一条记录的头和尾的位置，因此我们可以利用dmlc-core中提供的InputSplit函数实现上述目标。     
InputSplit需要以下参数：

- FileSystem *filesys*：不同文件系统如hdfs,s3,local等的IO操作的dmlc-core wrapper。用户不应该担心不同文件系统的差别。
- Char *uri*：文件的URI。注意这可能是文件的列表，因为我们会把文件打包成多份，文件URIs通过“；”分割。
- Unsigned *nsplit*：逻辑分割的数目。*nsplit*可以和物理文件的数目不同。
- Unsigned *rank*：哪个split要加载进当前进程。

逻辑分割的过程如下：    

- 确定每一份的大小
![](resources/beforepartition.jpg)

- 根据文件大小将record大致分成指定份。注意每份的边界可能位于某条record的中间。
![](resources/approximatepartition.jpg)

- 调整每一份的起始位置，保证一条记录不会被分到不同的partition中。
![](resources/afterpartition.jpg)

通过上述操作，我们现在能够知道哪条记录属于哪个部分，哪个部分需要哪个物理数据文件。InputSplit很大程度上简化了数据并行，这样每个process只需要读取部分的数据即可。    
由于我们的分割不是依赖于物理文件的个数的，因此我们可以以并行的方式处理像ImageNet_22k这样大型的数据库，如下图所示。我们不再需要在准备数据的时候考虑分布式读取的事情，只需要根据数据集的大小和计算资源的多少选择合适的物理文件数目。
![](resources/parallelprepare.jpg)

## 数据读取和预处理
当数据的读取和预处理的速度跟不上训练／评估的速度时，IO可能成为整个系统的速度瓶颈。在这一章节中，我们将介绍一些tricks来实现更加高效地读取和预处理binary recordIO形式的数据。当在ImageNet数据集上使用的时候，我们的方法在一个HDD上实现了3000张图／秒的IO速度。
### Loading and preprocessing on the fly
当训练DNN时，我们有时候必须在训练的同时读取和预处理数据，这是因为：

- 当数据集的大小超过了可用的RAM大小时，我们不能事先完成读取
- 有时候为了使模型对平移／旋转／颜色变化等变换鲁棒，我们在训练的过程中会加入一些随机因素。这时候我们就必须在每次使用到每张图片的时候对它进行重新的预处理。

为了更加高效，我们提出多线程的机制。以Imagenet的训练为例，在读取了一组image records之后，我们开始以多线程的方式同时进行image decoding和image augmentation。这一过程如下图所示：
![](resources/process.jpg)

### Hide IO Cost Using Threadediter
降低IO消耗的一种方式是在一个线程中事先取出下一个batch的数据，同时在主线程中进行训练的前向和反向过程。为了支持更佳复杂的训练场景，MXNet利用dmlc-core中的threadediter来提供一个普适性的IO处理流程。threadediter的关键在于开启一个独立的线程用于提供数据，同时主线程则作为数据的使用方，如下图所示。    
threadediter保持一个固定大小的buffer，当buffer不满的时候自动填充它。并且，在buffer中的部分数据被使用后，threadediter会重新利用这部分空间来保存数据的下一部分。
![](resources/threadediter.png)

### MXNet IO Python Interface
一般地讲，创建一个数据迭代器需要实现下面讲到的五种参数:

- Dataset Param 提供数据集的基本信息, 比如说, 文件路径, 输入的数据的 shape.
- Batch Param 提供构建一个 batch 的信息, 比如说 batch size.
- Augmentation Param 指定输入数据的扩充方式 (e.g. crop, mirror).
- Backend Param 控制后端线程掩盖数据加载开销的行为.
- Auxiliary Param 提供的可选项, 用来帮助检查和 debug.

通常地讲, Dataset Param 和 Batch Param 必须提供, 否则 data batch 无法创建. 其他的参数根据算法和性能的需要来设置. 
下面的代码是如何创建一个 Cifar 的数据迭代器的代码.

```
dataiter = mx.io.ImageRecordIter(
    # Dataset Parameter, indicating the data file, please check the data is already there
    path_imgrec="data/cifar/train.rec",
    # Dataset Parameter, indicating the image size after preprocessing
    data_shape=(3,28,28),
    # Batch Parameter, tells how many images in a batch
    batch_size=100,
    # Augmentation Parameter, when offers mean_img, each image will subtract the mean value at each pixel
    mean_img="data/cifar/cifar10_mean.bin",
    # Augmentation Parameter, randomly crop a patch of the data_shape from the original image
    rand_crop=True,
    # Augmentation Parameter, randomly mirror the image horizontally
    rand_mirror=True,
    # Augmentation Parameter, randomly shuffle the data
    shuffle=False,
    # Backend Parameter, preprocessing thread number
    preprocess_threads=4,
    # Backend Parameter, prefetch buffer size
    prefetch_buffer=1)
```
从上面的代码中, 我们可以学到如何创建一个数据迭代器. 首先, 你需要明确的指出需要取哪种类型的数据(MNIST, ImageRecord 等等). 然后, 提供描述数据的可选参数, 比如 batching, 数据扩充方式, 多线程处理, 预取数据. MNNet 框架会检查参数的有效性, 如果一个必须的参数没有提供, 框架会报错.


#### 自定义data iter
MXnet中的data iterator和python中的迭代器是很相似的， 当其内置方法next被call的时候它每次返回一个databatch。所谓databatch，就是神经网络的data和label，一般是(n, c, h, w)大小的图片输入和(n)大小的label。直接上官网上的一个简单的例子来说说吧。
    
[dataIter](https://github.com/dmlc/mxnet/blob/4feb759fdcf401ca8b442887635a0f8425cae521/python/mxnet/io.py)

```
import numpy as np
class SimpleIter:
    def __init__(self, data_names, data_shapes, data_gen,
                 label_names, label_shapes, label_gen, num_batches=10):
        self._provide_data = zip(data_names, data_shapes)
        self._provide_label = zip(label_names, label_shapes)
        self.num_batches = num_batches
        self.data_gen = data_gen
        self.label_gen = label_gen
        self.cur_batch = 0

    def __iter__(self):
        return self

    def reset(self):
        self.cur_batch = 0        

    def __next__(self):
        return self.next()

    @property
    def provide_data(self):
        return self._provide_data

    @property
    def provide_label(self):
        return self._provide_label

    def next(self):
        if self.cur_batch < self.num_batches:
            self.cur_batch += 1
            data = [mx.nd.array(g(d[1])) for d,g in zip(self._provide_data, self.data_gen)]
            assert len(data) > 0, "Empty batch data."
            label = [mx.nd.array(g(d[1])) for d,g in zip(self._provide_label, self.label_gen)]
            assert len(label) > 0, "Empty batch label."
            return SimpleBatch(data, label)
        else:
            raise StopIteration
```

上面的代码是最简单的一个dataiter了，没有对数据的预处理，甚至于没有自己去读取数据，但是基本的意思是到了，一个dataiter必须要实现上面的几个方法，provide\_data返回的格式是(dataname, batchsize, channel, width, height)， provide\_label返回的格式是(label_name, batchsize),reset()的目的是每个epoch结束从头读取数据，通常情况下会做shuffle，即打乱读取图片的顺序，这样随机采样的话训练效果会好一点。next()的方法是用来返回你的databatch。需要注意的是，databatch返回的数据类型是mx.nd.ndarry。

## Data Loading API
### MXNet Data Iterator
1. mxnet中的所有IO都是通过`mx.io.DataIter`类及其子类来进行处理的。   
2. data iterators在每次请求`next`的时候则返回一个`DataBatch`，其中包括n个training examples和它们对应的labels。当读取到数据的末尾时，iterator会产生`StopIteration` exception。    
3. 另外，像名字，形状，类型，每个训练数据的layout（NCHW）等信息可以通过`DataDesc`这个数据描述体来保存，通过`DataBatch`中的`provide_data`和`provide_label`来调用。
4. 读取内存中的数据：NDArrayIter
5. 读取CSV文件中的数据：CSVIter
6. 自定义iterator:需要实现next()方法／reset()方法，提供provide_data()接口和provide_label()接口

#### ImageRecordIter
从.rec的RecordIO文件中读取image batches。这个iterator不太适合进行用户化定制，它由大量的不同语言的绑定，但是速度比较快。在raw images上进行迭代就直接使用ImageIter进行代替（是python的）。    
代码：[imagerecordIter](https://github.com/dmlc/mxnet/blob/4feb759fdcf401ca8b442887635a0f8425cae521/src/io/iter_image_recordio_2.cc)      
ImageRecordIter包含以下部分：
    
- Threaded Iter iter\_; 用于多线程预读取data batch
- PrefetcherParam prefetch\_param\_; 预取参数
- DataBatch *out\_; 输出
- std::queue<DataBatch*> recycle\_queue\_; 用于回收的已使用的data batch
- ImageRecordIOParser parser_; 解析recordIO生成数据（array）

其中最重要的部分是ImageRecordIOParser，包含以下部分：   
   
- ParseNext():从recordIO中得到下一个DataBatch，借助ParseChunk实现
- ParseChunk():
- CreateMeanImg()