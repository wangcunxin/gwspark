# -*- coding:utf8 -*-
from pymongo import MongoClient
from userprofile.properties import Properties

__author__ = 'wangcx'


class MongodbClient:
    def __init__(self):
        conf_file = "../../../userprofile/config-mongodb.properties"
        prop = Properties()
        conf = prop.getProperties(conf_file)
        host = conf.get("wala.host")
        port = int(conf.get("wala.port"))
        username = conf.get("wala.username")
        password = conf.get("wala.password")
        dbname = conf.get("wala.dbname")

        self.mongoClient = MongoClient(host, port)
        self.mongoDatabase = self.mongoClient.get_database(dbname)
        self.mongoDatabase.authenticate(username, password)

    def __del__(self):
        self.mongoClient.close()

    def getCollection(self, colName):
        return self.mongoDatabase.get_collection(colName)

    def findAll(self, collectionName):
        return list(self.mongoDatabase.get_collection(collectionName).find())
