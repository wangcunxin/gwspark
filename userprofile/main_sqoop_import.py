#-*- coding:utf8 -*-
import os
from userprofile.properties import Properties

__author__ = 'wangcx'

if __name__ == '__main__':
    '''
    sqoop import from postgre sql tables:
    report=6
    usertag=2
    pfyc=1
    '''
    #input
    begin_date='2016-01-01'
    end_date='2016-01-02'
    dat='2016-01-01'

    # load config
    conf_file = "config-postgresql.properties"
    prop = Properties()
    conf = prop.getProperties(conf_file)

    #1.report
    host = conf.get("report.host")
    port = conf.get("report.port")
    username = conf.get("report.username")
    password = conf.get("report.password")
    # import 订单表:ticketorder
    cmd = '''
    sqoop import \
    --driver org.postgresql.Driver \
    --connect "jdbc:postgresql://%(host)s/report" \
    --username %(username)s \
    --password %(password)s \
    --table report.ticketorder \
    --where "ordertype = 'ticket' and  paidtime >= '%(begin_date)s 00:00:00' and paidtime <='%(end_date)s 23:59:59'" \
    --columns "recordid, ordertype, tradeno, citycode, status, createtime, addtime,paidtime, memberid, partnerid, paymethod, paybank, payseqno,totalcost, amount, alipaid, gewapaid, quantity, itemfee, otherfee,discount, disreason, description, membername, regtime, regfrom,spid, acount, bcount, ccount, dcount, aamount, bamount, camount,damount, point, specdis, accountpay, wabipay, relatedid, placeid,itemid, costprice, playtime, beforemin, primetime, opentype,edition, buytype, tag, ptime, synchother, settle, updatetime,addpoint, buytimes, downtime, synchtime, itemcost, startdate,enddate, synstatus, fromcity, firstpay, paytimes, category, pricategory,maingewapay, mobilemd5, ordertypesh, filmfest, expressfee, unitprice,deposit, gewadiscount, membercardvalue, membercardgain, membercarddisrate,areaid, totalcostsh, salecycle, adddateid, paiddateid, merchantcode,gatewaycode, newpaymethod, tmpbuytimes, inneramount, partneridsh" \
    --target-dir /user/sqoop/ticket/%(dat)s  \
    -fields-terminated-by  '|' \
    --append \
    -m 1;
    '''
    sqoop_cmd = cmd % ({'host':host,'username':username,'password':password,'begin_date':begin_date,'end_date':end_date,'dat':dat})
    print sqoop_cmd
    # exit_status = os.system(sqoop_cmd)
    # if (exit_status!=0):
    #     print "error happen"
    #     os._exit(exit_status)

    # import 电影库表:movie
    cmd = '''
    sqoop import \
    --driver org.postgresql.Driver \
    --connect "jdbc:postgresql://%(host)s/report" \
    --username %(username)s \
    --password %(password)s \
    --table report.movie  \
    --columns "recordid,moviename,director,actors,type,premieretime" \
    --target-dir /user/sqoop/movie/ \
    -fields-terminated-by  '|'  \
    --append \
    -m 1;
    '''
    sqoop_cmd = cmd % ({'host':host,'username':username,'password':password})
    print sqoop_cmd
    # exit_status = os.system(sqoop_cmd)

    #import 预售数据:goods
    cmd = '''
    sqoop import \
    --driver org.postgresql.Driver \
    --connect "jdbc:postgresql://%(host)s/report" \
    --username %(username)s \
    --password %(password)s \
    --table report.goods  \
    --where " smalltype='pre' " \
    --columns "recordid, tag, relatedid, goodsname, unitprice, costprice, feetype,category, itemid, addtime, goodstype, servicetype, fromtime, totime, fromvalidtime, tovalidtime, period, spcounterid, smalltype, smallid, pretype, settleid"   \
    --target-dir /user/sqoop/goods/  \
    -fields-terminated-by  '|'   \
    --append  \
    -m 1;
    '''
    sqoop_cmd = cmd % ({'host':host,'username':username,'password':password})
    print sqoop_cmd

    #import 预售订单表:ticketorder
    cmd = '''
    sqoop import \
    --driver org.postgresql.Driver \
    --connect "jdbc:postgresql://%(host)s/report" \
    --username %(username)s \
    --password %(password)s \
    --table report.ticketorder \
    --where "ordertype = 'goods' and  paidtime >= '2013-01-01 00:00:00' " \
    --columns "recordid, ordertype, tradeno, citycode, status, createtime, addtime,paidtime, memberid, partnerid, paymethod, paybank, payseqno,totalcost, amount, alipaid, gewapaid, quantity, itemfee, otherfee,discount, disreason, description, membername, regtime, regfrom,spid, acount, bcount, ccount, dcount, aamount, bamount, camount,damount, point, specdis, accountpay, wabipay, relatedid, placeid,itemid, costprice, playtime, beforemin, primetime, opentype,edition, buytype, tag, ptime, synchother, settle, updatetime,addpoint, buytimes, downtime, synchtime, itemcost, startdate,enddate, synstatus, fromcity, firstpay, paytimes, category, pricategory,maingewapay, mobilemd5, ordertypesh, filmfest, expressfee, unitprice,deposit, gewadiscount, membercardvalue, membercardgain, membercarddisrate,areaid, totalcostsh, salecycle, adddateid, paiddateid, merchantcode,gatewaycode, newpaymethod, tmpbuytimes, inneramount, partneridsh" \
    --target-dir /user/sqoop/goods_ticket/  \
    -fields-terminated-by  '|' \
    --append \
    -m 1;
    '''
    sqoop_cmd = cmd % ({'host':host,'username':username,'password':password})
    print sqoop_cmd

    #import 是否有APP:appsource
    cmd = '''
    sqoop import \
    --driver org.postgresql.Driver \
    --connect "jdbc:postgresql://%(host)s/report" \
    --username %(username)s \
    --password %(password)s \
    --table report.appsource  \
    --where " type='login' and addtime >= '%(begin_date)s 00:00:00' and addtime <= '%(end_date)s 23:59:59' " \
    --columns "recordid, memberid, orderid, osversion, ostype, type, appsource,mobiletype, deviceid, citycode, addtime, flag, appversion, apptype,newdeviceid"   \
    --target-dir /user/sqoop/appsource/%(dat)s  \
    -fields-terminated-by  '|'   \
    --append  \
    -m 1;
    '''
    sqoop_cmd = cmd % ({'host':host,'username':username,'password':password,'begin_date':begin_date,'end_date':end_date,'dat':dat})
    print sqoop_cmd

    #import 用户基本信息:member
    cmd = '''
    sqoop import \
    --driver org.postgresql.Driver \
    --connect "jdbc:postgresql://%(host)s/report" \
    --username %(username)s \
    --password %(password)s \
    --table report.member  \
    --columns "recordid,addtime, fromcity, invitetype, regfrom, source,mobilemd5, mblbindtime, emlbindtime, pointvalue"   \
    --target-dir /user/sqoop/member/ \
    -fields-terminated-by  '|'   \
    --append  \
    -m 1;
    '''
    sqoop_cmd = cmd % ({'host':host,'username':username,'password':password})
    print sqoop_cmd

    #2.usertag
    host = conf.get("usertag.host")
    port = conf.get("usertag.port")
    username = conf.get("usertag.username")
    password = conf.get("usertag.password")
    #import wala数据:comment
    cmd = '''
    sqoop import \
    --driver org.postgresql.Driver \
    --connect "jdbc:postgresql://%(host)s/usertag" \
    --username %(username)s \
    --password %(password)s \
    --table usertag.comment  \
    --where " addtime >= '%(begin_date)s 00:00:00' and addtime <= '%(end_date)s 23:59:59' " \
    --columns "recordid,memberid,nickname,addtime,body_length,replycount,flowernum,recommend_top" \
    --target-dir /user/sqoop/comment/%(dat)s \
    -fields-terminated-by  '|'  \
    --append \
    -m 1;
    '''
    sqoop_cmd = cmd % ({'host':host,'username':username,'password':password,'begin_date':begin_date,'end_date':end_date,'dat':dat})
    print sqoop_cmd

    #import 评分数据:membermark
    cmd = '''
    sqoop import \
    --driver org.postgresql.Driver \
    --connect "jdbc:postgresql://%(host)s/usertag" \
    --username %(username)s \
    --password %(password)s \
    --table usertag.membermark \
    --where " addtime >= '%(begin_date)s 00:00:00' and addtime <= '%(end_date)s 23:59:59' " \
    --columns "recordid,tag,relatedid,markvalue,addtime,memberid" \
    --target-dir /user/sqoop/membermark/%(dat)s \
    -fields-terminated-by  '|' \
    --append \
    -m 1;
    '''
    sqoop_cmd = cmd % ({'host':host,'username':username,'password':password,'begin_date':begin_date,'end_date':end_date,'dat':dat})
    print sqoop_cmd

    #3.pfyc
    host = conf.get("pfyc.host")
    port = conf.get("pfyc.port")
    username = conf.get("pfyc.username")
    password = conf.get("pfyc.password")
    #import 喜欢数据:treasure
    cmd = '''
    sqoop import \
    --driver org.postgresql.Driver \
    --connect "jdbc:postgresql://%(host)s/pfyc" \
    --username %(username)s \
    --password %(password)s \
    --table pfyc.treasure \
    --where " addtime >= '%(begin_date)s 00:00:00' and addtime <= '%(end_date)s 23:59:59' " \
    --columns "recordid,member_id,tag,relatedid,action,addtime" \
    --target-dir /user/sqoop/treasure/%(dat)s \
    -fields-terminated-by  '|'  \
    --append \
    -m 1;
    '''
    sqoop_cmd = cmd % ({'host':host,'username':username,'password':password,'begin_date':begin_date,'end_date':end_date,'dat':dat})
    print sqoop_cmd
