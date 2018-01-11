---
title: "内核硬浮点VFP开关"
date: 2018-01-11T11:50:48+08:00
draft: false
tags: [linux]
---

一个产品编译链打开了VFPv3开关，重新编译版本后发现内核启动init失败。

<!--more-->

失败信息如下：

```
Kernel panic - not syncing: Attempted to kill init! exitcode=0x00000004
```

通过新旧内核和新旧文件系统交叉对比发现，是内核出现异常了。init程序属于busybox。网上大部分说是EABI不兼容，但是这部分没有修改，和之前一致。唯一区别是VFP。

```
$arm-linux-readelf  -A  vmlinux
...
Tag_FP_arch: VFPv2
...
$arm-linux-readelf  -A  busybox
...
Tag_FP_arch: VFPv3
...
```

搜索发现内核可以配置VFPv3，打开内核`CONFIG_VFP`和`CONFIG_VFPv3`选项问题解决。


