# -*- coding:utf8 -*-

from spark.datacenter.etl.hbase_client import HbaseClient, HbaseUtil
from spark.datacenter.etl.mysql_client import MysqlClient

__author__ = 'wangcx'

if __name__ == '__main__':
    '''
    mysql:gmatrix_uvtime
    url，avgtime...不是以用户为key的聚合，不符合要求
    '''
    try:
        dat = "201608"
        mysqlClient = MysqlClient("logcenter")
        sql = "SELECT * FROM gmatrix_uvtime limit 10;"
        rows = mysqlClient.query(sql)
        tups = []
        for row in rows:
            print row

    except Exception, e:
        print e
