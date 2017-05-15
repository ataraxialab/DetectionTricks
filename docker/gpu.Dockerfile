FROM nvidia/cuda:8.0-cudnn5-devel
LABEL maintainer "Qiniu ATLab <ai@qiniu.com>"

RUN sed -i s/archive.ubuntu.com/mirrors.163.com/g /etc/apt/sources.list
RUN sed -i s/security.ubuntu.com/mirrors.163.com/g /etc/apt/sources.list

# apt-get && python && pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates wget vim lrzsz curl git unzip build-essential cmake \
    python-dev python-pip \
    libatlas-base-dev libopencv-dev libcurl4-openssl-dev \
    libgtest-dev \
    openssh-server rsync && \
    cd /usr/src/gtest && cmake CMakeLists.txt && make && cp *.a /usr/lib && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# pip
RUN pip install -U pip setuptools && pip install nose pylint numpy nose-timer requests

# opencv 3
RUN export OPENCV_CONTRIB_ROOT=/tmp/opencv-contrib OPENCV_ROOT=/tmp/opencv OPENCV_VER=3.2.0 && \
    git clone -b ${OPENCV_VER} --depth 1 https://github.com/opencv/opencv.git ${OPENCV_ROOT} && \
    git clone -b ${OPENCV_VER} --depth 1 https://github.com/opencv/opencv_contrib.git ${OPENCV_CONTRIB_ROOT} && \
    mkdir -p ${OPENCV_ROOT}/build && cd ${OPENCV_ROOT}/build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=OFF -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=${OPENCV_CONTRIB_ROOT}/modules \
    -D WITH_CUDA=ON -D BUILD_opencv_python2=ON -D BUILD_EXAMPLES=OFF .. && \
    make -j"$(nproc)" && make install && ldconfig && \
    rm -rf /tmp/*

# mxnet
ENV MXNET_ROOT=/opt/mxnet MXNET_VER=v0.9.3

WORKDIR $MXNET_ROOT
RUN git clone -b ${MXNET_VER} --depth 1 --recursive https://github.com/dmlc/mxnet . && \
    pip install -U pip setuptools && pip install nose pylint numpy nose-timer requests && \
    make -j"$(nproc)" USE_DIST_KVSTORE=1 USE_CUDA=1 USE_CUDA_PATH=/usr/local/cuda USE_CUDNN=1 && \
    rm -rf build

ENV PYMXNET_ROOT=$MXNET_ROOT/python
ENV PYTHONPATH=$PYMXNET_ROOT:$PYTHONPATH

WORKDIR /workspace
# 将时区改成 GMT+8
RUN wget http://ooc9uea7n.bkt.clouddn.com/docker/PRC-tz -O /tmp/PRC-tz && mv /tmp/PRC-tz /etc/localtime
LABEL com.qiniu.atlab.os = "ubuntu-16.04"
LABEL com.qiniu.atlab.type = "mxnet"

