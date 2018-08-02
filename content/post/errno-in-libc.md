---
title: "标准C库里的errno是怎么实现的？"
date: 2018-08-02T14:36:18+08:00
draft: false
tags: [tech]
---

首先`errno`是个全局变量，刚开始UNIX/Linux只有进程，这样多进程也是安全的。但是后来有了线程，线程间是可以共享全局变量的，这样`errno`就线程不安全了。解决办法是线程实现TLS(Thread Local Storage)，每个线程都有一个`errno`变量。

<!--more-->

> errno is defined by the ISO C standard to be a modifiable lvalue of type int, and must not be explicitly declared; errno may be a macro. errno is thread-local; setting it in one thread does not affect its value in any other thread.

如uClibc里的定义`./libc/misc/internals/errno.c`，glibc是`csu/errno.c`。

```c
	__thread int errno;
```

这依赖编译器打开TLS特性，很多嵌入式编译链不一定打开。运行`arm-linux-uclibcgnueabi-gcc -v`来检查，如果看到`--enable-tls`就是编译链打开TLS特性，这样编译链支持`__thread`或者`thread_local `关键词。

如果是C库是可配置的，C库的TLS也要打开，如uClibc，查看`include/bits/uClibc_config.h`文件，查找是否有下面选项：

```c
#define __UCLIBC_HAS_TLS__ y
```

## 参考资料

1.  [Is errno thread-safe?](https://stackoverflow.com/questions/1694164/is-errno-thread-safe)
2.  [Thread_Local_Storage](https://wiki.osdev.org/Thread_Local_Storage)


