# Region Proposal Tricks

## CRAFT 方法
* CRAFT训练RPN方法
  * 按照标准流程训练RPN
  * RPN的输出，每个训练图片生成2000个Proposals，训练二元的Fast RCNN。训练时挑选正负样本的方式与RPN一致：IoU >0.7 as Pos, <0.3 as Neg
  * RPN和FRSN的训练，不共享参数

* CRAFT的测试方法
  * 运行RPN，得到2000个Proposals
  * 在2000个Proposals上运行FRCN，得到final Proposals
  * 经过suppression或thresholding，获取少于300个Proposals
