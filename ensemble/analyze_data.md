## Analyze data
### groundtruth box statistics:
![a.png](resources/gt_box_analysis.png)
![b.png](resources/gt_box_analysis2.png)
从上图中可以看出groundtruth boxes的scale(即面积)和aspect ratio的基本分布。  
对于scale而言，通常在fast rcnn中使用的scale为8，16，32，对应于原图即检测框的边长为128，256，512. 在计算mAP时，以IOU overlap>0.5为阈值筛选检测框，则上述三个尺度分别能够检测到的面积区间为：[128\*128／2,128\*128\*2], [256\*256/2,256\*256\*2], [512\*512/2, 512\*512\*2],取log2则为[13,15],[15,17],[17,19]. 因此以下在统计实验结果时为区分以上区间，共分为5组：[<13],[13,15],[15,17],[17,19],[>19]。   
对于aspect ratio而言，通常取0.5，1，2，取log2为-1，0，1.以下在统计时共分为6组:[<-2],[-2,-1],[-1,0],[0,1],[1,2],[>2]。

### detection result statistics:
1. constrained positive negative ratio:      

mAP for all  | ![](resources/ap_all.png)|
------------- |---------|
mAP for log\_area  | ![](resources/map_log_area.png)|
mAP for log\_aspect\_ratio | ![](resources/map_log_aspect_ratio.png)|

AP in log\_area range [<13] |![](resources/ap_<13.png)|
----|-----|
AP in log\_area range [13,15] |![](resources/ap_13~15.png)|
AP in log\_area range [15,17] |![](resources/ap_15~17.png)|
AP in log\_area range [17,19] |![](resources/ap_17~19.png)|
AP in log\_area range [>19] |![](resources/ap_>19.png)|

AP in log\_aspect_ratio range [<-2] |![](resources/ap_<-2.png)|
----|-----|
AP in log\_aspect_ratio range [-2,-1] |![](resources/ap_-2~-1.png)|
AP in log\_aspect_ratio range [-1,0] |![](resources/ap_-1~0.png)|
AP in log\_aspect_ratio range [0,1] |![](resources/ap_0~1.png)|
AP in log\_aspect_ratio range [1,2] |![](resources/ap_1~2.png)|
AP in log\_aspect_ratio range [>2] |![](resources/ap_>2.png)|

