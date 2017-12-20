---
title: "linux信号回调栈空间"
date: 2017-12-20T14:13:53+08:00
draft: false
tags: [linux,tech]
---

Linux上通过signal()或者sigaction()可以自定义注册一个信号的信号回调，那么信号回调是执行的栈空间在哪里呢？以下代码以内核3.4.100为例。

<!--more-->

通过`man 7 signal`查看手册，有这么一句话。

> By default, the signal handler is invoked on the normal
       process stack.  It is possible to arrange that the signal handler
       uses an alternate stack; see sigaltstack(2) for a discussion of how
       to do this and when it might be useful.
  
  通过`sigaltstack`可以设置信号handler独立的执行栈，如果没有设置就是在进程栈里。那应用正在执行，进程栈已经压栈了很多层次函数调用，信号handler使用进程栈的哪一部分呢。

信号执行时刻：当进程因为（系统调用、中断和异常）从内核态切换到用户态时检查该进程是否有信号等待处理。

![enter image description here](http://lh6.googleusercontent.com/-_HeCa43rU8o/T69fVlh4E2I/AAAAAAAAAIw/EGiHTpWzNQE/s755/signal_handle.png)

![信号的捕捉](http://img.blog.csdn.net/20130519183522574)

##  独立信号栈

先说独立信号栈，用`sigaltstack`设置独立的栈，在应用上如下设置：

```
    stack_t ss;
      
    ss.ss_sp = malloc(SIGSTKSZ);
    ss.ss_size = SIGSTKSZ;
    ss.ss_flags = 0;
    if (sigaltstack(&ss, NULL) == -1)
    {
        return EXIT_FAILURE;
    }
```

内核在`do_sigaltstack`函数里将地址和大小保存到进程的task struct结构里。

```
		current->sas_ss_sp = (unsigned long) ss_sp;
		current->sas_ss_size = ss_size;
```

信号handler执行的时候内核通过get_sigframe获得信号的栈地址。

```
	/*
	 * This is the X/Open sanctioned signal stack switching.
	 */
	if ((ka->sa.sa_flags & SA_ONSTACK) && !sas_ss_flags(sp))
		sp = current->sas_ss_sp + current->sas_ss_size;
```

第一个判断条件的意思是用户态通过sigstack系统调用设置了独立栈标志;
第二个判断条件是，用户态进程栈，不在独立栈的范围内;

如果满足条件，就把`sigaltstack`设置的空间作为信号handler执行的栈空间。

##  信号共享进程栈

如果用户没有用`sigaltstack`设置单独的栈，那就用进程栈。同样在内核`get_sigframe`获得进程栈地址。默认sp赋予`regs->ARM_sp`，这个是进程栈中已经使用的栈顶(小地址，栈的使用从高地址到低地址减少)。**信号栈在进程栈已经使用的后面(向小地址扩展)开始,使用进程栈空闲区域**。

```
static inline void __user *
get_sigframe(struct k_sigaction *ka, struct pt_regs *regs, int framesize)
{
	unsigned long sp = regs->ARM_sp;
	void __user *frame;

	/*
	 * This is the X/Open sanctioned signal stack switching.
	 */
	if ((ka->sa.sa_flags & SA_ONSTACK) && !sas_ss_flags(sp))
		sp = current->sas_ss_sp + current->sas_ss_size;

	/*
	 * ATPCS B01 mandates 8-byte alignment
	 */
	frame = (void __user *)((sp - framesize) & ~7);

	return frame;
}
```

进程栈和信号栈位置大概如下：

```
|————————————————————| 低地址 栈顶
|                    |
|                    |
|--------------------| 信号栈栈底，向低地址扩展 
|                    |
|--------------------| 应用被调度切换走时栈顶(regs->ARM_sp)
|                    |
|                    |
|                    |
|                    |
|                    |
|                    |
|                    |
|                    |
|————————————————————| 高地址 进程栈底  main
```


#  参考资料

[<深入浅出> linux 信号栈](http://blog.csdn.net/chenyu105/article/details/7093603)

[Linux 信号应用之黑匣子程序设计](http://blog.jobbole.com/101619/)

