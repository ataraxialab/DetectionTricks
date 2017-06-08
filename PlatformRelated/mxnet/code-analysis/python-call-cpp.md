# python调用cpp分析

## 导入

把C&CPP函数导入python。这个地方主要用到了两个模块**cython**和**ctypes**。

### ctypes

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

### ctypes

ctypes的工作就是把mxnet编译好的动态链接库导出到python，来达到python调用C&CPP的目的。cython暴露出来的接口，都可以通过ctypes的导出。

导出代码：

```python
# file: mxnet/base.py:L52

_LIB = _load_lib()
```

有了**_LIB**就可以调用任何C&CPP暴露出来的函数。函数列表：mxnet/include/c_api.h

## 代码分析

mxnet的C&CPP中定义了一系列的关于ndarray和operator的函数，通过库*dmlc-core*中的类*Registry*暴露数据，通过库*nnvm*中的类*Op*统一了调用姿势。

### Registry

类Registry的功能是定义全局唯一数据实例。是一个模板类，模板参数为全局实例的类型，维护每个全局实例的名称到全局实例的映射关系。

#### 定义全局实例

```cpp
#define DMLC_REGISTRY_ENABLE(EntryType)                                 \
  template<>                                                            \
  Registry<EntryType > *Registry<EntryType >::Get() {                   \
    static Registry<EntryType > inst;                                   \
    return &inst;                                                       \
  }                                                                     \
```

以上代码通过显示实例化模板的方式定义了全局变量。

#### 新建全局实例

```cpp
#define DMLC_REGISTRY_REGISTER(EntryType, EntryTypeName, Name)          \
  static DMLC_ATTRIBUTE_UNUSED EntryType & __make_ ## EntryTypeName ## _ ## Name ## __ = \
      ::dmlc::Registry<EntryType>::Get()->__REGISTER__(#Name)           \
```



### ndarray

### operator(op)