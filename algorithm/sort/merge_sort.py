# -*- coding:utf-8 -*-
__author__ = 'kevin'


# 归并
def merge(left, right):
    result = []
    while left and right:
        if left[0] < right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    if left:
        result += left
    if right:
        result += right
    return result


# 归并排序
def merge_sort(src_arr):
    if len(src_arr) <= 1:
        return src_arr
    mid = len(src_arr) / 2
    left = src_arr[:mid]
    right = src_arr[mid:]

    left = merge_sort(left)
    right = merge_sort(right)
    return merge(left, right)
    '''
    归并排序
    原理如下（假设序列共有{displaystyle n}个元素）：
    将序列每相邻两个数字进行归并操作，形成{displaystyle ceil(n/2)}个序列，排序后每个序列包含两/一个元素
    若此时序列数不是1个则将上述序列再次归并，形成{displaystyle ceil(n/4)}个序列，每个序列包含四/三个元素
    重复步骤2，直到所有元素排序完毕，即序列数为1
    '''


if __name__ == '__main__':
    src_arr = [3, 2, 1, 4, 5, 7, 6, 10, 9, 8]
    dst_arr = merge_sort(src_arr)
    print dst_arr
    pass
