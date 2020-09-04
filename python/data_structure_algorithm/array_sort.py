# -*- coding:utf8 -*-

__author__ = 'kevin'


def swap(r, i, j):
    # reduce exchange
    if i == j:
        return
    temp = r[i]
    r[i] = r[j]
    r[j] = temp


# quick sort
def qsort(lis, low, high):
    begin = low
    end = high
    if low < high:
        pivot_key = lis[low]
        while low < high:
            while low < high and lis[high] >= pivot_key:
                high -= 1
            while low < high and lis[low] <= pivot_key:
                low += 1
            # exchange找到的比pivot大和小的value
            swap(lis, low, high)
        # exchange pivot
        swap(lis, begin, low)

        qsort(lis, begin, low - 1)
        qsort(lis, low + 1, end)
    return lis


if __name__ == '__main__':
    arr = [10, 3, 11, 9, 17, 8, 20, 1000, 1, 0, -1]
    print qsort(arr, 0, len(arr) - 1)

    pass
