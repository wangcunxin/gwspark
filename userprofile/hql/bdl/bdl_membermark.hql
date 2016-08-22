#-*-coding: UTF-8 -*-

#**********************程序说明*********************************#
#*模块: BDL
#*功能: 评分基础表
#*作者：jys
#*时间：2014-12-22
#*备注：
#***************************************************************#

#导入相关模块
#***********************模块说明********************************#
#conn_db模块,封装了mysql、hive数据库接口
#***************************************************************#

drop table if exists bdl_membermark;
create table if not exists bdl_membermark (
recordid string  comment '记录ID'
,tag string comment '评分类型'
,relatedid string comment '评分类型对应数据ID'
,markvalue string  comment '评分值'
,addtime string comment '创建时间'
,memberid string comment '会员id'
,fds       string comment '数据日期'
)
comment '评分基础数据表'
partitioned by (ds  string  comment '数据日期')
row format delimited fields terminated by '|'
stored as  textfile;

alter table bdl_membermark SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  bdl_membermark partition  (ds='$runday')
select 
trim(recordid) recordid
,trim(tag) tag
,trim(relatedid) relatedid
,trim(markvalue) markvalue
,trim(addtime) addtime
,trim(memberid) memberid
,'$runday' fds
from odl_base_membermark where ds='$runday' and tag='movie' ; 