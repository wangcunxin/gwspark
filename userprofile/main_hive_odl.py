# -*- coding:utf8 -*-
import os

__author__ = 'wangcx'

if __name__ == '__main__':
    '''
    after regist udf,loop:hive -f hql
    '''
    base_path = os.path.abspath('.') + "/hql"
    print base_path
    odl_hql = base_path + "/odl/"
    hqls = []
    for root, dirs, files in os.walk(odl_hql):
        for file in files:
            file_path = os.path.join(root, file)
            hqls.append(file_path)

    for hql in hqls:
        cmd = "hive -f %s" % hql
        print cmd
        # exitVal = os.system(cmd)
        # if (exitVal!=0):
        #     print cmd
