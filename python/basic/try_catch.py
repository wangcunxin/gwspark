# -*- coding:utf-8 -*-

__author__ = 'kevin'


def normal_trycatch():
    try:
        fh = open("test.txt", "w")
        try:
            fh.write("there is an exception")
            1 / 0
            raise Exception("an exception")
        finally:
            fh.close()
    except IOError:
        print("fail to open a file")
    except Exception, e:
        print(e)
    else:
        print("no exception")


if __name__ == '__main__':
    normal_trycatch()

    pass
