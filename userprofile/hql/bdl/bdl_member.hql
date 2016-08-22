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
drop table if exists bdl_member;
create  table if not exists bdl_member (
recordid string comment 'ID'
,addtime string comment '创建时间'
,fromcity string comment '注册城市'
,invitetype string comment ''
,regfrom string comment ''
,source string comment ''
,mobilemd5 string comment '手机号MD5'
,mblbindtime string comment '时间戳'
,emlbindtime string comment '时间戳'
,pointvalue string comment '值'
)
comment '会员基础表'
row format delimited fields terminated by '|'
stored as  textfile
;

alter table bdl_member SET SERDEPROPERTIES('serialization.null.format' = '');


insert overwrite table  bdl_member
select 
trim(recordid) recordid
,trim(addtime) addtime
,trim(fromcity) fromcity
,trim(invitetype) invitetype
,trim(regfrom) regfrom
,trim(source) source
,trim(mobilemd5) mobilemd5
,trim(mblbindtime) mblbindtime
,trim(emlbindtime) emlbindtime
,trim(pointvalue) pointvalue
from odl_base_member ; 
