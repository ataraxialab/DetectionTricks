## Multiscale Training:
在训练的时候，对图片的大小不再固定，而是可变地采用不同大小的输入。
以Faster RCNN为例，通常我们会采用resize图片的短边为600，长边最多截取1000的方法。
当然，也可以采取短边800，1000之类的。但是一旦固定，在训练的时候就不再更改。
而Multiscale Training的意思则是训练的时候设定可取如短边（600，800，1000）中的任意一个。

## Multiscale Training 代码解析：
修改的地方很简单，将MXNET_ROOT/example/rcnn/rcnn/config.py文件中
```
config.SCALES = [(600, 1000)]  # 前一个为短边长度; 后一个为长边的最长长度
```
改为所想要取的多个scale即可。例如：
```
config.SCALES = [(600, 1000), (800, 1333), (1000, 1666)]
```
       
这是因为mxnet rcnn中在get_image的时候会自动从config.SCALES中random一个scale出来，如下：
reference: https://github.com/ataraxialab/mxnet/blob/master/example/rcnn/rcnn/io/image.py#L28-L31
```
scale_ind = random.randrange(len(config.SCALES))
target_size = config.SCALES[scale_ind][0]
max_size = config.SCALES[scale_ind][1]
im, im_scale = resize(im, target_size, max_size, stride=config.IMAGE_STRIDE)
```