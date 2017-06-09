# DeepMask
## 论文阅读
参见我的博客：[【论文笔记】物体检测与分割系列 DeepMask](http://blog.csdn.net/elaine_bao/article/details/72967800)

## DeepMask代码
使用DeepMask为Imagenet val数据集提取region proposals, 代码在[computeProposals.lua](https://github.com/ElaineBao/deepmask/blob/master/computeProposals.lua)，由于lua貌似没有cPickle可以直接生成pkl文件，所以这里首先将region proposals存在了txt里。     
那为了和Fast RCNN的输入输出格式对齐，另外写了一个[text2pkl.py](https://github.com/ElaineBao/deepmask/blob/master/text2pkl.py)来进行格式的转换。

### 1. 代码解析
- 参数设置：

|-model| 预训练模型path |
|-----|-----|
|-imglist|imglist path，默认为 /disk2/data/ILSVRC2017/ILSVRC/ImageSets/DET/val.txt|
|-datapath|图片存储的根目录，默认为/disk2/data/ILSVRC2017/ILSVRC/Data/DET/val/ |
|-gpu|使用哪个gpu，默认为1|
|-np|输出的proposal的个数，默认为500|
|-si|图像scale的起始值，默认为-2.5，表示2^(-2.5)|
|-sf|图像scale的终止值，默认为2.，表示2^2|
|-ss|图像scale的step,默认为.5|
|-dm|是否使用DeepMask version of SharpMask，默认为false|


- [load image](https://github.com/ElaineBao/deepmask/blob/master/computeProposals.lua#L86-L98)
- [mask和objectness score](https://github.com/ElaineBao/deepmask/blob/master/computeProposals.lua#L102-L105)
- [从mask生成bbox](https://github.com/ElaineBao/deepmask/blob/master/computeProposals.lua#L110-L111)
- [保存bbox的结果，输出](https://github.com/ElaineBao/deepmask/blob/master/computeProposals.lua#L115-L127)

### 2. 使用姿势
- 输入一张图片，输出带segmentation结果的图片：

```
th computeProposals_singleimg.lua /path/to/trained/model/ -img /path/to/test/image
```
- 输入一个list，输出list中所有图片的region proposals，保存在txt里：

```
th computProposals.lua /path/to/trained/model/ -imglist /path/to/image/list -datapath /path/to/img/data/
```
- 存放region proposals的txt转换成pkl文件：   

```
python test2pkl.py /region/proposal/txt /save/to/pkl/path
```