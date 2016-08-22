drop table if exists odl_base_sex;
create external table if not exists odl_base_sex (
id string  comment ''
,constellationid string comment ''
,sex string comment '性别'
,userid string comment '用户ID'
,moveid string comment '电影ID'
,praise string comment ''
,opationtime string comment ''
,ip string comment 'ip'
) 
comment '性别基础表'

row format delimited fields terminated by '|'
stored as textfile
location '/user/hdfs/sex'
;

alter table odl_base_sex SET SERDEPROPERTIES('serialization.null.format' = '');

