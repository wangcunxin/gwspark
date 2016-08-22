drop table if exists bdl_sex;
create external table if not exists bdl_sex (
id string  comment ''
,constellationid string comment ''
,sex string comment '性别'
,userid string comment '用户ID'
,movieid string comment '电影ID'
,praise string comment ''
,opationtime string comment ''
,ip string comment 'ip'
) 
comment '性别基础表'
row format delimited fields terminated by '|'
stored as textfile
;

alter table bdl_sex SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  bdl_sex 
select 
trim(id) id
,trim(constellationid) constellationid
,trim(sex) sex
,trim(userid) userid
,trim(moveid) movieid
,trim(praise) praise
,trim(opationtime) opationtime
,trim(ip) ip
from odl_base_sex where id is not null 
and constellationid is not null 
and sex is not null 
and userid is not null 
and moveid is not null 
and praise is not null 
and opationtime is not null 
and ip is not null ; 
 
 
  