# python调用cpp分析

## 导入

把C&CPP函数导入python。这个地方主要用到了两个模块**cython**和**ctypes**。

### 模块ctypes

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

cython代码编译完成以后会根据python的版本分别生成两个模块*_c2*和*_c3*供使用。

通过环境变量`MXNET_ENABLE_CYTHON`控制 源代码`mxnet/symbol.py`和`mxnet/ndarray.py`是否使用cython。

### 模块ctypes

ctypes的工作就是把mxnet编译好的动态链接库导出到python，来达到python调用C&CPP的目的。cython暴露出来的接口，都可以通过ctypes的导出。

导出代码：

```python
# file: mxnet/base.py:L52

_LIB = _load_lib()
```

有了**_LIB**就可以调用任何C&CPP暴露出来的函数。函数列表：mxnet/include/c_api.h

## 代码分析

mxnet的C&CPP中定义了一系列的关于ndarray和operator的函数，通过库*dmlc-core*中的类*Registry*暴露数据，通过库*nnvm*中的类*Op*统一了调用姿势。

### 类Registry

类Registry的功能是定义全局唯一数据实例仓储。一个模板类，模板参数为全局实例的类型，内部维护了每个全局实例的名称到全局实例的映射关系。

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

以上代码通过显示实例化模板的方式定义了全局变量。

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

类Op的功能是抽象mxnet中函数(操作，例如加减乘除、卷积等等)。在mxnet中如果你要暴露一个函数，必须通过Op来定义输入，输出的个数以及类型。另外，Op还涉及到其他计算相关的信息。

所有的Op实例都维护在一个全局的Registry当中。

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

`OperatorProperty`：封装operator的参数返回值等等有关Operator的信息，提供创建Operator接口。

`Operator`：封装了两个核心函数`Forward`/`Backword`。

`Parameter`：封装参数，一个结构体包含某个操作所需要的所有参数，通过记录字段的偏移量来访问字段，目的是可以通过字段的名字来访问字段。

新版本

暂时没有实现的代码。

### 代码流程

*TODO*