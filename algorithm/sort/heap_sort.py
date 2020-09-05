# -*- coding:utf-8 -*-
__author__ = 'kevin'


# 堆排序
def heap_sort(nums):
    length = len(nums)

    def shift_down(start, end):
        root = start
        while True:
            child = 2 * root + 1
            if child > end:
                break
            if child + 1 <= end and nums[child] < nums[child + 1]:
                child += 1
            if nums[root] < nums[child]:
                nums[root], nums[child] = nums[child], nums[root]
                root = child
            else:
                break

    # 创建最大堆
    for start in range((length - 2) / 2, -1, -1):
        shift_down(start, length - 1)

    # 堆排序
    for end in range(length - 1, 0, -1):
        nums[0], nums[end] = nums[end], nums[0]
        shift_down(0, end - 1)

    return nums
    '''
    堆排序
    若以升序排序说明，把数组转换成最大堆积(Max-Heap Heap)，
    这是一种满足最大堆积性质(Max-Heap Property)的二叉树：对于除了根之外的每个节点i, A[parent(i)] ≥ A[i]。
    重复从最大堆积取出数值最大的结点(把根结点和最后一个结点交换，把交换后的最后一个结点移出堆)，
    并让残余的堆积维持最大堆积性质。
    '''


if __name__ == '__main__':
    src_arr = [3, 2, 1, 4, 5, 7, 6, 10, 9, 8]
    dst_arr = heap_sort(src_arr)
    print dst_arr
    pass
