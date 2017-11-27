---
title: "从octopress迁移到hugo"
date: 2017-11-27T17:23:59+08:00
draft: false
tags: [tech,hugo,octopress]
---

[octopress](http://octopress.org/)编译速度很慢，2.0版本依赖老的ruby版本，环境搭建复杂，3.0版本几年来还没有正式发布，所以本blog切换到了[Hugo](https://gohugo.io/)，下面是迁移记录。

<!--more-->

## 下载hugo

从<https://github.com/gohugoio/hugo/releases>下载合适的hugo版本，我下载的是ARM版本，在树莓派3上运行。

## hugo新建站

用下面hugo命令，新建站点文件。

```
hugo new site myblog
```

## 选择模板

选择`Hugo-Octopress`模板，用下面命令获取。

```
git submodule add https://github.com/parsiya/Hugo-Octopress.git themes/Hugo-Octopress
```

## 配置站点config.toml

参考<https://github.com/xixitalk/blog-source/blob/master/config.toml>配置。效果参看<https://xixitalk.github.io/>

## 博客转换迁移

主要是文章头的格式转换，可以参考这个python脚本<https://github.com/xixitalk/blog-source/blob/master/convert.py>，把main函数里下面两行放开，把`octopress`的`source/_post`目录博文(.markdown)放在`post`目录，执行`mkdir -p out && python convert.py`命令，会将转换的hugo博文放在`out`目录，将`out`目录的博文拷贝到hugo的`content/post`目录。

```
  #convert_dir()
  #return
```

## 博客预览

用下面的命令进行博客预览，假定IP是192.168.1.104，如果是本机换成localhost。

```
hugo server -D --bind 192.168.1.104 --theme=Hugo-Octopress  --disableFastRender
--buildDrafts --baseURL=http://192.168.1.104:1313
```

## 初始化博客发布目录public

用git初始化public目录，这个目录就是博客的发布目录，是要上传到github的仓库的，仓库名要是：`[yourname].github.io`。

```
git submodule add git@github.com:[yourname]/[yourname].github.io.git public
```

## 博客编译

用下面的命令进行博客编译生成，生成文件在`public`目录。

```
hugo  --theme=Hugo-Octopress
```

## 博客发布

把`public`目录文件发布到github上。

```
cd public
git add -A
git commit -m "deploy to github"
git push origin master
```

除public目录外，其他文件自行找git仓库管理，可以是github page的source分支，也可以是独立git仓库。我用了独立仓库，参见<https://github.com/xixitalk/blog-source>。

