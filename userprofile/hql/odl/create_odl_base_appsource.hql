drop table if exists odl_base_appsource;
create external table if not exists odl_base_appsource (
recordid string  comment '记录ID'
,memberid string comment '员工ID'
,orderid string comment ''
,osversion string comment ''
,ostype string comment ''
,type string comment '类型'
,appsource string comment ''
,mobiletype string comment '手机类型'
,deviceid string comment ''
,citycode string comment '城市编码'
,addtime string comment '创建时间'
,flag string comment ''
,appversion string comment ''
,apptype string comment ''
,newdeviceid string comment ''
) 
comment 'appsource'
partitioned by (ds string comment '数据日期')
row format delimited fields terminated by '|'
stored as textfile
;

alter table odl_base_appsource SET SERDEPROPERTIES('serialization.null.format' = '');

alter table odl_base_appsource add partition (ds='2014-07-01') location '/user/sqoop/appsource/2014-07-01';







