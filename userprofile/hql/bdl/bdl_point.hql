#-*-coding: UTF-8 -*-

#**********************程序说明*********************************#
#*模块: BDL
#*功能: 演员基础表
#*作者：jys
#*时间：2014-12-22
#*备注：
#***************************************************************#

#导入相关模块
#***********************模块说明********************************#
#conn_db模块,封装了mysql、hive数据库接口
#***************************************************************#

drop table if exists bdl_point;
create table if not exists bdl_point (
addtime string  comment '创建时间'
,memberid string  comment '会员ID'
,point string  comment '积分'
,tag string  comment '类型'
,rowid string  comment ''
,fds       string comment '数据日期'
)
comment '积分数据表'
partitioned by (ds  string  comment '数据日期')
row format delimited fields terminated by '|'
stored as  textfile;

alter table bdl_point SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  bdl_point partition  (ds='$runday')
select 
trim(addtime) addtime
,trim(memberid) memberid
,trim(point) point
,trim(tag) tag
,trim(rowid) rowid
,'2015-02-09'
from odl_base_point where addtime >='2013-01-01 00:00:00:00' and addtime<'2015-01-31 00:00:00:00' ;
