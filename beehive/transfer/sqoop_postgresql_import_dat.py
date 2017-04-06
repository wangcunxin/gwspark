# -*- coding:utf8 -*-
import os
import sys
import time

from beehive.beehivelogger import *
from beehive.transfer.utils.sqoop_utils import HiveUtil
from config.properties import Properties

__author__ = 'kevin'


def insert_values(tb, dat, columns):
    hive_cmd = HiveUtil.templet_insert_sql_partition(tb, dat, columns)
    print hive_cmd
    exit_val = os.system(hive_cmd)
    if exit_val != 0:
        log.error("fail to insert values:%s.%s" % (tb, dat))


def execute_sqoop(sqoop_cmd, db_name, tb_name, hive_tb_name, dat, columns):
    print sqoop_cmd
    exit_status = os.system(sqoop_cmd)
    if exit_status != 0:
        log.error("fail to import:%s.%s" % (db_name, tb_name))
    else:
        insert_values(hive_tb_name, dat, columns)


def main(argv):
    # input
    dat = argv[0]
    # load config
    current_path = os.path.abspath('.')
    conf_file = "%s/../../config/oracle.properties" % current_path
    prop = Properties()
    conf = prop.getProperties(conf_file)
    sep = "/001"

    # 2.wala
    db_name = "wala"
    host = conf.get("%s.host" % db_name)
    port = conf.get("%s.port" % db_name)
    username = conf.get("%s.username" % db_name)
    password = conf.get("%s.password" % db_name)

    # 1.1 import treasure
    tb_name = "treasure"
    hive_tb_name = "o_wala_%s" % tb_name
    columns = "recordid,member_id,tag,relatedid,addtime,action,actionlabel,unreadnum"

    cmd = HiveUtil.templet_sqoop_sql_postgresql_partition()
    sqoop_cmd = cmd % ({'host': host, 'port': port, 'username': username, 'password': password,
                        'db_name': db_name, 'tb_name': tb_name, 'sep': sep, 'columns': columns,
                        'dat': dat, 'hive_tb_name': hive_tb_name})
    execute_sqoop(sqoop_cmd, db_name, tb_name, hive_tb_name, dat, columns)

    # 1.2 import activity
    tb_name = "activity"
    hive_tb_name = "o_%s" % tb_name
    columns = "recordid,memberid,title,body,start_date,start_time,end_date,end_time,contactway,tag," \
              "relatedid,categoryid,category,address,activity_type,capacity,clickedtimes,addtime,updatetime,citycode," \
              "countycode,indexareacode,status,summary,membercount,reply_time,reply_count,reply_memberid,hometime,communityid," \
              "flag,logo,priceinfo,searchkey,seotitle,seodescription,repeat,membername,replyname,duetime," \
              "sign,activityurl,mobilemsg,needprepay,qq,joinlimit,fromtime,signid,otherinfo,collectedtimes," \
              "linkman,memberlimit,ip,data_version,lotterytag,hotvalue,containmpi,containgoods,first_logo,client_type," \
              "focusvalue,operated,show_type,getway,fee_type,getcash"

    sqoop_cmd = cmd % ({'host': host, 'port': port, 'username': username, 'password': password,
                        'db_name': db_name, 'tb_name': tb_name, 'sep': sep, 'columns': columns,
                        'dat': dat, 'hive_tb_name': hive_tb_name})
    execute_sqoop(sqoop_cmd, db_name, tb_name, hive_tb_name, dat, columns)

    # 1.3 import comment_ym
    ym = dat[0:6]
    tb_name = "comment_%s" % ym
    hive_tb_name = "o_%s" % "comment"
    columns = "recordid,memberid,tag,relatedid,flowernum,addtime,status,flag,transferid,address," \
              "replycount,transfercount,replytime,sorttime,topic,body,nickname,generalmark,otherinfo,apptype," \
              "picturename,link,pointx,pointy,ip,suspected_ad,body_length,order_time,recommend_top,flowernum_member," \
              "isqa,title,videopath,mtids,moderatorid,basicweight,timeweight,type,htmltext,effect,changeweight,moviechangeweight," \
              "bodyweight,validflowernum,biglabelids,anonymousflowernum,recomment_wala"

    sqoop_cmd = cmd % ({'host': host, 'port': port, 'username': username, 'password': password,
                        'db_name': db_name, 'tb_name': tb_name, 'sep': sep, 'columns': columns,
                        'dat': dat, 'hive_tb_name': hive_tb_name})
    execute_sqoop(sqoop_cmd, db_name, tb_name, hive_tb_name, dat, columns)


if __name__ == '__main__':
    begin = time.time()
    class_name = os.path.basename(__file__)
    log = logging.getLogger('beehive.%s' % class_name)
    if len(sys.argv) != 2:
        log.error("Usage: %s <dat>" % class_name)
        sys.exit(-1)
    log.info("begin %s" % class_name)
    log.info(sys.argv[1:])
    try:
        main(sys.argv[1:])
    except Exception, e:
        log.error(e)
    log.info("end %s" % class_name)
    end = time.time()
    log.info('total cost:%s minutes' % round((end - begin) / 60, 3))
