---
title: "用base64进行关键词编码"
date: 2013-07-02T22:01:04+08:00
draft: false
tags: [base64]
---
用base64对关键词进行两次编码，浏览器客户端用javascript进行两次解码。对于支持javascript的浏览器来说透明，目的是防止关键词过滤。

<!--more-->

如(查看网页源代码)

{% base64_block %}
GFW 民主 自由 胡锦涛 江泽民 
{% endbase64_block %}

###base64_block.rb
把<https://gist.github.com/xixitalk/5927023>代码保存为base64_block.rb，放到`octopress\plugins`目录。

###base64.js
把<https://github.com/xixitalk/xixitalk.github.com/blob/source/source/javascripts/base64.js>保存为base64.js，放到`octopress\source\javascripts`目录。

###使用base64_block使用
使用`base64_block`和`endbase64_block`包含需要编码的段落。详细参看`base64_block.rb`文件前部的注释说明。注意：一篇文章里只能有一个`base64_block`块。

{% raw %}

~~~
{% base64_block %}
这些信息会被编码
{% endbase64_block %}
~~~

{% endraw %}
