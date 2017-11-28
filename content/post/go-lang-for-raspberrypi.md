---
title: "Raspberry Pi上安装Go lang并编译cow proxy"
date: 2013-06-14T11:48:41+08:00
draft: false
tags: [golang,raspberrypi,cowproxy]
---

【golang和cow都提供ARM版本了 2017.11.28 更新，文档更新了一下】

### 安装go语言

下载golang的ARM版本<https://golang.org/dl/>，如1.9.2版本是go1.9.2.linux-armv6l.tar.gz。

<!--more-->

解压到/home/pi/go目录即可

### 设置go语言编译环境变量

```
export GOROOT=/home/pi/go/go
export GOPATH=/home/pi/go/mygo
export PATH=$PATH:$GOROOT/bin
```

如果系统没有安装mercurial软件包，则需要用`apt-get`安装mercurial软件，cow proxy需要用到go语言的crypto package，`go get`会调用`hg`命令来获得。

```
sudo apt-get install mercurial
```

### 编译cow proxy

[cow proxy](https://github.com/cyfdecyf/cow)是[@cyfdecyf](http://twitter.com/cyfdecyf)用go语言编写的一个自动代理，代码开源，支持二级socks代理。  
用下面的命令编译

```
go get github.com/cyfdecyf/cow
```

如果上面的命令出现go build出错`signal: killed`，再单独build

```
go build github.com/cyfdecyf/cow
```

编译好的cow二进制文件位于/home/pi/go/mygo目录下。

cow官方已经提供ARM版本了<https://github.com/cyfdecyf/cow/releases>。

### 下一次更新代码再编译

```
go get -u  github.com/cyfdecyf/cow
```
