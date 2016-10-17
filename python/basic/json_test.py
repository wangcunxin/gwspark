# -*- coding:utf-8 -*-

import json

__author__ = 'kevin'


def test1():
    data1 = [{'b': '789', 'c': 456, 'a': 123}, {'b': '789', 'c': 456, 'a': 123}]

    encode_json = json.dumps(data1)
    print encode_json
    print type(encode_json)

    decode_json = json.loads(encode_json)
    print type(decode_json)
    print decode_json

    for map in decode_json:
        print map.get('a')

if __name__ == '__main__':

    test1()



    pass
