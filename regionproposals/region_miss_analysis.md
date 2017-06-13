# Region Miss Analysis

## 检查漏检Region
* 画出来的框中，白色的框为所有的region proposal 的框均没有检测到的框(IOU < 0.5)
* 试着分析漏检的框的类型，例如

|类型|数目|例子|
|---|---|---|
|缺失严重|1|![](resouce/part.png)|
|光照变化|1|![](resouce/illution.png)|
|边缘物体|1|![](resouce/Edge.png)|
|极小物体|1|![](resouce/Tiny.png)|

大家有新的类型可以添加到表格中