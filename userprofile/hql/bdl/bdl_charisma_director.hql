#-*-coding: UTF-8 -*-

#**********************程序说明*********************************#
#*模块: BDL
#*功能: 导演基础表
#*作者：jys
#*时间：2014-12-22
#*备注：
#***************************************************************#

#导入相关模块
#***********************模块说明********************************#
#conn_db模块,封装了mysql、hive数据库接口
#***************************************************************#

drop table if exists bdl_charisma_director;
create table if not exists bdl_charisma_director (
name string  comment '名称'
)
comment '导演号召力基础表'
row format delimited fields terminated by '|'
stored as  textfile;

alter table bdl_charisma_director SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  bdl_charisma_director 
select 
trim(name) name
from odl_charisma_director;


