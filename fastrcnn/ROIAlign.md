## ROI Pooling:
ROI pooling的操作包括两个部分：  
(1)	将图像上提取的ROI区域映射到某层feature map上得到对应的一块区域，记作ROI_f。  
(2)	对ROI_f划分bins，然后每个bin做pooling。  
上述两个部分都包含了取整的操作。在映射ROI_f的过程中存在取整，例如原来的图像上ROI位置为x,y,w,h,映射到feature map上假设stride为16，那么对应的ROI_f在feature map上的位置就是x/16的取整。另外，由于ROI_f区域不一定能被bin的数目整除，所以也存在取整的操作，具体的是对bin的开始位置做floor，结束位置做ceil  。

## ROI Align: 
为了解决上述取整带来的feature不准确的问题，提出了ROIAlign层。ROIAlign的改变很简单，拒绝任何的取整操作，直接在浮点数上进行运算。首先，在ROI映射时，直接保留浮点的ROI_f坐标。然后在做max pooling的时候如果遇到不为整数的坐标，则做双线性插值。  
具体的实现逻辑为：输入为整张feature map和ROIs，将ROI通过stride缩放到feature map的尺度上得到ROI_f，保留浮点数。然后对ROI_f划分bins。假设某个bin对应原图的[wstart,wend],[hstart,hend]区域，遍历上述区域所有点，得到最大值(max pooling)。若某点[w,h]不为整数坐标，则进行插值：取[w,h]周围的4个坐标，做双线性插值，得到[w,h]点的值。  

## ROI Pooling 代码解析：
.h文件：https://github.com/ataraxialab/mxnet/blob/master/src/operator/roi_pooling-inl.h  
.cu文件：https://github.com/ataraxialab/mxnet/blob/master/src/operator/roi_pooling.cu  
.cc文件：https://github.com/ataraxialab/mxnet/blob/master/src/operator/roi_pooling.cc  
.h文件进行ROIPooling的forward/backward函数声明，.cu文件和.cc文件具体实现gpu版本和cpu版本的ROIPooling。下面以gpu版本为例解析ROI Pooling代码。  

### 1.	ROIPoolForward: 
https://github.com/ataraxialab/mxnet/blob/master/src/operator/roi_pooling.cu#L89-L113
1)	定义输入：data表示输入的feature map；bbox表示输入的rois。  
2)	定义输出：out表示ROIPooling后的feature map；max_idx表示ROIPooling具体取的哪个位置的值，方便进行backward。  
3)	参数解析：pooled_height, pooled_width等。   
4)	然后传入到ROIPoolForwardKernel中进行具体计算。    
 
### 2.	ROIPoolForwardKernel:
https://github.com/ataraxialab/mxnet/blob/master/src/operator/roi_pooling.cu#L17-L87   
1)	计算原图的ROI区域在feature map上的ROI_f区域，注意这里有取整操作：   
https://github.com/ataraxialab/mxnet/blob/master/src/operator/roi_pooling.cu#L41-L48   
2)	对ROI_f区域划分bins：   
https://github.com/ataraxialab/mxnet/blob/master/src/operator/roi_pooling.cu#L49-L52   
3)	对于ROIPooling输出的每一个元素[ph,pw],它在ROI_f的一块区域内做pooling，注意这里有取整操作：  
https://github.com/ataraxialab/mxnet/blob/master/src/operator/roi_pooling.cu#L54-L61  
4)	进行max pooling,并保留最大值对应的idx：   
https://github.com/ataraxialab/mxnet/blob/master/src/operator/roi_pooling.cu#L71-L87  

### 3. ROIPoolBackwardAcc:    
https://github.com/ataraxialab/mxnet/blob/master/src/operator/roi_pooling.cu#L192-L216
1) 定义输入：in_grad表示从top layer输入的梯度；bbox表示输入的rois；max_idx表示ROIPooling具体取的哪个位置的值。
2）定义输出：out_grad
3）参数解析：pooled_height, pooled_width等。
4）然后传入到ROIPoolBackwardAccKernel中进行具体计算。

### 4. ROIPoolBackwardAccKernel：  
https://github.com/ataraxialab/mxnet/blob/master/src/operator/roi_pooling.cu#L116-L189      
1）取出当前需要计算梯度的bottom layer的元素：     
https://github.com/ataraxialab/mxnet/blob/master/src/operator/roi_pooling.cu#L122-L129   
2）遍历所有ROI,找出和当前元素有梯度更新关系的ROI，即ROI的区域要包含当前元素的坐标：      
https://github.com/ataraxialab/mxnet/blob/master/src/operator/roi_pooling.cu#L141-L151   
3）对于每一个满足上述要求的ROI,计算当前元素与ROI_f区域的哪些bins有关联：   
https://github.com/ataraxialab/mxnet/blob/master/src/operator/roi_pooling.cu#L153-L177   
4）对于有关联的bins，如果这个bin在做maxpooling时候的最大元素是当前元素，则进行梯度更新：   
https://github.com/ataraxialab/mxnet/blob/master/src/operator/roi_pooling.cu#L179-L189   

## ROIAlign代码结构解析：  
生成一个operator，比如ROIAlign需要实现以下方法：
1. ROIAlignParam:定义ROIAlign中的参数,包括pooled_size,spatial_scale.  
reference: https://github.com/ElaineBao/mxnet/blob/master/example/rcnn/rcnn/symbol/roi_align-inl.h#L30-L41  
```
struct ROIAlignParam : public dmlc::Parameter<ROIAlignParam>{
	TShape pooled_size; //表示ROIAlign输出feature map的大小，为tuple:(h,w)
	float spatial_scale; //表示ROIAlign输入feature map相对于原图的尺度，为小于1的浮点数
}
```
2. ROIAlignOp:主要实现ROIAlign operator的前向和反向传播的定义  
reference: https://github.com/ElaineBao/mxnet/blob/master/example/rcnn/rcnn/symbol/roi_align-inl.h#L43-L126  
```
class ROIAlignOp : public Operator {
private:
	ROIAlignParam param_;
public：
	explicit ROIAlignOp(ROIAlignParam p); //构造函数传入ROIAlignParam
	virtual void Forward(...){ //前向传播
		//check输入输出维度的正确性
		...
		//然后调用ROIAlignForward进行计算
		ROIAlignForward(...);				
	}
	virtual void Backward(...){ //反向传播
		//check输入输出维度的正确性
		...
		//然后调用ROIAlignBackwardAcc进行计算
		ROIAlignBackwardAcc(...);
	}
}
```
3. ROIAlignProp:主要实现外部接口，例如在ROIAlignProp中有一个 Operator* CreateOperator()调用ROIAlignOp创建具体的ROIAlignOp,但是ROIAlignProb还不是直接与外部有接口，需要进一步注册  
reference: https://github.com/ElaineBao/mxnet/blob/master/example/rcnn/rcnn/symbol/roi_align-inl.h#L133-L229  
4. 上述操作定义完成之后进行注册:注册时接口为ROIAlignProp，ROIAlign为注册的名字，add_argument是为了方便使用者得到该操作的操作参数。 
reference: https://github.com/ElaineBao/mxnet/blob/master/example/rcnn/rcnn/symbol/roi_align.cc#L277-L287   
```
DMLC_REGISTER_PARAMETER(ROIAlignParam);
MXNET_REGISTER_OP_PROPERTY(ROIAlign, ROIAlignProp)
	.describe("Performs region of interest(ROI) align on the input array.")
	.add_argument("data", "NDArray-or-Symbol", "The input array to the pooling operator, "
                                            " a 4D Feature maps ")
	.add_argument("rois", "NDArray-or-Symbol", "Bounding box coordinates, a 2D array of "
	"[[batch_index, x1, y1, x2, y2]], where (x1, y1) and (x2, y2) are top left and bottom right "
	"corners of designated region of interest. `batch_index` indicates the index of corresponding "
	"image in the input array")
	.add_arguments(ROIAlignParam::__FIELDS__());
```

## ROIAlign关键代码解析：
ROIAlignForward和ROIAlignBackwardAcc各自有.cu和.cc的实现版本，分别用于GPU和CPU的运算。下面以GPU版本为例解析ROIAlign的前向和反向传播代码。    
### 1. ROIAlignForward  
reference: https://github.com/ElaineBao/mxnet/blob/master/example/rcnn/rcnn/symbol/roi_align.cu#L127-L152  
1) 定义输入：data表示输入的feature map；bbox表示输入的rois。  
2) 定义输出：out表示ROIAlign后的feature map；max_idx_x,max_idx_y表示ROIAlign具体取哪个位置的值，方便进行backward。  
3) 参数解析：pooled_height, pooled_width等。   
4) 然后传入到ROIAlignForwardKernel中进行具体计算。
### 2. ROIAlignForwardKernel
reference: https://github.com/ElaineBao/mxnet/blob/master/example/rcnn/rcnn/symbol/roi_align.cu#L23-L124  
1) 计算原图的ROI区域在feature map上的ROI_f区域:  
https://github.com/ElaineBao/mxnet/blob/master/example/rcnn/rcnn/symbol/roi_align.cu#L48-L51  
2) 对ROI_f区域划分bins：   
https://github.com/ElaineBao/mxnet/blob/master/example/rcnn/rcnn/symbol/roi_align.cu#L54-L59  
3) 对于ROIAlign输出的每一个元素[ph,pw],它在ROI_f的一块区域内做pooling,计算这块区域的起止位置：  
https://github.com/ElaineBao/mxnet/blob/master/example/rcnn/rcnn/symbol/roi_align.cu#L61-L71  
4) 遍历区域的所有位置，由于遍历的位置(h,w)不一定为整数，因此需进行双线性插值。具体地，选取(h,w)相邻的4个位置，进行双线性插值
https://github.com/ataraxialab/mxnet/blob/master/src/operator/roi_pooling.cu#L71-L87  
### 3. ROIAlignBackward
reference: https://github.com/ElaineBao/mxnet/blob/master/example/rcnn/rcnn/symbol/roi_align.cu#L252-L278  
1) 定义输入：out_grad表示ROIAlign后的feature map的梯度，即为输入梯度；bbox表示输入的rois；max_idx_x和max_idx_y表示做ROIAlign时所取值的位置。  
2) 定义输出：in_grad表示前一层的梯度，即输出梯度。 
3) 参数解析：pooled_height, pooled_width等。   
4) 然后传入到ROIAlignBackwardAccKernel中进行具体计算。
### 4. ROIAlignBackwardAccKernel
reference: https://github.com/ElaineBao/mxnet/blob/master/example/rcnn/rcnn/symbol/roi_align.cu#L155-L249  
1) 计算原图的ROI区域在feature map上的ROI_f区域:  
https://github.com/ElaineBao/mxnet/blob/master/example/rcnn/rcnn/symbol/roi_align.cu#L174-L186   
2) 如果当前ROI_f区域包含所需要计算梯度的point (h,w),则继续计算(h,w)具体属于哪个bin,否则遍历下一个ROI：  
https://github.com/ElaineBao/mxnet/blob/master/example/rcnn/rcnn/symbol/roi_align.cu#L189-L218  
3) 如果(h,w)是max_idx_x,max_idx_y中记录的位置的4个相邻位置之一，则按照双线性插值进行求导。  
https://github.com/ElaineBao/mxnet/blob/master/example/rcnn/rcnn/symbol/roi_align.cu#L220-L249  

## ROIAlign的使用方法：
1. 新建容器：
例如：kirk services run your-container-name -i ataraxia/ava-training-mxnet-det:opencv3-py27-cuda8-cudnn5  --unit-type G_2U_TESLA_M40_24GB --cmd="sleep 999999" --metadata="NFS=/nfs/datastore:/disk2:rw"
2. 加入ROIAlign：
将roi_align-inl.h, roi_align.cu, roi_align.cc放入/opt/mxnet/example/rcnn/operator/下
3. 编译：
RUN `make` in `/opt/mxnet/`
4. 使用：
ROIAlign的使用方法和ROIPooling完全一样，例如，在symbol_resnet.py中，使用ROIPooling的姿势为：
```
roi_pool = mx.symbol.ROIPooling(
        name='roi_pool5', data=conv_feat, rois=rois, pooled_size=(14, 14), spatial_scale=1.0 / config.RCNN_FEAT_STRIDE)

```
则使用ROIAlign的姿势为：
```
roi_align = mx.symbol.ROIAlign(
        name='roi_align5', data=conv_feat, rois=rois, pooled_size=(14, 14), spatial_scale=1.0 / config.RCNN_FEAT_STRIDE)

```
