# -*- coding:utf8 -*-

import psycopg2
from hbase.ttypes import Mutation, BatchMutation
from spark.datacenter.etl.hbase_client import HbaseClient, HbaseUtil
from userprofile.properties import Properties

__author__ = 'wangcx'

if __name__ == '__main__':
    '''
    oracle:member,point,memberinfo,Charge,payment
    postgresql:comment
    mongo:user_attention,user_be_attention
    '''
    # pip install cx_Oracle,PsyCopg,pymongo,hbase-thrift
    try:
        # load config
        conf_file = "../../../userprofile/config-postgresql.properties"
        prop = Properties()
        conf = prop.getProperties(conf_file)

        host = conf.get("wala.host")
        port = conf.get("wala.port")
        username = conf.get("wala.username")
        password = conf.get("wala.password")
        # list tables
        conn = psycopg2.connect(database="wala", user=username, password=password, host=host, port=port)
        cur = conn.cursor()
        try:
            cur.execute("SELECT memberid,count(1),sum(flowernum),sum(replycount) FROM comment_201608 group by memberid limit 10;")
            rows = cur.fetchall()
            tups=[]
            for row in rows:
                mutations = []
                userid = str(row[0])
                commentcount = str(row[1])
                flowernum = str(row[2])
                replycount = str(row[3])

                tup = [userid,commentcount,flowernum,replycount]
                tups.append(tup)

            cf = "DF"
            qualifiers=["userid","commentcount","flowernum","replycount"]
            batchMutations = HbaseUtil.getBatchMutations(cf,qualifiers,tups)
            print len(batchMutations)
            #save
            hbase_client = HbaseClient()
            tableName = "up_dat2"
            # cf = ["DF:ip_cities",]
            # print hbase_client.get(tableName, "17578029")
            # hbase_client.scan(tableName, cf)
            hbase_client.insertMany(tableName,batchMutations)
        finally:
            cur.close()
            conn.close()

    except Exception, e:
        print e

