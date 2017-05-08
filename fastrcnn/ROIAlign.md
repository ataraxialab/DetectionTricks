## ROI Pooling:
ROI pooling的操作包括两个部分：
(1)	将图像上提取的ROI区域映射到某层feature map上得到对应的一块区域，记作ROI_f。
(2)	对ROI_f划分bins，然后每个bin做pooling。
上述两个部分都包含了取整的操作。在映射ROI_f的过程中存在取整，例如原来的图像上ROI位置为x,y,w,h,映射到feature map上假设stride为16，那么对应的ROI_f在feature map上的位置就是x/16的取整。另外，由于ROI_f区域不一定能被bin的数目整除，所以也存在取整的操作，具体的是对bin的开始位置做floor，结束位置做ceil。

## ROI Align:
为了解决上述取整带来的feature不准确的问题，提出了ROIAlign层。ROIAlign的改变很简单，拒绝任何的取整操作，直接在浮点数上进行运算。首先，在ROI映射时，直接保留浮点的ROI_f坐标。然后在做max pooling的时候如果遇到不为整数的坐标，则做双线性插值。

## ROI Align 具体实现逻辑：
输入为整张feature map和ROIs，将ROI通过stride缩放到feature map的尺度上得到ROI_f，保留浮点数。
然后对ROI_f划分bins。假设某个bin对应原图的[wstart,wend],[hstart,hend]区域，遍历上述区域所有点，得到最大值(max pooling)。若某点[w,h]不为整数坐标，则进行插值：取[w,h]周围的4个坐标，做双线性插值，得到[w,h]点的值。

## Roi align 代码（未完待续）：
https://github.com/ElaineBao/mxnet/blob/34736d184320b68e5d97fb2c16a4f56c073dbcca/example/rcnn/rcnn/symbol/roi_align.cu