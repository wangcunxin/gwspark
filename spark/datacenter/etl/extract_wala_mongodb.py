# -*- coding:utf8 -*-

import psycopg2
from hbase.ttypes import Mutation, BatchMutation
from spark.datacenter.etl.hbase_client import HbaseClient, HbaseUtil
from spark.datacenter.etl.mongodb_client import MongodbClient

__author__ = 'wangcx'

if __name__ == '__main__':
    '''
    oracle:member,point,memberinfo,Charge,payment
    postgresql:comment
    mongo:user_attention,user_be_attention
    '''
    # pip install cx_Oracle,PsyCopg,pymongo,hbase-thrift
    try:
        mongodbClient = MongodbClient()
        colName = "user_attention"
        rs = mongodbClient.findAll(colName)
        tups = []
        for r in rs:
            total= str(r["total"])
            userid= str(r["_id"])
            attentions= r["attentions"]
            tup = [userid,total]
            tups.append(tup)
        qualifiers = ["userid","total"]

        cf = "DF"
        batchMutations = HbaseUtil.getBatchMutations(cf,qualifiers,tups)
        print len(batchMutations)
        #save
        hbase_client = HbaseClient()
        tableName = "up_dat2"
        hbase_client.insertMany(tableName,batchMutations)

    except Exception, e:
        print e

