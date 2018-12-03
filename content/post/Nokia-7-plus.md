---
title: "Nokia 7 Plus手机体验"
date: 2018-08-24T09:15:38+08:00
draft: false
tags: [life]
---

### 软件系统 

系统android Oreo 8.1，现在是8月份，可以升级到7月份的安全补丁版本。并且声称9月份提供android pie 9正式版。软件开发和安全更新很及时，超越绝大多数android手机厂商。

<!--more-->

大陆国行版（型号TA-1062 版本号00CN开头）内置了微信、微博和支付宝应用，可以卸载，还有如下内置国产应用不能卸载：

- 内建与应用宝内容合作提供的应用商店，可以停用
- 内建浏览器似乎是由 QQ 浏览器技术支持，可以停用
- 内建小源科技提供的智能短信识别功能，可以停用
- 内建腾讯技术支持的手机管家，不能停用
- 内建 HMD Nokia 的云账号备份／同步系统

大陆国行版不带Google全家桶，但是用自带应用商店可以直接安装Google Play官方商店，安装后加上代理可以直接登录Google账号，登录Google Play。下载chrome浏览器、gmail、twitter一切正常，和原生android没有差异。

网上说可以刷国际版ROM，但是有人说bootloader没有解锁有基带丢失的风险，还有什么启动要解锁码。

### 性能和功耗

高通660 CPU性能足够用，功耗控制优异，几乎没有发烫的情况。支持18W快充3800毫安电池也令人心安。

### 对付流氓应用方法

目前Nokia手机解锁bootloader和root系统都比较麻烦，root后系统也不方便OTA。建议还是用官方系统，也不root系统。这样的话冰箱之类软件无法使用。系统提供**锁屏清理**，可以配置允许**自动唤醒**和**锁屏保留**的应用，这样锁屏后系统会及时清理流氓应用，并阻断唤醒。再加上绿色守护+island，不给权限不让使用的应用用island隔离起来，使用起来体验还算不错。

### 照相效果

照相效果一般，[Nokia 8的DXOMARK分数是68](https://www.dxomark.com/nokia-8-review-nokias-return-high-end-segment/)，可以类比一下,Nokia 7 plus的分数不会比它高。不要对照相有太多的期望，光线好的时候成相还不错，毕竟是双摄，还可以打开美颜。

### 缺点

自带的应用市场、浏览器、手机管家都无法卸载，应用市场和浏览器可以停用，但手机管家无法停用。照相效果一般。硬件配置同类手机价值1700￥左右（小米6X  6G/64G），300￥的Nokia情怀+原生android就看你觉得值不值了。

### 后续：刷android Pie beta版

方法是：下载B2N-3150-0-00WW-B04-update.zip，重命名成 B2N-3150-0-00CN-B04-update.zip放到内置存储根目录，拨号`*#*#874#*#*`按照提示升级即可。目前看起来一切正常，这个是最后一个beta版本，bug应该很少了，可以做主力使用。  
**建议：升级前备份数据，退出google账号，恢复系统到出厂状态，然后再拨号升级**。

### 再后续：刷android Pie 正式版

HMD发布了Nokia 7 Plus的android Pie正式版，[新闻在此](https://www.nokiacamp.com/stable-android-pie-update-for-nokia-7-plus-is-now-available/)。

可以下载软件包，手动刷机。软件包[下载地址在此](https://redirector.gvt1.com/packages/data/ota-api/nokia_b2nsprout_onyx00ww/105d70f18f853101a4e4d47f66b60a97318bc589.zip)。

方法：进 recovery 通过在电脑上adb sideload 刷机。   
注意：最好备份数据、登出 Google 账号和清空数据再刷机。

作为主力机使用了半个月，体验一切正常。

### 手动更新android Pie 2018.10月份安全补丁

手动更新来自[xda](https://forum.xda-developers.com/nokia-7-plus/development/ota-nokia-7-plus-ota-links-t3818774)。

先下载[WW 3.22C_SP01 October 2018 (B2N-322D-0-00WW-B01-update.zip)](https://android.googleapis.com/packages/ota-api/nokia_b2nsprout_onyx00ww/d734e46db890dc1ca67009c7341f0c2b5da22e87.zip)，下载文件重命名**B2N-322D-0-00WW-B01-update.zip**，放在手机内存存储空间根目录。手机拨号 `*#*#874#*#*`会提示系统更新，按照提示操作即可。升级完重启系统，从设置里查看**关于手机**，手机版本号变成**00WW_3_22C_SP01**，从**系统更新**里可以看到安全补丁程序级别是2018年10月1日。

### 手动更新android Pie 2018.11月份安全补丁

手动更新来自[xda](https://forum.xda-developers.com/nokia-7-plus/development/ota-nokia-7-plus-ota-links-t3818774)。

升级包[下载页面](https://androidfilehost.com/?fid=11410963190603861728)，下载文件名为**B2N-339B-0-00WW-B03-322D-0-00WW-B01-update.zip**，放在手机内存存储空间根目录。手机拨号 `*#*#874#*#*`会提示系统更新，按照提示操作即可。升级完重启系统，从设置里查看**关于手机**，手机版本号变成**00WW_3_39B**，从**系统更新**里可以看到安全补丁程序级别是2018年11月1日。

更新完2018.11月份安全补丁后，发现可以用中国电信的VoLTE了。

### 参考文档

1. [Nokia 7 的原味 Android 使用体验](https://steemit.com/cn/@momok/nokia-7-android)
2. [hmd公布Nokia 7 plus Android P DP5 (nokia称DP4)](https://www.dospy.wang/archiver/?tid-477.html)

