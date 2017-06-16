# Region Miss Analysis

## 检查漏检Region
* 画出来的框中，白色的框为所有的region proposal 的框均没有检测到的框(IOU < 0.5)
* 试着分析漏检的框的类型，例如

|类型|数目|例子|
|---|---|---|
|缺失严重|42/1000|![](resouce/part.png)|
|光照变化|3/1000|![](resouce/illution.png)|
|边缘物体|79/1000|![](resouce/Edge.png)|
|极小物体|225/1000|![](resouce/Tiny.png)|
|比例失调|44/1000|![](resouce/aspect.PNG)|
|物体重叠|25/1000|![](resouce/overlap.PNG)|
|严重形变|5/1000|![](resouce/deformable.PNG)|

大家有新的类型可以添加到表格中
