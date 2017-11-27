---
title: "数字签名时的私钥加密公钥解密"
date: 2013-06-07T15:33:05+08:00
draft: false
tags: [tech,cryptography]
---
疑问：数字签名时的`私钥加密 公钥解密`怎么理解？

前一段时间设计系统启动,为了保障安全使用数字签名进行版本验证，平常的不对称加解密（公钥加密，私钥解密）很容易理解，而数字签名时的`私钥加密 公钥解密`是怎么回事呢？

<!--more-->

### RSA算法
[RSA算法][rsa_url]的数学原理基于两个大素数（也称质数）相乘很容易，但是对其乘积进行因式分解很难。

下面是wikipedia上的RSA生成公钥私钥的简单描述：

> 假设Alice想要通过一个不可靠的媒体接收Bob的一条私人讯息。她可以用以下的方式来产生一个公钥和一个私钥：
> 随意选择两个大的质数p和q，p不等于q，计算N=pq。
> 根据欧拉函数，求得r= φ(n) = φ(p)φ(q) = (p-1)(q-1)
> 选择一个小于r的整数e，求得e关于模r的模反元素，命名为d。（模反元素存在，当且仅当e与r互质）
> 将p和q的记录销毁。
> (N,e)是公钥，(N,d)是私钥。Alice将她的公钥(N,e)传给Bob，而将她的私钥(N,d)藏起来。

(N,e)和(N,d)是一对密钥对（pair keys），本身没有公钥和私钥的属性。(N,e)进行加密，只有(N,d)才能解密。反之亦然，(N,d)进行加密，只有(N,e)才能解密。并且二者不可互相推导，(N,e)推导不出(N,d），(N,d）推导不出(N,e)。

### 不对称加密消息
假定(N,e)作为公钥，(N,d）作为私钥。Alice将她的公钥(N,e)传给Bob，而将她的私钥(N,d)藏起来。如果Bob要发信息给Alice，则先用Alice的公钥进行加密。Alice收到加密的信息后用自己的私钥进行解密。

### 数字签名
假定(N,e)作为公钥，(N,d）作为私钥。  
数字签名的主要流程：Alice先将信息进行hash，对hash值用私钥(N,d)进行加密作为数字签名和信息一起发送。Bob收到信息和数字签名后，用Alice的公钥(N,e)进行解密，如果得到信息的hash值，就表示信息确实是Alice发出的((N,e)和(N,d)唯一对应)。再和信息计算所得的hash相比，如果一致就表示信息未遭到篡改。

### 为什么用ssh-keygen产生的私钥能导出公钥
使用ssh-keygen命令会产生两个文件：id_rsa和id_rsa.pub。id_rsa是私钥，id_rsa.pub是公钥。id_rsa.pub包含其中一个密钥(key)，而id_rsa除了包含一个密钥(key)之外，还包含RSA的推导过程，如p、q、r等数值，这就是为什么id_rsa文件比id_rsa.pub大的原因。因为id_rsa包含RSA推导过程，所以id_rsa可以推导出id_rsa.pub，而id_rsa.pub不包含RSA推导过程，推导不出id_rsa。

(N,e)和(N,d)不分公钥、私钥，一个作为公钥，另一个就作为私钥。但是ssh-keygen生成的id_rsa.pub只能是公钥，id_rsa只能是私钥，不可反了。

### 参考

1. 有了rsa的私钥，可以推出它的公钥吗 <http://ar.newsmth.net/thread-c32c41baf6289.html>
2. RFC2313 PKCS #1: RSA Encryption Version 1.5 <http://tools.ietf.org/html/rfc2313>
3. 阮一峰：数字签名是什么？<http://www.ruanyifeng.com/blog/2011/08/what_is_a_digital_signature.html>

[rsa_url]:http://zh.wikipedia.org/wiki/RSA%E5%8A%A0%E5%AF%86%E6%BC%94%E7%AE%97%E6%B3%95
