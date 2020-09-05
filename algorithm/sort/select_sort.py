# -*- coding:utf-8 -*-
__author__ = 'kevin'


# 用于查找出数组中最小的元素，返回最小元素的索引。
def find_smallest(arr):
    smallest = arr[0]
    smallest_index = 0
    for i in range(1, len(arr)):
        if smallest > arr[i]:
            smallest = arr[i]
            smallest_index = i
    return smallest_index


# 选择排序
def select_sort(arr):
    dst_arr = []
    while arr:
        smallest = find_smallest(arr)
        dst_arr.append(arr.pop(smallest))
    return dst_arr
    '''
    选择排序（Selection sort）是一种简单直观的排序算法。
    首先在未排序序列中找到最小（大）元素，存放到排序序列的起始位置，然后，再从剩余未排序元素中继续寻找最小（大）元素，
    然后放到已排序序列的末尾。以此类推，直到所有元素均排序完毕。
    '''


if __name__ == '__main__':
    src_arr = [3, 2, 1, 4, 5, 7, 6, 10, 9, 8]
    dst_arr = select_sort(src_arr)
    print dst_arr
    pass
