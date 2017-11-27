---
title: "我的AStyle配置选项"
date: 2016-07-11T18:35:57+08:00
draft: false
tags: [tech]
---

我的AStyle代码格式工具的选项：AStyle.exe -A1 -C -S -K -Y -f -s4 -p -U -o -n main.c

在`notepad++`里添加：`运行(R)--运行(R)` 选择AStyle.exe，选项输入`-A1 -C -S -K -Y -f -s4 -p -U -o -n "$(FULL_CURRENT_PATH)"`，然后点击`保存`，这样就保存在运行菜单里了。每次使用从`运行(R)`点击即可。

<!--more-->

简略选项：`-A1 -C -S -K -Y -f -s4 -p -U -o -n`
对应长选项如下：

```
--style=bsd
--indent-classes
--indent-switches
--indent-cases
--indent-col1-comments
--break-blocks
--indent=spaces=4
--pad-oper
--unpad-paren
--keep-one-line-statements
--suffix=none
```

