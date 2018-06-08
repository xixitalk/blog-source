---
title: "nexus 6p更新系统"
date: 2018-06-06T15:51:04+08:00
draft: false
tags: [android]
---

## 备份数据

1. 备份联系人、短信和通话记录
1. 备份照片和各别目录如Download
1.  用钛备份备份应用，导出备份数据

## 下载Factory Images

从<https://developers.google.com/android/images>下载Factory Images，并在windows PC上解压。

<!--more-->

## 安装新系统

按电源键+音量(-)键，进入bootloader，在Factory Images的解压目录，运行下面命令。

PS：*android bootloader驱动和 fastboot.exe命令都要准备好*。

```
flash-all.bat
```

更新完毕会自动重启进入系统，这是一个崭新的系统。设置新系统，连接网络，用浏览器下载magisk root工具。

下载[最新的magisk](http://tiny.cc/latestmagisk)，比如Magisk-v16.0.zip，用手机浏览器下载到Download目录。

## 安装twrp recovery

从twrp下载适合nexus 6p最新版本<https://dl.twrp.me/angler/>,系统关机后按电源键+音量(-)键，进入bootloader，执行：

```
fastboot flash recovery twrp-3.2.1-0-angler.img
```

## magisk root工具

Magisk 的[xda页面](https://forum.xda-developers.com/apps/magisk/official-magisk-v7-universal-systemless-t3473445)

在bootloader，再进入到twrp recovery界面，输入解密密码，点击install，选择Download目录的Magisk-v16.0.zip进行安装。安装后重启到系统。

##  恢复数据

1. 安装钛备份恢复数据，恢复应用和设置
1. 恢复短信、联系人和通话记录


