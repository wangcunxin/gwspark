#-*-coding: UTF-8 -*-

#**********************程序说明*********************************#
#*模块: BDL
#*功能: 喜欢数据表
#*作者：jys
#*时间：2014-12-22
#*备注：
#***************************************************************#

#导入相关模块
#***********************模块说明********************************#
#conn_db模块,封装了mysql、hive数据库接口
#***************************************************************#

drop table if exists bdl_treasure;
create table if not exists bdl_treasure (
recordid string  comment '记录ID'
,memberid string comment '会员id'
,tag string comment '类型'
,relatedid string  comment '类型对应数据ID'
,action string comment '方式'
,addtime string comment '创建时间'
,addtimestr string comment '创建时间戳'
,fds       string comment '数据日期'
)
comment '喜欢数据表'
partitioned by (ds  string  comment '数据日期')
row format delimited fields terminated by '|'
stored as  textfile;

alter table bdl_treasure SET SERDEPROPERTIES('serialization.null.format' = '');


insert overwrite table  bdl_treasure partition  (ds='$runday')
select 
trim(recordid) recordid
,trim(memberid) memberid
,trim(tag) tag
,trim(relatedid) relatedid
,trim(action) action
,trim(addtime) addtime
,trim(addtimestr) addtimestr
,'$runday' fds
from odl_base_treasure where ds='$runday' and tag='movie' ; 
