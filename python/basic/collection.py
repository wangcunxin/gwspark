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


if __name__ == '__main__':
    # test1()
    test2()

    pass
