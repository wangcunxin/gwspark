# -*- coding:utf8 -*-

__author__ = 'kevin'


def recursive(number, days):
    if days == 10:
        return 1
    else:
        return (recursive(number, days + 1) + 1) * 2
    pass


if __name__ == '__main__':
    '''
    猴子吃桃问题
    猴子第一天摘下若干个桃子，当即吃了一半，还不过瘾，又多吃了一个；
    第二天又将剩下的桃子吃掉了一半，又多吃了一个；
    以后每天早晨都吃了前一天剩下的一半加一个，到第十天早上再想吃时，发现只剩下一个桃子。
    求第一天共摘了多少个桃子。
    an=am/2-1->am=(an+1)*2
    a1=(a2+1)*2; a2=(a3+1)*2; a3=(a4+1)*2; ...... a9=(a10+1)*2; a10=1;
    '''
    peachs = recursive(1, 1)
    print peachs
