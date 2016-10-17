# -*- coding:utf-8 -*-
import urllib

__author__ = 'kevin'


def strs():
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
    print repr(u) # u'\u6c49'
    print u
    s = u.encode('UTF-8')
    print repr(s) # '\xe6\xb1\x89'
    print s
    u2 = s.decode('UTF-8')
    print repr(u2) # u'\u6c49'
    print u2

def decoding():
    x1=u"米国"
    x2="中国".decode("utf-8")
    print repr(x1+x2)
    print x1+x2

def url_quote():
    y3="日本"
    y3_1=urllib.quote(y3)
    print repr(y3_1),y3_1
    y3_2=urllib.unquote(y3_1)
    print repr(y3_2),y3_2
    print str(y3_2)

def test1():
    a = "[[1,2], [3,4], [5,6], [7,8], [9,0]]"
    b = eval(a)
    print b
    print b[1]

if __name__ == '__main__':
    #strs()
    encoding()
    decoding()
    url_quote()
    test1()
    pass
