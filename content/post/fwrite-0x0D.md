---
title: "fwrite()多了个了0x0D字符"
date: 2016-08-02T08:18:55+08:00
draft: false
tags: [libc]
---

fwrite()写文件竟然多了个了0x0D字符，buffer里检查了也确实没有0x0D，一搜索竟然是如果fopen不是二进制打开，fwrite()遇到0x0A额外写一个0x0D。0D 0A是windows平台的换行符，很明显这是只有在windows平台才有的奇特现象。

<!--more-->

解决办法是fopen的flag加个`b`。

```
fopen("sample.bin", "w+");
```

修改成：

```
fopen("sample.bin", "wb+");
```

另外想起来几年前我遇到过，也解决过，但是忘记了。这次随手记录下来。

#### 参考文章

<http://blog.csdn.net/njuitjf/article/details/5821716>  
<http://stackoverflow.com/questions/5537066/strange-0x0d-being-added-to-my-binary-file>

