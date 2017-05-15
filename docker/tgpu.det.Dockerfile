FROM ava-mxnet:gpu
LABEL maintainer "Qiniu ATLab <ai@qiniu.com>"

RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64 && \
    chmod +x /usr/local/bin/dumb-init 

RUN mkdir -p /var/run/sshd && mkdir -p /root/.ssh && mkdir -p /workspace
ADD shared/id_rsa* /root/.ssh/
RUN cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys && chmod 400 /root/.ssh/id_rsa

# 保证 ssh 之后 mxnet 环境可用
RUN echo "PYTHONPATH=$PYTHONPATH" >> ~/.ssh/environment && \
    echo "PermitUserEnvironment yes" >> /etc/ssh/sshd_config

RUN apt-get update && apt-get install -y vim git lrzsz python-tk
RUN pip install easydict 
RUN pip install matplotlib
RUN pip install Cython
RUN pip install scikit-image -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /opt/mxnet/example/rcnn
RUN bash script/additional_deps.sh
# RUN bash script/get_voc.sh
# RUN bash script/get_pretrained_model.sh

ADD shared/entrypoint.sh /workspace
RUN chmod 777 /workspace/entrypoint.sh
ENTRYPOINT ["/workspace/entrypoint.sh"]

LABEL com.qiniu.atlab.type = "mxnet.training"

