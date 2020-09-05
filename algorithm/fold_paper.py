# -*- coding:utf-8 -*-
__author__ = 'kevin'


def in_order(i, n, down):
    '''
    二叉树 binary tree
    中序遍历：左-根-右
    '''
    if i > n:
        return
    in_order(i + 1, n, True)
    # 三目表达式 a if true else b
    direction = 'down' if down else 'up'
    arr.append(direction)
    print direction
    in_order(i + 1, n, False)


if __name__ == '__main__':
    arr = []
    in_order(1, 3, True)
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
