---
title: "编译stunnel"
date: 2016-10-19T09:21:51+08:00
draft: false
tags: [stunnel]
---

现在最新的stunnel是v5.36，而很多平台都还是`stunnel4`

<!--more-->

[下载](https://www.stunnel.org/downloads/stunnel-5.36.tar.gz)stunnel-5.36.tar.gz，解压。

```
wget https://www.stunnel.org/downloads/stunnel-5.36.tar.gz
tar -zxvf stunnel-5.36.tar.gz
```

用`./configure --help`查看编译配置选项。

```
cd stunnel-5.36
./configure --help
```

配置选项中`--with-threads`可以配置成`ucontext`、`pthread`或者`fork`，默认是`pthread`。如果是`pthread`模式，创建一个线程处理每个连接；如果是`fork`模式，创建一个进程处理每个连接。用`ps aux | grep stunnel`查看，如果很多个`stunnel`进程，则是`fork`模式；如果只有一个`stunnel`进程，那就是`ucontext`或者`pthread`模式。`ucontext`实现了用户空间一个进程中上下文切换，用这种机制可以实现协程（Coroutine），从资源利用上来说`ucontext`比`pthread`和`fork`更好一点。`fork`方式稳定性和安全性应该最好，一是代码最简单，二是进程独立空间。`pthread`是默认配置，稳定性也有保障。

用`configure`生成`Makefile`，下面配置选项含义：禁用`ipv6`，禁用[fips][fips_www]，禁用TCP Wrappers，每个网络连接创建一个线程处理。选项根据自己需要增删。

备注：TCP Wrappers作用是用`/etc/hosts.allow` 和 `/etc/hosts.deny`进行IP地址过滤，属于安全增强。

```
./configure --disable-ipv6 --disable-fips --disable-libwrap --with-threads=pthread
```

生成`Makefile`之后，`make`进行编译。

```
make
```

`make`编译完成编译好的stunnel位于`src/stunnel`，根据发行版本配置启动。我偷懒，直接覆盖了原来安装的`/usr/bin/stunnel4`命令，其他的脚本还用`stunnel4`的，目前没有发现问题。

```
sudo service  stunnel4  stop
sudo cp /usr/bin/stunnel4 /usr/bin/stunnel4.backup
sudo cp src/stunnel /usr/bin/stunnel4
sudo service  stunnel4  start
```


[fips_www]:https://en.wikipedia.org/wiki/Federal_Information_Processing_Standards "fips"




