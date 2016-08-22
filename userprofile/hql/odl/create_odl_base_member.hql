drop table if exists odl_base_member;
create external table if not exists odl_base_member (
recordid string comment 'ID'
,addtime string comment '创建时间'
,fromcity string comment '注册城市'
,invitetype string comment ''
,regfrom string comment ''
,source string comment ''
,mobilemd5 string comment '手机号MD5'
,mblbindtime string comment '时间戳'
,emlbindtime string comment '时间戳'
,pointvalue string comment '值'
) 
comment '会员基础表'

row format delimited fields terminated by '|'
stored as textfile
location '/user/sqoop/member/'
;

alter table odl_base_member SET SERDEPROPERTIES('serialization.null.format' = '');

