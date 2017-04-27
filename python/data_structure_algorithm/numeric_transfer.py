# -*- coding:utf8 -*-
from python.data_structure_algorithm.stack import Stack

__author__ = 'kevin'


def transfer(n, b):
    stack = Stack(20)
    while n > 0:
        x = n % b
        n = n / b
        stack.push(x)
    while not stack.isempty():
        print stack.pop()


if __name__ == '__main__':
    '''
    将一个非负的十进制整数N转换为另一个等价的基为B的B进制数的问题
    一个简单算法基于下列原理：N=(N/B)*B+N%B；可以利用此公式从低位到高位顺序产生B进制的各个位数，而打印输出。
    一般来说应用从高位到低位进行，恰好和计算过程相反。因此，若将计算过程中得到的B进制数的各位顺序进栈，则按出栈顺序打印输出的即为与输入对应的B进制数。
    '''
    transfer(20,2)
    print '-'*10
    transfer(20,8)
    print '-'*10
    transfer(20,16)
    pass
