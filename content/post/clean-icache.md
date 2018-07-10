---
title: "动态模块加载清除icache"
date: 2018-07-09T20:07:29+08:00
draft: false
tags: [tech]
---

产品是嵌入式RTOS系统，一个第三方软件自己实现了程序动态加载，问题是：程序加载后跳转执行，有时候正常，有时候导致系统死机，死机原因是未定义指令异常（ARM UND）。

<!--more-->

从死机导出来的现场看，该地址是个跳转指令，并没有发现有什么异常，很是奇怪。

**在load模块前，按照模块地址空间清空icache后问题解决**。

理论分析：ARM的icache和dcache是分开的，模块再次加载是内存填充操作，只更新了dcache，icache还是之前执行的指令，这样与内存（DDR）的程序指令不一致了。

linux内核的ko模块加载也有类似操作，见`kernel/module.c`里`flush_module_icache`函数。

```

static void flush_module_icache(const struct module *mod)
{
	mm_segment_t old_fs;

	/* flush the icache in correct context */
	old_fs = get_fs();
	set_fs(KERNEL_DS);

	/*
	 * Flush the instruction cache, since we've played with text.
	 * Do it before processing of module parameters, so the module
	 * can provide parameter accessor functions of its own.
	 */
	if (mod->module_init)
		flush_icache_range((unsigned long)mod->module_init,
				   (unsigned long)mod->module_init
				   + mod->init_size);
	flush_icache_range((unsigned long)mod->module_core,
			   (unsigned long)mod->module_core + mod->core_size);

	set_fs(old_fs);
}

```


