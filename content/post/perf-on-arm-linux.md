---
title: "交叉编译perf(ARM Linux)"
date: 2018-05-02T09:14:37+08:00
draft: false
tags: [linux]
---

关键词：ARM linux perf

perf对于Linux性能分析非常有用。perf在linux上编译依赖几个库，库的编译问题不大，但是要打ARM架构的补丁不好操作。所以不如索性用buildroot制作一个和平台兼容的交叉编译链，在buildroot里自动选择上需要的库，让buildroot自动下载打补丁和编译，这样操作最省事省力。

<!--more-->

### 制作perf交叉编译链

下载buildroot，配置编译链，选择ARM架构指令集，选择C库，就算产品平台是uClibc，最好选择glibc，兼容性最好（用静态链接perf来解决C库冲突），选择Linux内核版本，同时选择libunwind、elfutils和libz库。假定编译链的CC命令制作成arm-perf-linux-gnueabi-gcc。

###  编译perf

进入到内核代码tools/perf目录（内核版本linux-3.4.113为例），配置如下：

```

export ARCH=arm
export CROSS_COMPILE=arm-perf-linux-gnueabi-
export LDFLAGS='-static'

```

说明：如果编译链的bin没有在用户$PATH里，CROSS_COMPILE可以配置成绝对路径。

然后执行make编译。

```

make

```

编译完成后，在perf目录会生成一个perf静态可执行程序。

```

$file perf
perf: ELF 32-bit LSB executable, ARM, version 1 (SYSV), statically linked, for GNU/Linux 2.6.32, not stripped

```


