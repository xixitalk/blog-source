---
title: "用ss-redir搭建透明代理"
date: 2018-08-31T06:11:31+08:00
draft: false
tags: [tech,shadowsocks,redsocks]
---

原生android刷机后第一次开机系统初始设置要连接Google服务器，如果没有透明代理就很麻烦，进不了桌面。这里可以通过一台Linux机器（我用的是第一代树莓派）来达到透明代理的作用。手机、平板和机顶盒也可以通过透明代理上网，简化配置。

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

### 启用内核转发

使用iptables转发需要打开内核IPv4转发功能，编辑/etc/sysctl.conf，设置net.ipv4.ip_forward=1，让更新实时生效: 

```
sudo sysctl -p /etc/sysctl.conf
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
# 如果使用redsocks就没有ss代理服务器的ip，直接注释掉

iptables -t nat -A SHADOWSOCKSR -d 0.0.0.0/8 -j RETURN
iptables -t nat -A SHADOWSOCKSR -d 10.0.0.0/8 -j RETURN
iptables -t nat -A SHADOWSOCKSR -d 127.0.0.0/8 -j RETURN
iptables -t nat -A SHADOWSOCKSR -d 169.254.0.0/16 -j RETURN
iptables -t nat -A SHADOWSOCKSR -d 172.16.0.0/12 -j RETURN
iptables -t nat -A SHADOWSOCKSR -d 192.168.0.0/16 -j RETURN
iptables -t nat -A SHADOWSOCKSR -d 224.0.0.0/4 -j RETURN
iptables -t nat -A SHADOWSOCKSR -d 240.0.0.0/4 -j RETURN
# 过滤局域网IP

# 需要过滤的国内IP段加在这个位置，有几千条，参考下面命令获取的cn_rules.conf
# cn_rules.conf里是iptables命令，如果不想几千条拷贝过来可以用bash执行，如下
# sudo bash cn_rules.conf

iptables -t nat -A SHADOWSOCKSR -p tcp -j REDIRECT --to-ports 1088
# 1088 是 ss-redir 的监听端口,ss-local 和 ss-redir 的监听端口不同,配置文件不同

iptables -t nat -I PREROUTING -p tcp -j SHADOWSOCKSR
# 在 PREROUTING 链前插入 SHADOWSOCKSR 链,使其生效
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

### 过滤国内IP

有人提供了apnic的中国IP范围，目前有8000多条，不知道是不是树莓派性能太差了全部导入系统要好久。

```
curl http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest | grep 'apnic|CN|ipv4' | awk -F\| '{ printf("iptables -t nat -A SHADOWSOCKSR -d %s/%d -j RETURN\n", $4, 32-log($5)/log(2)) }' > cn_rules.conf
```

我使用的ip.cn上提供的[中国大陆 IP 列表（基于全球路由优化版）](https://ip.cn/chnroutes.html)，导出来2900多条，常用的大部分大陆IP都覆盖了。获取命令：

```
curl https://raw.githubusercontent.com/ym/chnroutes2/master/chnroutes.txt | grep -v "^#" | awk  '{ printf("iptables -t nat -A SHADOWSOCKSR -d %s -j RETURN\n", $1) }'  > cn_rules.conf
```

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

* 不支持UDP流量转发
* iptables规则可以sh脚本运行，或者iptables-save后用iptables-restore来加载

### 参考资料

1. [ss-redir 透明代理](https://gist.github.com/wen-long/8644243)
1. [linux 用 shadowsocks + iptables + ss-redir 实现全局代理](https://blog.csdn.net/chouzhou9701/article/details/78816029)
1. [有没有比较全的国内 IP 段表？](https://www.v2ex.com/t/351714)
1. [Ubuntu编译运行Redsocks2实现透明代理](https://blog.csdn.net/lvshaorong/article/details/52933544)

