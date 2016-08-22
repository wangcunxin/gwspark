
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

drop table if exists bdl_charisma_actor;
create table if not exists bdl_charisma_actor (
name string  comment '名称'
)
comment '演员号召力'
row format delimited fields terminated by '|'
stored as  textfile;

alter table bdl_charisma_actor SET SERDEPROPERTIES('serialization.null.format' = '');


insert overwrite table  bdl_charisma_actor
select 
trim(name) name
from odl_charisma_actor; 