# -*- coding:utf8 -*-

from spark.datacenter.etl.hbase_client import HbaseClient, HbaseUtil
from spark.datacenter.etl.postgresql_client import PostgresqlClient

__author__ = 'wangcx'

if __name__ == '__main__':
    '''
    oracle:member,point,memberinfo,Charge,payment
    postgresql:comment
    mongo:user_attention,user_be_attention
    '''
    # pip install cx_Oracle,PsyCopg,pymongo,hbase-thrift
    try:
        postgresqlClient = PostgresqlClient("wala")
        sql = "SELECT memberid,count(1),sum(flowernum),sum(replycount) FROM comment_201608 group by memberid limit 10;"
        rows = postgresqlClient.query(sql)
        tups = []
        for row in rows:
            mutations = []
            userid = str(row[0])
            commentcount = str(row[1])
            flowernum = str(row[2])
            replycount = str(row[3])

            tup = [userid, commentcount, flowernum, replycount]
            tups.append(tup)

        cf = "DF"
        qualifiers = ["userid", "commentcount", "flowernum", "replycount"]
        batchMutations = HbaseUtil.getBatchMutations(cf, qualifiers, tups)
        print len(batchMutations)
        # save
        hbase_client = HbaseClient()
        tableName = "up_dat2"
        # cf = ["DF:ip_cities",]
        # print hbase_client.get(tableName, "17578029")
        # hbase_client.scan(tableName, cf)
        hbase_client.insertMany(tableName, batchMutations)

    except Exception, e:
        print e
