做样本均衡的脚本程序

## 处理过程
原来的样本处理方法是每个类的图片放在一起，许多类组成一个train.txt，这时候每个类的图片是放在一起的，训练的之前对所有图片做一遍shuffle。
现在要对这些类别的图片做更加均匀的排列。首先从每一个类取一张图片，然后对类别做一遍shuffle，再从每一个类中取出一个图片，由此得到训练集列表。

 - 对于图片数量不够的类别，当该类中所有图片使用完一遍的时候，接下来对已经用过的图片做一些对比度和亮度等一些变化，再加入训练集中。
 - 对类别做shuffle是可选的，如果不想shuffle类别，则把脚本中的`shuflle_cls`变量设置为false。

## 需要修改的参数
假设数据集在`/disk2/data/VOCdevkit/VOCdevkit/VOC2007`目录下的`ImageSets`, `Annotations`, `JPEGImages`三个目录中,那么设置如下:

```
root_path = '/disk2/data/VOCdevkit/VOCdevkit/VOC2007'
txt_sub_path = 'ImageSets/Main/trainval.txt'
xml_sub_path = 'Annotations'
save_balanced_path = 'ImageSets/Main/trainvalbalanced.txt'
img_sub_path = 'JPEGImages'
image_postfix = '.jpg'
shuffle_cls = True
```

其中txt_sub_path, xml_sub_path, savapath都是相对于root_path的。即它们三个与root_path能够拼成绝对路径

`txt_sub_path`是image_set文件

`xml_sub_path`是annotations文件所在的目录

`sava_balanced_path`保存新生成的image_set文件

`img_sub_path`是图片所在的路径

`image_postfix`是训练集中的图片后缀

`shuffle_cls`为true的时候会在每次循环一遍所有类的时候对类别做一次shuffle

