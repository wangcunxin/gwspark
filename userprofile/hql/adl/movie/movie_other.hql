
--4.常规型特效控
drop table if exists adl_movie_genera_edition;
create table if not exists adl_movie_genera_edition (
memberid bigint comment '会员id'
,edition_normal_2d int comment '2D次数'
,edition_normal_3d int comment '3D次数'
,edition_jumu int comment '巨幕次数'
,edition_imax int comment 'imax次数'
,fds string comment '分析日期'
)
comment '常规型特效控'
row format delimited fields terminated by '|'
stored as  textfile;

--select * from  adl_movie_genera_edition where edition_normal_2d ='' or edition_normal_3d ='' or edition_jumu ='' or edition_imax ='';

insert overwrite table  adl_movie_genera_edition
select memberid
,sum(case when edition = '2D' then 1 else 0 end) as edition_normal_2d
,sum(case when edition in ('3D','双机3D') then 1 else 0 end) as edition_normal_3d
,sum(case when edition in ('巨幕2D','巨幕3D') then 1 else 0 end) as edition_jumu
,sum(case when edition in ('IMAX2D','IMAX3D') then 1 else 0 end) as edition_imax
,'2015-02-06'
from idl_member_order_detail
group by memberid;

--5.特殊型特效控
drop table if exists adl_movie_spec_edition;
create table if not exists adl_movie_spec_edition (
memberid bigint comment '会员id'
,edition_4d int comment '4d次数'
,edition_4k int comment '4k次数'
,edition_sound int comment '声效次数'
,fds string comment '分析日期'
)
comment '特殊型特效控'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite table  adl_movie_spec_edition
select memberid
,sum(case when edition ='4D' then 1 else 0 end) as edition_4d
,sum(case when edition ='4K' then 1 else 0 end) as edition_4k
,sum(case when edition ='声效' then 1 else 0 end) as edition_sound
,'2015-02-06'
from idl_member_order_detail
group by memberid;

--6.受众特征

drop table if exists adl_movie_audiencefeature1;
create table if not exists adl_movie_audiencefeature1 (
memberid bigint comment '会员id'
,audience_feature_first string comment '受众特征一'
,audience_feature_first_count int comment '受众特征一的次数'
,fds string comment '分析日期'
)
comment '受众特征一'
row format delimited fields terminated by '|'
stored as  textfile;

--取所有特征
insert overwrite table  adl_movie_audiencefeature1
select memberid,audiencefeature_tmp,cou,'2015-02-11'
from (
select memberid,audiencefeature_tmp,cou,row_number() over (distribute by memberid sort by cou desc) rownum
from
(
select memberid,audiencefeature_tmp,count(1) cou
from
(
select memberid,audiencefeature_tmp from idl_member_order_detail  lateral view explode(split(audiencefeature,'/')) adtable as audiencefeature_tmp
) t group by memberid,audiencefeature_tmp
) tt
) ttt
where rownum=1;

--受众特征二
drop table if exists adl_movie_audiencefeature2;
create table if not exists adl_movie_audiencefeature2 (
memberid bigint comment '会员id'
,audience_feature_second string comment '受众特征二'
,audience_feature_second_count int comment '受众特征二的次数'
,fds string comment '分析日期'
)
comment '受众特征二'
row format delimited fields terminated by '|'
stored as  textfile;

--取所有特征
insert overwrite table  adl_movie_audiencefeature2
select memberid,audiencefeature_tmp,cou,'2015-02-11'
from (
select memberid,audiencefeature_tmp,cou,row_number() over (distribute by memberid sort by cou desc) rownum
from
(
select memberid,audiencefeature_tmp,count(1) cou
from
(
select memberid,audiencefeature_tmp from idl_member_order_detail  lateral view explode(split(audiencefeature,'/')) adtable as audiencefeature_tmp
) t group by memberid,audiencefeature_tmp
) tt
) ttt
where rownum=2;

--7.影片受众性别

drop table if exists adl_movie_audiencesex1;
create table if not exists adl_movie_audiencesex1 (
memberid bigint comment '会员id'
,audience_sex_first string comment '受众性别一'
,audience_sex_first_count int comment '受众性别一的次数'
,fds string comment '分析日期'
)
comment '受众性别一'
row format delimited fields terminated by '|'
stored as  textfile;


insert overwrite table  adl_movie_audiencesex1
select memberid,audiencesex_tmp,cou,'2015-02-11'
from (
select memberid,audiencesex_tmp,cou,row_number() over (distribute by memberid sort by cou desc) rownum
from
(
select memberid,audiencesex_tmp,count(1) cou
from
(
select memberid,audiencesex_tmp from idl_member_order_detail  lateral view explode(split(audiencesex,'/')) adtable as audiencesex_tmp
) t group by memberid,audiencesex_tmp
) tt
) ttt
where rownum=1;

--受众性别二
drop table if exists adl_movie_audiencesex2;
create table if not exists adl_movie_audiencesex2 (
memberid bigint comment '会员id'
,audience_sex_second string comment '受众性别二'
,audience_sex_second_count int comment '受众性别二的次数'
,fds string comment '分析日期'
)
comment '受众性别二'
row format delimited fields terminated by '|'
stored as  textfile;


insert overwrite table  adl_movie_audiencesex2
select memberid,audiencesex_tmp,cou,'2015-02-11'
from (
select memberid,audiencesex_tmp,cou,row_number() over (distribute by memberid sort by cou desc) rownum
from
(
select memberid,audiencesex_tmp,count(1) cou
from
(
select memberid,audiencesex_tmp from idl_member_order_detail  lateral view explode(split(audiencesex,'/')) adtable as audiencesex_tmp
) t group by memberid,audiencesex_tmp
) tt
) ttt
where rownum=2;

--10.受众年龄
drop table if exists adl_movie_audienceage1;
create table if not exists adl_movie_audienceage1 (
memberid bigint comment '会员id'
,audience_age_first string comment '受众年龄一'
,audience_age_first_count int comment '受众年龄一的次数'
,fds string comment '分析日期'
)
comment '受众年龄一'
row format delimited fields terminated by '|'
stored as  textfile;


insert overwrite table  adl_movie_audienceage1
select memberid,audienceage_tmp,cou,'2015-02-11'
from (
select memberid,audienceage_tmp,cou,row_number() over (distribute by memberid sort by cou desc) rownum
from
(
select memberid,audienceage_tmp,count(1) cou
from
(
select memberid,audienceage_tmp from idl_member_order_detail  lateral view explode(split(audienceage,'/')) adtable as audienceage_tmp
) t group by memberid,audienceage_tmp
) tt
) ttt
where rownum=1;

--受众年龄二
drop table if exists adl_movie_audienceage2;
create table if not exists adl_movie_audienceage2 (
memberid bigint comment '会员id'
,audience_age_second string comment '受众年龄二'
,audience_age_second_count int comment '受众年龄二的次数'
,fds string comment '分析日期'
)
comment '受众年龄二'
row format delimited fields terminated by '|'
stored as  textfile;


insert overwrite table  adl_movie_audienceage2
select memberid,audienceage_tmp,cou,'2015-02-11'
from (
select memberid,audienceage_tmp,cou,row_number() over (distribute by memberid sort by cou desc) rownum
from
(
select memberid,audienceage_tmp,count(1) cou
from
(
select memberid,audienceage_tmp from idl_member_order_detail  lateral view explode(split(audienceage,'/')) adtable as audienceage_tmp
) t group by memberid,audienceage_tmp
) tt
) ttt
where rownum=2;
