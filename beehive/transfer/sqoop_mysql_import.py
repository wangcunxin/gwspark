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
    else:
        insert_values(hive_tb_name, columns)


def main():
    # load config
    current_path = os.path.abspath('.')
    # modify
    conf_file = "%s/../../config/mysql.properties" % current_path
    prop = Properties()
    conf = prop.getProperties(conf_file)
    sep = "/001"

    # modify 1.movie
    db_name = "movie"
    host = conf.get("%s.host" % db_name)
    port = conf.get("%s.port" % db_name)
    username = conf.get("%s.username" % db_name)
    password = conf.get("%s.password" % db_name)
    # modify 1.1 import movie
    tb_name = "movie"
    hive_tb_name = "o_%s" % tb_name
    columns = "recordid,language,moviename,englishname,pinyin,director,playwright,actors,filmfirm,originalcountry," \
              "releasedate,type,honor,website,remark,adddate,moviealias,hotvalue,tag1,state,prevideo,clickedtimes," \
              "xiangqu,quguo,generalmark,generalmarkedtimes,updatetime,logo,collectedtimes,highlight,playdate," \
              "briefname,seodescription,seotitle,imdbid,boughtcount,avgprice,videolen,content,minprice,maxprice," \
              "otherinfo,edition,color_eggs,hlogo,offlinedate,filmtype,importmodel,period,characteristic,agelayer," \
              "filmmark,countryrelease,samemovie"
    # modify
    cmd = HiveUtil.templet_sqoop_sql_mysql()
    sqoop_cmd = cmd % ({'host': host, 'port': port, 'username': username, 'password': password,
                        'db_name': db_name, 'tb_name': tb_name, 'sep': sep, 'columns': columns,
                        'hive_tb_name': hive_tb_name})
    execute_sqoop(sqoop_cmd, db_name, tb_name, hive_tb_name, columns)

    # modify 1.2 import cinema
    tb_name = "cinema"
    hive_tb_name = "o_%s" % tb_name
    columns = "recordid,citycode,name,englishname,pinyin,postalcode,contactphone,opentime,fax,website,email,transport,remark," \
              "indexareacode,adddate,exitnumber,stationid,hotvalue,googlemap,logo,clickedtimes,xiangqu,quguo,generalmark," \
              "generalmarkedtimes,brandname,feature,discount,updatetime,collectedtimes,coupon,pointx,pointy,briefname," \
              "briefaddress,seodescription,seotitle,flag,lineidlist,booking,newaddress,countycode,countyname,indexareaname," \
              "firstpic,otherinfo,stationname,bpointx,bpointy,popcorn,contact_telephone,subway_transport,mobile_phone," \
              "englishaddress,manage_company,show_gawara,pcid"
    sqoop_cmd = cmd % ({'host': host, 'port': port, 'username': username, 'password': password,
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
