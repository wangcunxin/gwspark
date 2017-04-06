# -*- coding:utf8 -*-
import os
import time

from beehive.beehivelogger import *
from beehive.transfer.utils.sqoop_utils import HiveUtil
from config.properties import Properties

__author__ = 'kevin'


def insert_values(tb, columns):
    hive_cmd = HiveUtil.templet_insert_sql(tb, columns)
    print hive_cmd
    exit_val = os.system(hive_cmd)
    if exit_val != 0:
        log.error("fail to insert values:%s" % tb)


def execute_sqoop(sqoop_cmd, db_name, tb_name, hive_tb_name, columns):
    print sqoop_cmd
    exit_status = os.system(sqoop_cmd)
    if exit_status != 0:
        log.error("fail to import:%s.%s" % (db_name, tb_name))
        # os._exit(exit_status)
    else:
        insert_values(hive_tb_name, columns)


def main():
    # load config
    current_path = os.path.abspath('.')
    conf_file = "%s/../../config/oracle.properties" % current_path
    prop = Properties()
    conf = prop.getProperties(conf_file)
    sep = "/001"

    # 1.webdata
    db_name = "webdata"
    sid = conf.get("%s.sid" % db_name)
    host = conf.get("%s.host" % db_name)
    port = conf.get("%s.port" % db_name)
    username = conf.get("%s.username" % db_name)
    password = conf.get("%s.password" % db_name)
    # 1.1 import member
    tb_name = "member"
    hive_tb_name = "o_%s" % tb_name
    columns = "RECORDID,EMAIL,PASSWORD,NICKNAME,MOBILE,REJECTED,BINDSTATUS,PRIKEY,NEEDVALID,HEADPIC,ADDTIME,IP"

    cmd = HiveUtil.templet_sqoop_sql_oracle()
    sqoop_cmd = cmd % ({'sid': sid, 'host': host, 'port': port, 'username': username, 'password': password,
                        'db_name': db_name, 'tb_name': tb_name, 'sep': sep, 'columns': columns,
                        'hive_tb_name': hive_tb_name})
    execute_sqoop(sqoop_cmd, db_name, tb_name, hive_tb_name, columns)

    # 1.2 import memberinfo
    tb_name = "memberinfo"
    hive_tb_name = "o_%s" % tb_name
    columns = "RECORDID,MEMBER_VERSION,POINTVALUE,NEWTASK,EXPVALUE,REALNAME,NICKNAME,HEADPIC,UPDATETIME,SEX," \
              "FROMCITY,RIGHTS,OTHERINFO,ADDTIME,SOURCE,REGFROM,INVITETYPE,INVITEID,IP,NEEDVALID"

    sqoop_cmd = cmd % ({'sid': sid, 'host': host, 'port': port, 'username': username, 'password': password,
                        'db_name': db_name, 'tb_name': tb_name, 'sep': sep, 'columns': columns,
                        'hive_tb_name': hive_tb_name})
    execute_sqoop(sqoop_cmd, db_name, tb_name, hive_tb_name, columns)

    # 1.3 import member_label
    tb_name = "member_label"
    hive_tb_name = "o_%s" % tb_name
    columns = "RECORDID,NAME,PINYIN,REMARK,TYPE,STATUS,ADDTIME,UPDATETIME,SORT_NUM"

    sqoop_cmd = cmd % ({'sid': sid, 'host': host, 'port': port, 'username': username, 'password': password,
                        'db_name': db_name, 'tb_name': tb_name, 'sep': sep, 'columns': columns,
                        'hive_tb_name': hive_tb_name})
    execute_sqoop(sqoop_cmd, db_name, tb_name, hive_tb_name, columns)

    # 1.4 import drama
    tb_name = "drama"
    hive_tb_name = "o_%s" % tb_name
    columns = "RECORDID,LANGUAGE,DRAMANAME,ENGLISHNAME,PINYIN,DIRECTOR,PLAYWRIGHT,ACTORS,RELEASEDATE,TYPE,WEBSITE,LENGTH," \
              "ADDDATE,DRAMAALIAS,HOTVALUE,STATE,CLICKEDTIMES,XIANGQU,QUGUO,GENERALMARK,GENERALMARKEDTIMES,UPDATETIME," \
              "LOGO,COLLECTEDTIMES,HIGHLIGHT,BRIEFNAME,SEODESCRIPTION,SEOTITLE,ENDDATE,DRAMACOMPANY,DRAMADATA,DRAMATYPE," \
              "PLAYINFO,BOUGHTCOUNT,ACTORSTEXT,DIRECTORTEXT,TROUPECOMPANY,TROUPECOMPANYTEXT,CITYCODE,ACTORCONTENT,OTHERINFO," \
              "PRETYPE,SALECYCLE,PRICES,PERFORMDESC,PREPAY,PREPAYDESC,CALENDAREXT,WARMPROMPT,FIRSTPIC,SEPARATE,PROMO," \
              "CRMMSG,GYPMSG,PARTNER,PSEQNO"

    sqoop_cmd = cmd % ({'sid': sid, 'host': host, 'port': port, 'username': username, 'password': password,
                        'db_name': db_name, 'tb_name': tb_name, 'sep': sep, 'columns': columns,
                        'hive_tb_name': hive_tb_name})
    execute_sqoop(sqoop_cmd, db_name, tb_name, hive_tb_name, columns)


if __name__ == '__main__':
    begin = time.time()
    class_name = os.path.basename(__file__)
    log = logging.getLogger('beehive.%s' % class_name)
    log.info("begin %s" % class_name)
    try:
        main()
    except Exception, e:
        log.error(e)
    log.info("end %s" % class_name)
    end = time.time()
    log.info('total cost:%s minutes' % (round((end - begin) / 60, 3)))
