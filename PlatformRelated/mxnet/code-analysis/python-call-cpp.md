<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [python调用cpp分析](#python%E8%B0%83%E7%94%A8cpp%E5%88%86%E6%9E%90)
  - [导入](#%E5%AF%BC%E5%85%A5)
    - [模块cython](#%E6%A8%A1%E5%9D%97cython)
    - [模块ctypes](#%E6%A8%A1%E5%9D%97ctypes)
  - [代码分析](#%E4%BB%A3%E7%A0%81%E5%88%86%E6%9E%90)
    - [类Registry](#%E7%B1%BBregistry)
        - [定义全局实例仓储](#%E5%AE%9A%E4%B9%89%E5%85%A8%E5%B1%80%E5%AE%9E%E4%BE%8B%E4%BB%93%E5%82%A8)
        - [添加实例](#%E6%B7%BB%E5%8A%A0%E5%AE%9E%E4%BE%8B)
        - [核心源代码](#%E6%A0%B8%E5%BF%83%E6%BA%90%E4%BB%A3%E7%A0%81)
      - [类Op](#%E7%B1%BBop)
        - [定义全局函数仓储](#%E5%AE%9A%E4%B9%89%E5%85%A8%E5%B1%80%E5%87%BD%E6%95%B0%E4%BB%93%E5%82%A8)
        - [定义函数](#%E5%AE%9A%E4%B9%89%E5%87%BD%E6%95%B0)
        - [核心源代码](#%E6%A0%B8%E5%BF%83%E6%BA%90%E4%BB%A3%E7%A0%81-1)
    - [ndarray函数](#ndarray%E5%87%BD%E6%95%B0)
        - [legacy版本](#legacy%E7%89%88%E6%9C%AC)
        - [新版本](#%E6%96%B0%E7%89%88%E6%9C%AC)
    - [symbol(operator)函数](#symboloperator%E5%87%BD%E6%95%B0)
        - [legacy版本](#legacy%E7%89%88%E6%9C%AC-1)
        - [新版本](#%E6%96%B0%E7%89%88%E6%9C%AC-1)
    - [代码流程](#%E4%BB%A3%E7%A0%81%E6%B5%81%E7%A8%8B)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# python调用cpp分析

## 导入

把C&CPP函数导入python。这个地方主要用到了两个模块**cython**和**ctypes**。

### 模块cython

cython 在python sdk中是一个可选项，主要提供初始化*ndarray*,*_ndarray_internal*,*_symbol_internal*和*symbol*模块接口，导出CPP中的*ndaray*和*operator*函数到python的相应模块。

接口代码：

```python
# file: cython/symbol.pyx
def _init_symbol_module(symbol_class, root_namespace):
	'''导出C&CPP中的operator到python的symbol模块'''
    
# file: cython/ndarray.pyx
def _init_symbol_module(symbol_class, root_namespace):
	'''导出C&CPP中的ndarray的operator到python的ndarray模块'''
```

cython代码编译完成以后会根据python的版本分别生成两个模块 *_c2* 和 *_c3* 供使用，*_c2* 对应python2，*_c3 * 对应python3。

通过环境变量`MXNET_ENABLE_CYTHON`控制源代码`mxnet/symbol.py`和`mxnet/ndarray.py`是否使用cython导出C&CPP代码。

### 模块ctypes

ctypes的工作就是把mxnet编译好的动态链接库导出到python，来达到python调用C&CPP的目的。通过cython导出来的接口，都可以通过ctypes的导出。

导出代码：

```python
# file: mxnet/base.py:L52

_LIB = _load_lib()
```

有了**_LIB**就可以调用任何C&CPP暴露出来的函数。函数列表：include/mxnet/c_api.h

## 代码分析

mxnet的C&CPP中定义了一系列的关于ndarray和operator的函数，通过库*dmlc-core*中的类*Registry*暴露数据，通过库*nnvm*中的类*Op*统一了调用姿势。

### 类Registry

类Registry的功能是定义全局唯一数据实例仓储。它一个模板类，模板参数为全局实例的类型，内部维护了每个全局实例的名称到全局实例的映射关系。

##### 定义全局实例仓储

```cpp
// file: nnvm/dmlc-core/include/dmlc/registry.h
#define DMLC_REGISTRY_ENABLE(EntryType)                                 \
  template<>                                                            \
  Registry<EntryType > *Registry<EntryType >::Get() {                   \
    static Registry<EntryType > inst;                                   \
    return &inst;                                                       \
  }                                                                     \
```

以上代码通过显式实例化模板的方式定义了全局变量。

##### 添加实例

```cpp
// file: nnvm/dmlc-core/include/dmlc/registry.h

#define DMLC_REGISTRY_REGISTER(EntryType, EntryTypeName, Name)          \
  static DMLC_ATTRIBUTE_UNUSED EntryType & __make_ ## EntryTypeName ## _ ## Name ## __ = \
      ::dmlc::Registry<EntryType>::Get()->__REGISTER__(#Name)           \
```

以上代码在已经定义好的全局实例仓储中，添加一个实例，同时用一个名字来指代。

##### 核心源代码

nnvm/dmlc-core/include/dmlc/registry.h

#### 类Op

类`Op`的功能是抽象mxnet中函数(操作，例如加减乘除、卷积等等)。在mxnet中如果你要暴露一个函数，必须通过`Op`来定义输入，输出的个数以及类型。另外，`Op`还涉及到其他计算相关的信息。

所有的`Op`实例都维护在一个全局的Registry当中。

##### 定义全局函数仓储

```cpp
// file: nnvm/src/op.cc:L16

DMLC_REGISTRY_ENABLE(nnvm::Op);
```

##### 定义函数

```cpp
// file nnvm/include/nnvm/op.h:L369
#define NNVM_REGISTER_OP(OpName)                                        \
  DMLC_STR_CONCAT(NNVM_REGISTER_VAR_DEF(OpName), __COUNTER__) =         \
      ::dmlc::Registry<::nnvm::Op>::Get()->__REGISTER_OR_GET__(#OpName)
```

##### 核心源代码

nnvm/include/nnvm/op.h

nnvm/src/op.cc

### ndarray函数

##### legacy版本

```cpp
#define NVM_REGISTER_OP(name)                                 \
  DMLC_REGISTRY_REGISTER(::mxnet::NDArrayFunctionReg, NDArrayFunctionReg, name)
```

##### 新版本

通过宏`NNVM_REGISTER_OP`定义。

### symbol(operator)函数

##### legacy版本

主要三个接口来实现，分别是：`OperatorProperty`,`Operator`,`Parameter`，在`MXListAllOpName`函数中把`OperatorProperty`转换成`Op`。

`OperatorProperty`：封装operator的参数返回值等等有关`Operator`的信息，提供创建`Operator`接口。

`Operator`：封装了两个核心函数`Forward`/`Backward`。

`Parameter`：封装参数，是一个结构体包含某个操作所需要的所有参数，通过记录字段的偏移量来访问字段，目的是可以通过字段的名字来访问字段。

##### 新版本

暂时没有实现的代码。

### 代码流程

*TODO*