---
title: "用ss-redir或redsocks搭建透明网关"
date: 2018-08-31T06:11:31+08:00
draft: false
tags: [tech,shadowsocks,redsocks]
---

原生android刷机后第一次开机系统初始设置要连接Google服务器，如果没有透明代理就很麻烦，进不了桌面。这里可以通过一台Linux机器（我用的是第一代树莓派）来达到透明代理的作用。平常情况下手机、平板和机顶盒也可以通过透明代理上网，简化配置。

<!--more-->

### 环境要求

手机和树莓派在同一个局域网，并且可以相互访问，手机WiFi连接，树莓派可以是WiFi也可以是网线连接(没有WiFi的第一代树莓派即可）。有可用的SS/SSR或者socks5代理。

### 用ss-redir搭建带SS代理的端口

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

### 启用内核转发

使用iptables转发需要打开内核IPv4转发功能，编辑/etc/sysctl.conf，设置net.ipv4.ip_forward=1，让更新实时生效: 

```
sudo sysctl -p /etc/sysctl.conf
```

### 设置iptables、ipset转发

设置iptables的目的是将本机特定IP的流量转向ss-redir监听的端口，这个端口是带代理的，这样特定IP的流量就自动代理了。可以配置跳过无需代理的中国IP。iptables执行要root权限，可以切换到root用户，或者用sudo方式运行。

先获取中国IP范围，保存文件是cn.zone。

```
wget -P . http://www.ipdeny.com/ipblocks/data/countries/cn.zone
```

创建china.ipset脚本，内容如下：

```
# Destroy ipset if it already exists
#sudo systemctl stop iptables.service
sudo ipset destroy china

# Create the ipset list
sudo ipset -N china hash:net

# remove any old list that might exist from previous runs of this script
#rm cn.zone

# Pull the latest IP set for China
#wget -P . http://www.ipdeny.com/ipblocks/data/countries/cn.zone

# Add each IP address from the downloaded list into the ipset 'china'
for i in $(cat ./cn.zone ); do ipset -A china $i; done
```

运行脚本创建china的ipset，脚本会把cn.zone文件里的IP段都加到china的ipset里。

```
sudo bash china.ipset
```

创建iptables命令脚本

```
iptables -t nat -N REDSOCKS
# 在 nat 表中创建新链

iptables -t nat -A REDSOCKS -p tcp --dport 28888 -j RETURN
# 28888 是 ss 代理服务器的端口，即远程 shadowsocks 服务器提供服务的端口，如果你有多个 ip 可用,但端口一致，就设置这个

iptables -t nat -A REDSOCKS -d 11.11.11.11 -j RETURN
# 11.11.11.11 是 ss 代理服务器的 ip, 如果你只有一个 ss服务器的 ip，却能选择不同端口,就设置此条

iptables -t nat -A REDSOCKS -d 0.0.0.0/8 -j RETURN
iptables -t nat -A REDSOCKS -d 10.0.0.0/8 -j RETURN
iptables -t nat -A REDSOCKS -d 127.0.0.0/8 -j RETURN
iptables -t nat -A REDSOCKS -d 169.254.0.0/16 -j RETURN
iptables -t nat -A REDSOCKS -d 172.16.0.0/12 -j RETURN
iptables -t nat -A REDSOCKS -d 192.168.0.0/16 -j RETURN
iptables -t nat -A REDSOCKS -d 224.0.0.0/4 -j RETURN
iptables -t nat -A REDSOCKS -d 240.0.0.0/4 -j RETURN
# 过滤局域网IP

iptables -t nat -A REDSOCKS -p tcp -m set --match-set china dst -j RETURN
# 过滤国内IP段,IP保存在china ipset里

iptables -t nat -A REDSOCKS -p tcp -j REDIRECT --to-ports 1088
# 1088 是 ss-redir 的监听端口,ss-local 和 ss-redir 的监听端口不同,配置文件不同

iptables -t nat -I PREROUTING -p tcp -j REDSOCKS
# 在 PREROUTING 链前插入 REDSOCKS 链,使其生效
```

把上面的命令保存成 iprules.sh文件，运行设置到系统里。

```
sudo bash  iprules.sh
```

如果设置错误，清理iptables设置用下面的命令：

```
sudo iptables -t nat -F
```

### 手机端设置

手机端WiFi连接，**选择静态IP，网关填写树莓派的IP**。如果正常，此时手机不用配置代理即可正常访问Google服务器。

### 验证国内IP过滤

访问[ip138](http://www.ip138.com/)和[淘宝IP](http://ip.taobao.com/)，看看IP是不是国内IP，如果是国内IP就说明国内IP过滤成功了，国内IP没有走代理；相反如果是SSR服务器的IP，说明国内IP过滤配置失败了。

### 用redsocks2替代ss-redir

树莓派上本来跑了个SSR，环境太恶劣，经常需要tcping找可用的地址，重启SSR，不想再维护ss-redir的稳定性了，所以切换到redsocks了，redsocks可以直接用SSR提供socks5代理，只维护SSR稳定可用即可。  
没有用原版的[redsocks](https://github.com/darkk/redsocks)，使用了修改版的[redsocks2](https://github.com/semigodking/redsocks)，下载源代码编译略过。

redsocks2的配置config.json如下。如果socks5代理是本机，`ip = 192.168.1.104;`行改成`ip = 0.0.0.0;`。配置文件里`log_debug log_info daemon`调试的时候可以根据需要配置成on或者off，`daemon = on`是后台运行。这里redsocks监听的端口也配置成1088。

```
base {
        log_debug = off;
        log_info = off;

        log = "file:/home/pi/redsocks/log.txt";

        daemon = on;

        redirector = iptables;
}

redsocks {
        local_ip = 0.0.0.0;
        local_port = 1088;

        listenq = 128;

        ip = 192.168.1.104;
        port = 1081;

        type = socks5;

        autoproxy = 0;
        timeout = 10;

}

ipcache {
    cache_size = 4;
    stale_time = 900;
    port_check = 1;
    cache_file = "/tmp/ipcache.txt";
    autosave_interval = 3600;
}
```

运行redsocks2

```
sudo ./redsocks2 -c ./config.json
```

据说redsocks稳定性可能有些问题，配置cron计划任务，每天凌晨3点重启一下好了。

### 其他说明

* 不支持UDP流量转发，DNS污染用其他方法解决。我用的dnsmasq + overture。dnsmasq做缓存，overture做域名翻墙和国内IP分流。
* iptables规则可以sh脚本运行，或者iptables-save后用iptables-restore来加载

### 参考资料

1. [ss-redir 透明代理](https://gist.github.com/wen-long/8644243)
1. [linux 用 shadowsocks + iptables + ss-redir 实现全局代理](https://blog.csdn.net/chouzhou9701/article/details/78816029)
1. [Ubuntu编译运行Redsocks2实现透明代理](https://blog.csdn.net/lvshaorong/article/details/52933544)
1. [使用 iptables、ipset 的全局智能代理](https://blog.chih.me/global-proxy-within-ipset-and-iptables.html)

