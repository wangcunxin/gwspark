#-*-coding: UTF-8 -*-

#**********************程序说明*********************************#
#*模块: BDL
#*功能: trade基础表
#*作者：yn
#*时间：2014-09-18
#*备注：
#***************************************************************#

#导入相关模块
#***********************模块说明********************************#
#conn_db模块,封装了mysql、hive数据库接口
#***************************************************************#

drop table if exists bdl_movie;
create table if not exists bdl_movie (
recordid string comment '记录名称'
,moviename string comment '电影名称'
,director string comment '导演'
,actors string comment '主演'
,type string comment '电影类型'
,premieretime string comment '放映时间'
,audiencefeature string comment '受众特征'
,audiencesex string comment '受众性别'
,audienceage string comment '受众年龄'
)
comment '电影库表'
row format delimited fields terminated by '|'
stored as  textfile;

alter table bdl_movie SET SERDEPROPERTIES('serialization.null.format' = '');


insert overwrite table  bdl_movie 
select 
trim(recordid) recordid
,trim(moviename) moviename
,regexp_replace(director,"///","/") director
,regexp_replace(actors,"///","/") actors
,regexp_replace(type,"///","/") type
,trim(playdate) premieretime
,trim(usertag) audiencefeature
,trim(female) audiencesex
,trim(age) audienceage
from odl_base_movie  ; 