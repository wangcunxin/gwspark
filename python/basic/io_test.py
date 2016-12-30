# -*- coding:utf-8 -*-
import json

__author__ = 'kevin'


def test1():
    file_object = open('/home/kevin/temp/20161230.test','rb')
    try:
        # all_the_text = file_object.read()
        # print all_the_text
        while True:
            chunk = file_object.read()
            if not chunk:
                break
            print chunk
            decode_json = json.loads(chunk)
            print decode_json
            print decode_json.get('f1')
    finally:
        file_object.close()


def test2():
    file_object = open('/home/kevin/temp/20161230.test','w')
    try:
        lines = {'f1':{'b': '789', 'c': 456, 'a': 123}, 'f2':{'b': '789', 'c': 456, 'a': 123}}
        encode_json = json.dumps(lines)
        print encode_json
        file_object.write(encode_json)

        for line in lines:
            #file_object.write(line)
            pass
    finally:
        file_object.close()
    pass


if __name__ == '__main__':
    test2()
    test1()
    pass
