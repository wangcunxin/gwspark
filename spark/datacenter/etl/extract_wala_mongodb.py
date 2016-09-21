# -*- coding:utf8 -*-
import math

from spark.datacenter.etl.hbase_client import HbaseClient, HbaseUtil
from spark.datacenter.etl.mongodb_client import MongodbClient

__author__ = 'wangcx'

if __name__ == '__main__':
    '''
    oracle:member,point,memberinfo,Charge,payment
    postgresql:comment
    mongo:user_attention,user_be_attention
    mysql:gmatrix_uvtime
    '''
    # pip install cx_Oracle,psycopg2,pymongo,hbase-thrift,pymysql
    try:
        dat = "201608"
        mongodbClient = MongodbClient()
        colName = "user_attention"
        rs = mongodbClient.findAll(colName)
        tups = []
        for r in rs:
            total= str(r["total"])
            userid= dat+"#"+str(r["_id"])
            attentions= r["attentions"]
            tup = [userid,total]
            tups.append(tup)
        qualifiers = ["userid","friendnum"]

        cf = "DF"
        batchMutations = HbaseUtil.getBatchMutations(cf,qualifiers,tups)
        print len(batchMutations)

        #save
        hbase_client = HbaseClient()
        tableName = "up_dat"
        hbase_client.insertMany(tableName,batchMutations)

        colName = "user_be_attention"
        rs = mongodbClient.findAll(colName)
        tups = []
        for r in rs:
            total= str(r["total"])
            userid= dat+"#"+str(r["_id"])
            tup = [userid,total]
            tups.append(tup)
        qualifiers = ["userid","fannum"]

        batchMutations = HbaseUtil.getBatchMutations(cf,qualifiers,tups)
        print len(batchMutations)
        hbase_client.insertMany(tableName,batchMutations)

    except Exception, e:
        print e

