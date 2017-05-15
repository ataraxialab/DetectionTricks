# 基础镜像

* 基础镜像： mxnet
* 训练镜像：
    * 提供 entrypoint.sh，使用 dumb-init 为 PID=1 进程规避 \<defunc\> 问题
    * 后台运行 sshd 方便分布式集群（镜像包含一个共享的 sshkey 用于相互 ssh, 用于 **切勿用于其他场合**）。

```bash
$ docker build -t ava-mxnet:gpu -f gpu.Dockerfile .
$ docker build -t ava-training-mxnet:gpu -f tgpu.det.Dockerfile .
```
