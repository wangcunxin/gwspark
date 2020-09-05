# -*- coding:utf-8 -*-
__author__ = 'kevin'


# 递归法
def fib_recur(n):
    assert n >= 0, "n > 0"
    if n <= 1:
        return n
    return fib_recur(n - 1) + fib_recur(n - 2)


# 递推法
def fib_loop_for(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fib_loop_while(n):
    a, b = 0, 1
    while n > 0:
        a, b = b, a + b
        n -= 1
    return a

if __name__ == '__main__':

    for i in range(1, 10):
        print(fib_recur(i))
        # print(fib_loop_for(i))
        # print(fib_loop_while(i))
        print '*'*10
    '''
    斐波那契数列（Fibonacci sequence）
    又称黄金分割数列、因数学家列昂纳多·斐波那契（Leonardoda Fibonacci）以兔子繁殖为例子而引入，
    故又称为“兔子数列”，指的是这样一个数列：1、1、2、3、5、8、13、21、34、……
    在数学上，斐波纳契数列以如下被以递归的方法定义：F(1)=1，F(2)=1, F(n)=F(n-1)+F(n-2)（n>=2，n∈N*）

    '''
    pass
