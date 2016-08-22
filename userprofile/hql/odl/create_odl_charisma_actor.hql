drop table if exists odl_charisma_actor;
create external table if not exists odl_charisma_actor (
name string  comment '演员名称'
) 
comment '演员数据表'
row format delimited fields terminated by '|'
stored as textfile
location '/user/hdfs/actor'
;

alter table odl_charisma_actor SET SERDEPROPERTIES('serialization.null.format' = '');

