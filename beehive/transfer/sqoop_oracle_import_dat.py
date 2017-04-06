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

    # 2.webdata
    db_name = "webdata"
    sid = conf.get("%s.sid" % db_name)
    host = conf.get("%s.host" % db_name)
    port = conf.get("%s.port" % db_name)
    username = conf.get("%s.username" % db_name)
    password = conf.get("%s.password" % db_name)

    # 2.1 import point
    tb_name = "point"
    hive_tb_name = "o_%s" % tb_name
    columns = "RECORDID,TO_MEMBERID,TAG,TAGID,POINTVALUE,REASON,ADMINID,ADDTIME,STAT_FLAG"

    cmd = HiveUtil.templet_sqoop_sql_oracle_partition()
    sqoop_cmd = cmd % ({'sid': sid, 'host': host, 'port': port, 'username': username, 'password': password,
                        'db_name': db_name, 'tb_name': tb_name, 'sep': sep, 'columns': columns,
                        'dat': dat, 'hive_tb_name': hive_tb_name})
    execute_sqoop(sqoop_cmd, db_name, tb_name, hive_tb_name, dat, columns)

    # 2.2 import payment
    tb_name = "payment"
    hive_tb_name = "o_%s" % tb_name
    columns = "RECORDID,TRADE_NO,TOTAL_FEE,ADDTIME,MEMBERID,UPDATETIME,STATUS,PAYSEQNO,PAYMETHOD,PAYBANK," \
              "MEMBERNAME,CHARGETYPE,OUTORDERID,CHARGE_VERSION,VALIDTIME,CHARGETO,GATEWAY_CODE,MERCHANT_CODE,FROM_MEMBERID"

    cmd = HiveUtil.templet_sqoop_sql_oracle_partition()
    sqoop_cmd = cmd % ({'sid': sid, 'host': host, 'port': port, 'username': username, 'password': password,
                        'db_name': db_name, 'tb_name': tb_name, 'sep': sep, 'columns': columns,
                        'dat': dat, 'hive_tb_name': hive_tb_name})
    execute_sqoop(sqoop_cmd, db_name, tb_name, hive_tb_name, dat, columns)

    # 2.3 import treasure
    tb_name = "treasure"
    hive_tb_name = "o_drama_%s" % tb_name
    columns = "RECORDID,MEMBER_ID,TAG,RELATEDID,ADDTIME,ACTION"

    cmd = HiveUtil.templet_sqoop_sql_oracle_partition()
    sqoop_cmd = cmd % ({'sid': sid, 'host': host, 'port': port, 'username': username, 'password': password,
                        'db_name': db_name, 'tb_name': tb_name, 'sep': sep, 'columns': columns,
                        'dat': dat, 'hive_tb_name': hive_tb_name})
    execute_sqoop(sqoop_cmd, db_name, tb_name, hive_tb_name, dat, columns)

    # 2.4 import member_label_ext
    tb_name = "member_label_ext"
    hive_tb_name = "o_%s" % tb_name
    columns = "RECORDID,MEMBERID,LABELID,ADDTIME"

    cmd = HiveUtil.templet_sqoop_sql_oracle_partition()
    sqoop_cmd = cmd % ({'sid': sid, 'host': host, 'port': port, 'username': username, 'password': password,
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
