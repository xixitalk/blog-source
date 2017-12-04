---
title: "便于代码阅读清理内核代码"
date: 2017-12-03T14:42:05+08:00
draft: false
tags: [linux,tech]
---

Linux代码庞大，代码阅读时候发现无关代码太多，清理一下无关代码便于阅读（清理的标准是某产品内核编译没有用到的文件）。

原理：版本编译用到的文件会更新文件的atime，atime没有更新的文件就是编译无关文件。

<!--more-->

## 新建一个对atime敏感的分区

通常从性能考虑，文件系统挂载都选择忽略atime更新(noatime)，所以我们需要新建一个对atime敏感的分区，一有读文件，立即更新文件atime，编译过程对于源代码就是读操作，这样源代码atime更新了就说明这个文件参与编译了，没有变化就是没有参与编译。

分区通过创建一个大的EXT4的映像文件进行实现。挂载选项重点是加上`strictatime`选项。下面选项创建了一个4GB的EXT4文件系统映像，其他空间大小调整`count=4`即可。

```
dd if=/dev/zero of=kernel_new.img bs=1G count=4
mkfs.ext4 kernel_new.img
tune2fs -c0 -i0 kernel_new.img
```

备份内核原始代码

```
mv kernel kernel_old
```

EXT4文件映像挂载到原内核目录

```
mkdir -p kernel
mount -o loop,strictatime kernel_new.img ./kernel
```

同步代码

```
rsync -av --delete ./kernel_old/ ./kernel/
```

## 刷新所有(.S .c .h)文件atime

保存为touch.py，在kernel目录执行`python touch.py`

```
import os
import time

def TimeStampToTime(timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

now_time = time.time()
os.system('echo %s > touch.time' % now_time)
now_time_str = TimeStampToTime(now_time)
print "touch time: %s (%f)" % (now_time_str,now_time)

exec_str = 'find . -type f -name "*.c" | xargs  touch -a --date="%s"' % now_time_str
os.system(exec_str)

exec_str = 'find . -type f -name "*.h" | xargs  touch -a --date="%s"' % now_time_str
os.system(exec_str)

exec_str = 'find . -type f -name "*.S" | xargs  touch -a --date="%s"' % now_time_str
os.system(exec_str)

```

## 版本编译

## 标识无关代码

保存为analyse.py,在kernel目录，执行`python analyse.py`

```
import os

os.system('find . -type f -name "*.c" > allfile.txt')
os.system('find . -type f -name "*.h" >> allfile.txt')
os.system('find . -type f -name "*.S" >> allfile.txt')
os.system("touch *.py")

fd = open('touch.time','r')
touch_time = fd.read().strip('\n')
touch_time_int = int(float(touch_time))
#print touch_time_int
fd.close()

fd = open("allfile.txt",'r')

for item in fd.readlines():
  item = item.strip('\n')
  atime_int = int(os.path.getatime(item))
  if atime_int == touch_time_int:
    print 'file %s useless' % item
    if item[-7:] != '.backup':
      os.system('mv -v %s %s.backup' % (item,item))

fd.close()
```

清理后再编译，如果编译成功，用命令删除无关文件。

```
#!/bin/bash

find . -name "*.o" | xargs rm
find . -name "*.ko" | xargs rm
find . -name "*.backup" | xargs rm
find . -name "*.cmd" | xargs rm
find . -name "*.tmp" | xargs rm
find . -name "*.order" | xargs rm
find . -name "*.install" | xargs rm
find . -name "*.a" | xargs rm
find . -name "*.gz" | xargs rm
find . -name "*.so" | xargs rm
find . -name "*.dtb" | xargs rm
#find . -name "*.lds" | xargs rm
find . -name "*.check" | xargs rm
find . -name "built-in.mod.c" | xargs rm
find . -name "modules.order" | xargs rm
find . -name "modules.builtin" | xargs rm
#find . -name "\.?" | xargs rm
rm -fr vmlinux System.map .tmp_versions .tmp_*
rm -v arch/arm/boot/compressed/vmlinux*
rm -v arch/arm/boot/compressed/piggy*
rm -v arch/arm/boot/*Image

```

