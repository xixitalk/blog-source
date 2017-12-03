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

```
dd if=/dev/zero of=kernel_new.img bs=4k count=60000
mkfs.ext4 kernel_new.img
tune2fs -c0 -i0 kernel_new.img
mv kernel kernel_old
mount -o loop,strictatime kernel_new.img ./kernel
```

## 同步代码

```
rsync -av --delete ./kernel_old/ ./kernel/
```

## 刷新所有文件atime

```
import os
import time

def TimeStampToTime(timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

now_time = time.time()
os.system('echo %s > touch.time' % now_time)
now_time_str = TimeStampToTime(now_time)

exec_str = 'find . -type f | xargs  touch -a --date="%s"' % now_time_str
#print exec_str
print "touch time: %s (%f)" % (now_time_str,now_time)
print now_time
os.system(exec_str)
```

## 版本编译

## 清理无关代码

```
import os

os.system("find . -type f > allfile.txt")
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

清理后再编译，如果编译成功，用命令删除.backup文件。

```
find . -name "*.backup" | xargs rm -fv
```

