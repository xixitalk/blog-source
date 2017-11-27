#!/usr/bin/env python
# -*- coding: utf-8 -*-#
#

import os,sys

def convert_date(date_str):
  date_str=date_str.strip('\n')
  if len(date_str[17:]) == 5:
    date2 = date_str[:16]+'T'+date_str[17:]+':00'+'+08:00\n'
  else:
    date2 = date_str[:16]+'T'+date_str[17:]+'+08:00\n'
  #print date2
  return date2

def convert_tags(line):
  line = line.strip('\n')
  tags_str=line[len('categories: '):]
  tags_list = tags_str.split(' ')
  i=0
  tags_str2='['
  for tag in tags_list:
    i=i+1
    if i==1:
      tags_str2+=tag
    else:
      tags_str2+=','+tag
  tags_str2+=']'
  return 'tags: '+tags_str2+'\n'

def is_hugo_post(filename):
  fd = open(filename,'r')
  ret = False
  for line in fd.readlines():
    if line.find('draft: false') != -1:
      ret = True
  fd.close()
  return ret

def convert(src_dir,filename,dest_dir):
  dest_filename=filename[11:-9]+'.md'
  fd = open(src_dir+filename,'r')
  fd2 = open(dest_dir+dest_filename,'wb')
  i=0
  hugo_flag = is_hugo_post(src_dir+filename)
  for line in fd.readlines():
    i = i + 1
    if hugo_flag:
      fd2.write(line)
      continue
    if i > 8:
      fd2.write(line)
      continue
    if line.find('layout') != -1:
      continue
    if line.find('mathjax') != -1:
      continue
    if line.find('comments') != -1:
      continue

    if line.find('date') != -1:
      fd2.write(convert_date(line))
      fd2.write('draft: false\n')
      continue
    if line.find('categories') != -1:
      fd2.write(convert_tags(line))
      continue
    fd2.write(line)
  fd.close()
  fd2.close()

def convert_dir():
  for root, dirs, files in os.walk("./post/"):
    for item in files:
      convert(root,item,'./out/')

def main():
  #convert_dir()
  #return
  if len(sys.argv)<3:
    print 'argv error'
    return -1
  src_dir=sys.argv[1]
  src_filename=sys.argv[2]
  dest_dir=sys.argv[3]
  print src_dir+src_filename,dest_dir
  convert(src_dir,src_filename,dest_dir)

if __name__ == '__main__':
  main()
