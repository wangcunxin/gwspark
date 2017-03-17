# -*- coding:utf-8 -*-
import urllib

__author__ = 'kevin'


def test0():
    str = "hello world"
    print(str[0:2])
    print(str[3:5])

    if ("O" in str):
        print("in")
    elif ("ll" not in str):
        print("not in")
    else:
        print("no")


def encoding():
    u = u'汉'
    print u, repr(u)  # u'\u6c49'
    s = u.encode('UTF-8')
    print s, repr(s)  # '\xe6\xb1\x89'
    u2 = s.decode('UTF-8')
    print u2, repr(u2)  # u'\u6c49'


def decoding():
    '''
    str和unicode都是basestring的子类，basestring有以下两个方法：
    encode()： 将unicode字符串转换为其他编码字符串，参数为转换后编码
    decode()： 将其他编码转换为unicode字符串，参数为转换前编码

    unicode->encode()->str
    str->decode()->unicode
    '''

    u = u"米国"
    s = "中国"
    x1 = u.encode("utf-8")
    x2 = s.decode("utf-8")
    print repr(x1), repr(x2)
    print u + x2, s + x1
    # s是code_A的str
    # s.decode('code_A').encode('code_B')


def url_quote():
    y3 = "http://japan/日本/av"

    y3_1 = urllib.quote(y3, safe='/')
    print repr(y3_1), y3_1

    y3_2 = urllib.unquote(y3_1)
    print repr(y3_2), y3_2


def test1():
    a = "[[1,2], [3,4], [5,6], [7,8], [9,0]]"
    b = eval(a)
    print b
    print b[1]


def test2():
    '''
    str()->print:可读性好
    repr()->内建函数eval()->对象:对Python比较友好
    '''
    s = "内建函数eval"
    s1 = str(s)
    s2 = repr(s)
    print s1, s2, eval(s2)

    pass


def test3():
    import types
    s = ""
    i = 0
    obj = object()
    u = u""
    print isinstance(s, (int, str))
    print isinstance(i, int)
    print isinstance(obj, object)
    print isinstance(u, unicode)
    print isinstance(s, object)

    print type(u), type(s)

    if isinstance(u, types.UnicodeType):
        print "unicode"
    if type(s) == str:
        print "str"


def split_len():
    s = '0,10182083,1.54147109533,0.471977610293,0.724502159724,0.79783597792,1.88915296905,3.1377854748,1.39666051655,-0.136251841423,-0.102877731382,-0.0871245641184,-0.0991232624695,0.077884674608,2.05527435558'
    print len(s.split(","))


def test4():
    s1 = "10,13"
    s2 = "13,15"
    s3 = "15,18"
    s = '18'

    map = {s1: 'A1', s2: 'A2', s3: 'A3'}
    ls = list(map.keys())
    list.sort(ls)
    for key in ls:
        split = key.split(',')
        min = float(split[0])
        max = float(split[1])
        if (float(s) <= max) and (float(s) >= min):
            print map[key]


def test5():
    s = "123#/activity/sns/relation.xhtml"
    regex = r"/"
    import re
    match = re.search(regex, s)
    if match:
        result = match.group(0)
    else:
        result = s
    print result
    pass


if __name__ == '__main__':
    # test0()
    # encoding()
    decoding()
    # url_quote()
    # test1()
    # test2()
    # test5()
    # split_len()

    pass
