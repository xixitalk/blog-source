---
title: "TCP/IP之IP包头部"
date: 2016-10-10T17:03:51+08:00
draft: false
tags: [tech,network]
styles: [data-table]
---

TCP/IP之IP包头部

<!--more-->


![iphead](http://www.informit.com/content/images/chap3_0672323516/elementLinks/03table02.gif)


### IP包头


|4位版本|4位首部长度|8位服务类型|16位总长度|
|16位标识|3位标志|13位片偏移|
|8位生存时间（TTL）|8位协议|16位首部校验和|
|32位源IP地址|
|32位目的IP地址|
|可选字段|
|不定长度数据|
{: border="1"}


4位版本：4表示IPv4  
4位首部长度：一般是5，标识首部20bytes  
**注释： `08 00 45 00`是典型的IP包特征**,08 00是以太网帧头中IP包类型标识  
8位服务类型：  
16位总长度：整个IP包长度（如果数据是UDP包，包含了UDP包的长度）  
8位协议：**0x11是UDP，0x06是TCP**  
8位TTL：0x80（128）


### UDP包头


|16位源端口|16位目的端口|
|16位长度|16位校验和|
{: border="1"}


整个UDP包头8个字节。  
16位长度：包括UDP头和数据包（比如上层DNS协议）


READ MORE  
<http://www.informit.com/articles/article.aspx?p=28782&seqNum=3>


