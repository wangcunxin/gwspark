# -*- coding:utf8 -*-
import psycopg2
from userprofile.properties import Properties

__author__ = 'wangcx'


class PostgresqlClient:

    def __init__(self,dbname):
        # load config
        conf_file = "../../../userprofile/config-postgresql.properties"
        prop = Properties()
        conf = prop.getProperties(conf_file)

        host = conf.get("wala.host")
        port = conf.get("wala.port")
        username = conf.get("wala.username")
        password = conf.get("wala.password")

        self.conn = psycopg2.connect(database=dbname, user=username, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def query(self,sql):
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        return list(rows)