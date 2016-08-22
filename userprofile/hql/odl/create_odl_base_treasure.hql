drop table if exists odl_base_treasure;
create external table if not exists odl_base_treasure (
recordid string  comment '记录ID'
,memberid string comment '会员id'
,tag string comment '类型'
,relatedid string  comment '类型对应数据ID'
,action string comment '方式'
,addtime string comment '创建时间'
,addtimestr string comment '创建时间戳'
) 
comment '喜欢数据表'
partitioned by (ds string comment '数据日期')
row format delimited fields terminated by '|'
stored as textfile
;

alter table odl_base_treasure SET SERDEPROPERTIES('serialization.null.format' = '');

alter table odl_base_treasure add partition (ds='$runday') location '/user/sqoop/treasure/$runday';