#-*- coding:utf8 -*-
import os
from gwup.properties import Properties

__author__ = 'wangcx'

if __name__ == '__main__':
    '''
    sqoop export to postgre sql tables:
    monitor=usertag
    bdc=usertag_warehouse
    market=usertag
    '''
    #input
    begin_date='2016-01-01'
    end_date='2016-01-02'
    dat='2016-01-01'

    # load config
    conf_file = "e:/tmp/pros.properties"
    prop = Properties()
    conf = prop.getProperties(conf_file)

    #1.monitor
    host = conf.get("monitor.host")
    port = conf.get("monitor.port")
    username = conf.get("monitor.username")
    password = conf.get("monitor.password")
    # list tables
    cmd = '''
    sqoop list-tables --driver org.postgresql.Driver  --connect "jdbc:postgresql://%(host)s/monitor" --username %(username)s  --password %(password)s
    '''
    sqoop_cmd = cmd % ({'host':host,'username':username,'password':password,'begin_date':begin_date,'end_date':end_date,'dat':dat})
    print sqoop_cmd

    # export usertag:用户标签数据
    cmd = '''
    sqoop export --connect "jdbc:postgresql://%(host)s/monitor" --username %(username)s  --password %(password)s \
    --table usertag   --fields-terminated-by '|' --export-dir /user/hive/warehouse/adl_usertag/dat=%(dat)s
    '''
    sqoop_cmd = cmd % ({'host':host,'username':username,'password':password,'dat':dat})
    print sqoop_cmd

    #2.bdc
    host = conf.get("bdc.host")
    port = conf.get("bdc.port")
    username = conf.get("bdc.username")
    password = conf.get("bdc.password")
    # export usertag_warehouse:用户标签仓库数据
    cmd = '''
    sqoop export --connect "jdbc:postgresql://%(host)s/bdc" --username %(username)s  --password %(password)s \
    --table usertag_warehouse   --fields-terminated-by '|' --export-dir /user/hive/warehouse/adl_usertag_trade/dat=%(dat)s
    '''
    sqoop_cmd = cmd % ({'host':host,'username':username,'password':password,'dat':dat})
    print sqoop_cmd

    #3.market
    host = conf.get("market.host")
    port = conf.get("market.port")
    username = conf.get("market.username")
    password = conf.get("market.password")
    # export usertag:用户标签数据
    cmd = '''
    sqoop export --connect "jdbc:postgresql://%(host)s/market" --username %(username)s  --password %(password)s \
    --table usertag   --fields-terminated-by '|' --export-dir /user/hive/warehouse/adl_usertag/dat=%(dat)s
    '''
    sqoop_cmd = cmd % ({'host':host,'username':username,'password':password,'dat':dat})
    print sqoop_cmd
