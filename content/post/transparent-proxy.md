---
title: "用ss-redir搭建透明代理"
date: 2018-08-31T06:11:31+08:00
draft: false
tags: [tech]
---

原生android刷机后第一次开机系统初始设置要连接Google服务器，如果没有透明代理就很麻烦，进不了桌面。这里可以通过一台Linux机器（我用的是第一代树莓派）来达到透明代理的作用。

<!--more-->

### 环境要求

手机和树莓派在同一个局域网，并且可以相互访问，手机WiFi连接，树莓派可以是WiFi也可以是网线连接(没有WiFi的第一代树莓派即可）。

### 用ss-redir搭建带ss代理的端口

如果是SS用shadowsocks-libev里的ss-redir，如果是SSR用shadowsocksr-libev里的ss-redir。注意后者多了一个`r`。我用的是SSR，在树莓派上自己编译的shadowsocksr-libev，下面以SSR为例，SS类似。

配置ss-redir.json，参数和配置SSR一样，注意：`"local_address":"0.0.0.0"`,  这个必须为0.0.0.0。如果同一个机器上也运行SSR，local_port要用不同的端口，如SSR用1081，ss-redir用**1088**，下面配置里会用到1088这个端口。

运行ss-redir，`-v`会显示一些log信息：

```
./ss-redir -v -c ss-redir.json
```

调试完成后，实际运行可以用：

```
nohup ./ss-redir -c ss-redir.json > /dev/null 2>&1 &
```

### 设置iptables转发

设置iptables的目的是将本机所有流量都转向ss-redir监听的端口，这个端口是带代理的，这样所有的流量都自动代理了。iptables执行要root权限，可以切换到root用户，或者用sudo方式运行。

```
iptables -t nat -N SHADOWSOCKSR
# 在 nat 表中创建新链

iptables -t nat -A SHADOWSOCKSR -p tcp --dport 28888 -j RETURN
# 28888 是 ss 代理服务器的端口，即远程 shadowsocks 服务器提供服务的端口，如果你有多个 ip 可用,但端口一致，就设置这个

iptables -t nat -A SHADOWSOCKSR -d 11.11.11.11 -j RETURN
# 11.11.11.11 是 ss 代理服务器的 ip, 如果你只有一个 ss服务器的 ip，却能选择不同端口,就设置此条

iptables -t nat -A SHADOWSOCKSR -d 0.0.0.0/8 -j RETURN
iptables -t nat -A SHADOWSOCKSR -d 10.0.0.0/8 -j RETURN
iptables -t nat -A SHADOWSOCKSR -d 127.0.0.0/8 -j RETURN
iptables -t nat -A SHADOWSOCKSR -d 169.254.0.0/16 -j RETURN
iptables -t nat -A SHADOWSOCKSR -d 172.16.0.0/12 -j RETURN
iptables -t nat -A SHADOWSOCKSR -d 192.168.0.0/16 -j RETURN
iptables -t nat -A SHADOWSOCKSR -d 224.0.0.0/4 -j RETURN
iptables -t nat -A SHADOWSOCKSR -d 240.0.0.0/4 -j RETURN
# 过滤局域网IP

iptables -t nat -A SHADOWSOCKSR -p tcp -j REDIRECT --to-ports 1088
# 1088 是 ss-redir 的监听端口,ss-local 和 ss-redir 的监听端口不同,配置文件不同

iptables -t nat -I PREROUTING -p tcp -j SHADOWSOCKSR
# 在 PREROUTING 链前插入 SHADOWSOCKSR 链,使其生效
```

### 手机端设置

手机端WiFi连接，**选择静态IP，网关填写树莓派的IP**。如果正常，此时手机不用配置代理即可正常访问Google服务器。

### 透明代理进一步配置

* 过滤国内IP，和局域网IP类似，增加iptables规则即可
* 转发UDP流量需要SSR服务端开启，否则UDP可能转发不成功
* iptables规则可以sh脚本运行，或者iptables-save后用iptables-restore来加载
* 其他特殊转发自行看iptables规则

### 参考资料

1. [ss-redir 透明代理](https://gist.github.com/wen-long/8644243)
1. [linux 用 shadowsocks + iptables + ss-redir 实现全局代理](https://blog.csdn.net/chouzhou9701/article/details/78816029)

