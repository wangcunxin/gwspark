# -*- coding:utf-8 -*-
__author__ = 'kevin'


# 快速排序
def quick_sort(src_arr):
    if len(src_arr) < 2:
        return src_arr
    else:
        pivot = src_arr[0]
        less = [i for i in src_arr[1:] if i <= pivot]
        greater = [i for i in src_arr[1:] if i > pivot]
        return quick_sort(less) + [pivot] + quick_sort(greater)
    '''
    从数列中挑出一个元素，称为“基准”（pivot），
    重新排序数列，所有比基准值小的元素摆放在基准前面，所有比基准值大的元素摆在基准后面（相同的数可以到任何一边）。
    在这个分割结束之后，该基准就处于数列的中间位置。这个称为分割（partition）操作。
    递归地（recursively）把小于基准值元素的子数列和大于基准值元素的子数列排序。
    递归到最底部时，数列的大小是零或一，也就是已经排序好了。这个算法一定会结束，因为在每次的迭代（iteration）中，
    它至少会把一个元素摆到它最后的位置去。
    '''


if __name__ == '__main__':
    src_arr = [3, 2, 1, 4, 5, 7, 6, 10, 9, 8]
    dst_arr = quick_sort(src_arr)
    print dst_arr
    pass
