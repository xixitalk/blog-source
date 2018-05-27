---
title: "安装pi-hole"
date: 2018-05-27T17:19:42+08:00
draft: false
tags: [linux,raspbian,]
---

pi-hole是通过DNS来拦截网页广告服务，突出特点是有个**好看的数据管理/数据查询/数据分析界面**。它是个组合套件：包括pi-hole admin网页管理（php网页）、dnsmasq、php5、lighttpd、sqlite、curl等一起搭建一个拦截广告的DNS服务，DNS服务是通过dnsmasq提供的。

<!--more-->

###  安装

用下面命令进行安装，安装流程是组合套件依赖应用的安装，还有就是配置。

```

git clone --depth 1 https://github.com/pi-hole/pi-hole.git Pi-hole
cd "Pi-hole/automated install/"
sudo bash basic-install.sh

```

现在安装过程貌似没有设置密码流程了。用下面命令设置admin密码。

```

sudo pihole -a -p

```

### 启动pihole-FTL

安装后lighttpd和dnsmasq会自动启动，pihole-FTL可能不会自动启动。

```

sudo service pihole-FTL  restart

```

###  调整dnsmasq配置参数

如果系统中之前已经安装过dnsmasq，pi-hole增加的参数可能会冲突，在目录`/etc/dnsmasq.d`检查pi-hole增加的选项。比如我注释掉了server的设定，因为我原来的dnsmasq已经设置了上游dns server（用gdns-go搭建的可翻墙解析dns server）。

下面命令重新启动dnsmasq服务：

```

sudo service  dnsmasq restart

```

### 进入pi-hole管理界面

浏览器里打开`http://IP/admin`，点击左侧login栏目，输入密码，即可进入管理界面。

###  更新广告屏蔽列表

点击`Tools`->`Update Lists`进行列表更新。可以手动添加黑名单和白名单。

###  配置路由器的DNS

配置路由器的DNS server为pi-hole提供的DNS服务。

###  最后

经过几个小时，登录`http://IP/admin`就可以看到一些dns解析数据信息。可能会比较有趣。



![pi-hole image](https://pi-hole.github.io/graphics/Screenshots/dashboard.png)


