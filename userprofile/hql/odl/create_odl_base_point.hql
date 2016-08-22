drop table if exists odl_base_point;
create external table if not exists odl_base_point (
addtime string  comment '创建时间'
,memberid string  comment '会员ID'
,point string  comment '积分'
,tag string  comment '类型'
,rowid string  comment ''
) 
comment '积分数据表'
row format delimited fields terminated by '|'
stored as textfile
location '/user/hdfs/point'
;

alter table odl_base_point SET SERDEPROPERTIES('serialization.null.format' = '');

