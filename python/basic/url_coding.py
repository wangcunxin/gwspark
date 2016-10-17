# -*- coding:utf-8 -*-

import urllib2

__author__ = 'kevin'


def urllib2():
    req = urllib2.Request('http://www.pythontab.com')
    response = urllib2.urlopen(req)
    html = response.read()
    print html

if __name__ == '__main__':

    urllib2()

    pass