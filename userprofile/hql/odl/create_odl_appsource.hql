drop table if exists odl_appsource;
create external table if not exists odl_appsource (
addtime string  comment '记录时间'
,appVersion string comment ''
,citycode string comment ''
,memberid string comment ''
,mobileType string comment ''
,osType string comment '类型'
,osVersion string comment ''
,type string comment '类型'
) 
comment 'appsource'
row format delimited fields terminated by '|'
stored as textfile
location '/user/hdfs/appsource/'
;








