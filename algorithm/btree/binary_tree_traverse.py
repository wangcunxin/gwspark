# -*- coding:utf-8 -*-
__author__ = 'kevin'


# 实现树结构的类，树的节点有三个私有属性  左指针 右指针 自己的值
class TreeNode():
    def __init__(self, data=None, left=None, right=None):
        self._data = data
        self._left = left
        self._right = right


# 前序遍历  遍历过程 根左右 递归
def pre_order(tree):
    if tree == None:
        return False
    print(tree._data)
    pre_order(tree._left)
    pre_order(tree._right)


# 后序遍历 左右根
def pos_order(tree):
    if tree == None:
        return False
    pos_order(tree._left)
    pos_order(tree._right)
    print(tree._data)


# 中序遍历 左根右
def mid_order(tree):
    if tree == None:
        return False
    mid_order(tree._left)
    print(tree._data)
    mid_order(tree._right)


# 层次遍历 从根节点出发，依次访问左右节点，再从左右孩子出发，依次它们的孩子结点，直到节点访问完毕
def row_order(tree):
    queue = []
    queue.append(tree)
    while True:
        if queue == []:
            break
        print(queue[0]._data)
        first_tree = queue[0]
        if first_tree._left != None:
            queue.append(first_tree._left)
        if first_tree._right != None:
            queue.append(first_tree._right)
        queue.remove(first_tree)


if __name__ == '__main__':
    '''
    二叉树的遍历（traversing binary tree）是指从根结点出发，按照某种次序依次访问二叉树中所有的结点，
    使得每个结点被访问依次且仅被访问一次。
    四种遍历方式分别为：先序遍历、中序遍历、后序遍历、层序遍历。
    '''
    treeNode = TreeNode('A',
                        TreeNode('B', TreeNode('D'), TreeNode('E')),
                        TreeNode('C', TreeNode('F'), TreeNode('G'))
                        )
    print '前序遍历'
    pre_order(treeNode)
    print '中序遍历'
    mid_order(treeNode)
    print '后序遍历'
    pos_order(treeNode)
    print '层次遍历'
    row_order(treeNode)
