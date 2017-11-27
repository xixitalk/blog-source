---
title: "grep命令手册"
date: 2013-06-18T17:51:43+08:00
draft: false
tags: [linux]
---
详细参看这个博文 <http://blog.51yip.com/linux/1008.html>

GNU Grep 2.14 <http://www.gnu.org/software/grep/manual/grep.html>

我常用grep命令是这样的：

```
grep -r -n -I Search_String  DIR
```

-I 跳过二进制文件  
-r 递归子目录  
-n 显示匹配的行号  
Search_String 寻找匹配的字符串  
DIR 查找的目录范围

<!--more-->

```
grep --help  
匹配模式选择:  
 -E, --extended-regexp     扩展正则表达式egrep  
 -F, --fixed-strings       一个换行符分隔的字符串的集合fgrep  
 -G, --basic-regexp        基本正则  
 -P, --perl-regexp         调用的perl正则  
 -e, --regexp=PATTERN      后面根正则模式，默认无  
 -f, --file=FILE           从文件中获得匹配模式  
 -i, --ignore-case         不区分大小写  
 -w, --word-regexp         匹配整个单词  
 -x, --line-regexp         匹配整行  
 -z, --null-data           a data line ends in 0 byte, not newline  
  
杂项:  
 -s, --no-messages         不显示错误信息  
 -v, --invert-match        显示不匹配的行  
 -V, --version             显示版本号  
 --help                    显示帮助信息  
 --mmap                use memory-mapped input if possible  
  
输入控制:  
 -m, --max-count=NUM       匹配的最大数  
 -b, --byte-offset         打印匹配行前面打印该行所在的块号码。  
 -n, --line-number         显示的加上匹配所在的行号  
 --line-buffered           刷新输出每一行  
 -H, --with-filename       当搜索多个文件时，显示匹配文件名前缀  
 -h, --no-filename         当搜索多个文件时，不显示匹配文件名前缀  
 --label=LABEL            print LABEL as filename for standard input  
 -o, --only-matching       show only the part of a line matching PATTERN  
 -q, --quiet, --silent     不显示任何东西  
 --binary-files=TYPE   assume that binary files are TYPE  
 TYPE is 'binary', 'text', or 'without-match'  
 -a, --text                匹配二进制的东西  
 -I                        不匹配二进制的东西  
 -d, --directories=ACTION  目录操作，读取，递归，跳过  
 ACTION is 'read', 'recurse', or 'skip'  
 -D, --devices=ACTION      设置对设备，FIFO,管道的操作，读取，跳过  
 ACTION is 'read' or 'skip'  
 -R, -r, --recursive       递归调用  
 --include=PATTERN     files that match PATTERN will be examined  
 --exclude=PATTERN     files that match PATTERN will be skipped.  
 --exclude-from=FILE   files that match PATTERN in FILE will be skipped.  
 -L, --files-without-match 匹配多个文件时，显示不匹配的文件名  
 -l, --files-with-matches  匹配多个文件时，显示匹配的文件名  
 -c, --count               显示匹配了多少次  
 -Z, --null                print 0 byte after FILE name  
  
文件控制:  
 -B, --before-context=NUM  打印匹配本身以及前面的几个行由NUM控制  
 -A, --after-context=NUM   打印匹配本身以及随后的几个行由NUM控制  
 -C, --context=NUM         打印匹配本身以及随后，前面的几个行由NUM控制  
 -NUM                      根-C的用法一样的  
 --color[=WHEN],  
 --colour[=WHEN]       use markers to distinguish the matching string  
 WHEN may be `always', `never' or `auto'.  
 -U, --binary              do not strip CR characters at EOL (MSDOS)  
 -u, --unix-byte-offsets   report offsets as if CRs were not there (MSDOS)  
```
