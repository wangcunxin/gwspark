# -*- coding:utf8 -*-

from spark.datacenter.etl.hbase_client import HbaseClient, HbaseUtil
from spark.datacenter.etl.postgresql_client import PostgresqlClient

__author__ = 'wangcx'

if __name__ == '__main__':
    '''
    postgresql:comment
    '''
    try:
        dat = "201301"
        postgresqlClient = PostgresqlClient("wala")
        #sql = "SELECT memberid,count(1),sum(flowernum),sum(replycount) FROM comment where addtime between to_date('%s','yyyyMMdd') and to_date('%s','yyyyMMdd') group by memberid;" % ("20130103","20130104")
        sql = "SELECT * FROM comment limit 100"
        print sql
        rows = postgresqlClient.query(sql)
        tups = []
        for row in rows:
            print row
            mutations = []
            userid = dat+"#"+str(row[0])
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
        #hbase_client = HbaseClient()
        tableName = "up_dat"
        # cf = ["DF:ip_cities",]
        # print hbase_client.get(tableName, "17578029")
        # hbase_client.scan(tableName, cf)
        #hbase_client.insertMany(tableName, batchMutations)

    except Exception, e:
        print e
