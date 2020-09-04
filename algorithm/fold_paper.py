# -*- coding:utf-8 -*-
__author__ = 'kevin'


def inOrder(i, n, down):
    '''
    binary tree
    中序遍历：左-根-右
    '''
    if i > n:
        return
    inOrder(i + 1, n, True)
    # 三目表达式 a if true else b
    direction = 'down' if down else 'up'
    arr.append(direction)
    print direction
    inOrder(i + 1, n, False)


if __name__ == '__main__':
    arr = []
    inOrder(1, 3, True)
    print ','.join(arr)
    '''
    折纸问题：向上对折n次，上折痕为up，下折痕为down，对折n次后得到什么结果，数组记录
    折纸n次产生 2^n -1个折痕，符合如下的一颗满二叉树
    1       down
           /    \
    2    down     up
        / \     /  \
    3 down up  down  up
    '''
    pass
