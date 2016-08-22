drop table if exists odl_base_comment;
create external table if not exists odl_base_comment (
recordid string  comment '记录ID'
,memberid string comment '会员id'
,nickname string comment '昵称'
,addtime string  comment '添加时间'
,body_length string comment 'wala长度'
,replycount string comment '回复数量'
,flowernum string comment '点赞数量'
,recommend_top string comment 'wala推荐标示'
) 
comment 'wala数据表'
partitioned by (ds string comment '数据日期')
row format delimited fields terminated by '|'
stored as textfile
;

alter table odl_base_comment SET SERDEPROPERTIES('serialization.null.format' = '');

alter table odl_base_comment add partition (ds='$runday') location '/user/sqoop/comment/$runday';