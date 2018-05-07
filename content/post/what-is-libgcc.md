---
title: "libgcc是什么"
date: 2018-05-07T11:34:13+08:00
draft: false
tags: [tech,linux]
---

一个产品flash空间非常小，只有16MB，所以不必要的东西都要裁剪掉。一次有个研发问我：发现有个程序如果缺失`libgcc_s.so.1`，pthread_join()就会运行不正常，但是无论是`ldd`还是`readelf -d`都没有发现依赖`libgcc_s.so.1`。搜索得知PC linux上也大量类似`libgcc_s.so.1 must be installed for pthread_cancel to work`的问题。

<!--more-->

##  libgcc是什么

这是gcc官方的解释，<https://gcc.gnu.org/onlinedocs/gccint/Libgcc.html>  ，这里有个中文版<http://gccint.cding.org/Libgcc.html>，最明显的看到了整型和浮点数的转换，而产品平台正好是**软浮点**。

libgcc的静态库是libgcc.a，动态库是libgcc_s.so.1(libgcc_s.so指向libgcc_s.so.1)。

>> libgcc是GCC提供的一个低层运行时库，当一些操作/运算在特定平台上不支持时，GCC会自动生成对这些库函数的调用，使用这些库函数来模拟实现。从概念上和源码实现中，又可以分为libgcc1和libgcc2，虽然它们最终会被编译合并为libgcc.a。
>
> From《libgcc1和libgcc2的区别》

## 是否需要libgcc_s.so.1

搜索到下面一个信息 <https://wiki.osdev.org/Libgcc>

> ####   When do I need to link with libgcc?
>  All code compiled with GCC must be linked with  libgcc.

## 结论

这种底层的库，还是加到文件系统比较安全。

## 参考资料

[libgcc1和libgcc2的区别](https://www.hellogcc.org/?p=33412)



