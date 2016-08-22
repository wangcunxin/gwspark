drop table if exists odl_base_membermark;
create external table if not exists odl_base_membermark (
recordid string  comment '记录ID'
,tag string comment '评分类型'
,relatedid string comment '评分类型对应数据ID'
,markvalue string  comment '评分值'
,addtime string comment '创建时间'
,memberid string comment '会员id'
) 
comment '评分数据表'
partitioned by (ds string comment '数据日期')
row format delimited fields terminated by '|'
stored as textfile
;

alter table odl_base_membermark SET SERDEPROPERTIES('serialization.null.format' = '');

alter table odl_base_membermark add partition (ds='$runday') location '/user/sqoop/membermark/$runday';