drop table if exists odl_charisma_director;
create external table if not exists odl_charisma_director (
name string  comment '演员名称'
) 
comment '导演数据表'
row format delimited fields terminated by '|'
stored as textfile
location '/user/hdfs/director'
;

alter table odl_charisma_director SET SERDEPROPERTIES('serialization.null.format' = '');

