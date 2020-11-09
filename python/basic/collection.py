__author__ = 'kevin'


def test1():
    l = [1, 2, 3, 4, 5, 6]
    print(l[2:len(l)])
    print(l[0])
    print(l[1])


def test2():
    l = [1, 2, 3, 4, 5, 6]
    s = ','.join(str(i) for i in l)
    print s

    dic = {1:'a',2:'b'}
    for k in dic.keys():
        print k


def test3():
    val=2
    nums = [0,1,2,2,3,0,4,2]
    j=len(nums)
    for i in range(j-1,-1,-1):
        if nums[i]==val:
            nums.remove(val)
    print len(nums)


if __name__ == '__main__':
    # test1()
    test3()

    pass
