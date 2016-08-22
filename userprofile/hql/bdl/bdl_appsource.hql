drop table if exists bdl_appsource;
create table if not exists bdl_appsource (
recordid string  comment '记录ID'
,memberid string comment '员工ID'
,orderid string comment ''
,osversion string comment 'app版本'
,ostype string comment 'app类型'
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
,fds       string comment '数据日期'
)
comment 'appsource'
partitioned by (ds  string  comment '数据日期')
row format delimited fields terminated by '|'
stored as  textfile;

alter table bdl_appsource SET SERDEPROPERTIES('serialization.null.format' = '');

### appsource有2部分需分别添加
insert overwrite table  bdl_appsource partition  (ds='$runday')
select 
trim(recordid) recordid
,trim(memberid) memberid
,trim(orderid) orderid
,trim(osversion) osversion
,trim(ostype) ostype
,trim(type) type
,trim(appsource) appsource
,trim(mobiletype) mobiletype
,trim(deviceid) deviceid
,trim(citycode) citycode
,trim(addtime) addtime
,trim(flag) flag
,trim(appversion) appversion
,trim(apptype) apptype
,trim(newdeviceid) newdeviceid
,'$runday' fds
from odl_base_appsource where ds='$runday' ; 


insert overwrite table  bdl_appsource partition  (ds='$begin')
select 
'null'
,trim(memberid) memberid
,'null'
,trim(osversion) osversion
,trim(ostype) ostype
,trim(type) type
,'null'
,trim(mobiletype) mobiletype
,'null'
,trim(citycode) citycode
,trim(addtime) addtime
,'null'
,trim(appversion) appversion
,'null'
,'null'
,'$begin' fds
from odl_appsource where addtime >='$begin 00:00:00' and  addtime <'$end 00:00:00';
