---
title: "uClibc的TZ格式"
date: 2018-11-29T15:05:49+08:00
draft: false
tags: [linux]
---

在使用uClibc的linux环境， 时间换算总是不对，特别是出现夏令时。

<!--more-->

细究发现uClibc支持的TZ标准如下  <http://www.opengroup.org/onlinepubs/007904975/basedefs/xbd_chap08.html>

这个[文档写](http://boost.ez2learn.com/doc/html/date_time/local_time.html)的比较详细，补充整理如下：

POSIX 时区(IEEE Std 1003.1)字符串的格式如下：

```
 "std offset dst [offset],start[/time],end[/time]" (可带或不带空格)
```

'std' 给出时区的缩写；'offset' 为距UTC的偏移。'dst' 给出时区在夏令时的缩写；第二个offset 表示在DST时要改变的小时数（也是相对于UTC格林尼治伦敦时间）。'start' 和'end' 为开始(和结束)DST的日期。

'offset' 的格式如下：

```
 [+|-]hh[:mm[:ss]] {h=0-23, m/s=0-59}
```

注意：'time' 和'offset' 具有相同的格式,都是时分秒。

'start' 和'end' 可以是以下三种格式之一：

```
Mm.w.d {m,month=1-12; w,week=1-5 (5总是表示最后一周); d,day=0-6，0是星期天}  
Jn {n=1-365 Feb29不被计算}  
n {n=0-365 Feb29在闰年时被计算}
```

本初子午线以东是‘-’，以西是‘+’

举例耶路撒冷时间`IST-2IDT-3,M3.4.5/02:00:00,M10.5.0/02:00:00`，表示耶路撒冷位于东2区，夏令时比时区时间早一个小时（-3），夏令时开始时间3月，第四个星期五 2点开始变更时间，夏令时结束时间在10月最后一个星期天 2点变更时间,时间回到正常时区（东二区）。

夏令时后面的`offset`通常忽略，`IST-2IDT-3,M3.4.5/02:00:00,M10.5.0/02:00:00`简写为`IST-2IDT,M3.4.5/02:00:00,M10.5.0/02:00:00`，切换到夏令时默认加一小时，如果不是一小时就需要注明。

###  参考资料

1. https://www.uclibc.org/FAQ.html
2. http://www.opengroup.org/onlinepubs/007904975/basedefs/xbd_chap08.html
3.  https://m.blog.naver.com/devil3366/10040211090
4. http://boost.ez2learn.com/doc/html/date_time/local_time.html
5. https://bering-uclibc.zetam.org/wiki/Bering-uClibc_6.x_-_User_Guide_-_Basic_Configuration_-_Basic_System_Configuration
6. http://leaf.sourceforge.net/doc/buci-tz3.html
7. http://www.timeofdate.com/city/Israel/Jerusalem

