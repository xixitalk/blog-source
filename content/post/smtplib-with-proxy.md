---
title: "python里用smtplib发邮件使用代理"
date: 2014-04-04T09:51:49+08:00
draft: false
tags: [tech]
---
关键词：smtplib mail proxy

树莓派上一个cron python程序直接用smtplib发送gmail邮件昨天出现问题了，错误是：socket.error: [Errno 97] Address family not supported by protocol，之前都是好好的，我用的smtp.gmail.com，端口是587。

我搜索了一圈，觉得原因是国家防火墙搞得鬼，如果smtplib添加代理就可以避免这种情况。搜索了很多方法都觉得不好使，突然想到以前为google app engine的appcfg.py使用SocksiPy添加代理的方法，并且SocksiPy现在被包含在httplib2的库里了，这样就更方便了。

<!--more-->

在使用smtplib操作文件前部添加：

~~~
from httplib2 import socks
import socket
socket.socket = socks.socksocket
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,"192.168.1.106",1081)
~~~

经测试邮件发送正常，待后续观察。

socks支持SOCKS4、SOCKS5和HTTP代理，上述代码自行替换之。
