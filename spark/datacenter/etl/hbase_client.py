# -*- coding:utf8 -*-
from hbase.ttypes import Mutation, BatchMutation
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol, TCompactProtocol
from hbase import Hbase

__author__ = 'wangcx'


class HbaseClient:
    def __init__(self):
        self.transport = TBufferedTransport(TSocket("192.168.2.254", 9090), 10 * 1024 * 1024)
        self.transport.open()
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        # self.protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self.client = Hbase.Client(self.protocol)

    def __del__(self):
        self.transport.close()

    def list_table(self):
        for table in self.client.getTableNames():
            print table

    def get(self, tableName, rowkey):
        rs = self.client.getRow(tableName, rowkey)
        return rs

    def scan(self, tableName, cf):
        rets = []
        try:
            scanner = self.client.scannerOpen(tableName=tableName, startRow="", columns=cf)
            try:
                r = self.client.scannerGet(scanner)
                while r:
                    print r
                    rets.append(str(r[0].row))
                    r = self.client.scannerGet(scanner)
            except Exception, e:
                print e
            finally:
                self.client.scannerClose(scanner)
        except Exception, e2:
            print e2
        return rets

    def insertOne(self, tableName, rk, kvs):
        mutations = []
        for col, val in kvs:
            # mutations = [Mutation(column="cf:a", value="1")]
            mut = Mutation(column=col, value=val)
            mutations.append(mut)
        self.client.mutateRow(tableName, rk, mutations)

    def insertMany(self, tableName, batchMutations):
        self.client.mutateRows(tableName, batchMutations)
