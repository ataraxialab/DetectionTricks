# mxnet 代码分析计划

## 目标

1. 短期内理清mxnet整体使用流程，模块之间的交互的接口
2. 长期掌握mxnet代码细节，包括算法/数据结构/编程语言技巧，成为mxnet的维护者

## 代码版本

v0.9.5

## 分工

| 代码模块                | 责任人  |
| :------------------ | ---- |
| Data Loading(IO)    | 包包   |
| NDArray             | 包包   |
| Storage Allocator   | 包包   |
| Symbolic Execution  | 赵之健  |
| Symbol Construction | 赵之健  |
| Operators           | 赵之健  |
| KVStore             | 张凯   |
| Runtime Dependency  | 张凯   |
| Resource Manager    | 张凯   |
| python call cpp     | 张凯   |