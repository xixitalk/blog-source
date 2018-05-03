---
title: "模块unsupported RELA relocation:275错误"
date: 2018-05-03T14:58:17+08:00
draft: false
tags: [linux]
---

ARM A53芯片有个Erratum，编号是843419，在linux内核打开修正选项（CONFIG_ARM64_ERRATUM_843419）后，一些模块（ko）会insmod失败，提示：

<!--more-->

```
module xxx: unsupported RELA relocation:275
insmod: can't sinert xxx.ko: invalid module
```

当内核打开这个选项后，在模块的CFLAGS里增加了`-mcmodel=large`选项。而有些ko模块是自有编译框架，没有继承内核的编译选项，没有追加`-mcmodel=large`选项，所以造成insmod错误。

**解决办法:**就是在模块的CFLAGS里也增加`-mcmodel=large`选项。

检查方法1：确保ko文件进行反汇编没有adrp指令：

```
aarch64-linux-objdump -d xxx.ko ｜grep adrp
```

检查方法2：重定位信息没有`R_AARCH64_ADR_PRE`

```
aarch64-linux-readelf  -r xxx.ko  | grep R_AARCH64_ADR_PRE
```

如果仅增加`-mcmodel=large`选项还解决不了问题，可以试试下面的选项：

```
 -mcmodel=large -mfix-cortex-a53-843419 
```

