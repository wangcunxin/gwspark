--观影地点相关标签

--1.最常观影城市

drop table if exists adl_place_watchmovie_city;
create table if not exists adl_place_watchmovie_city (
memberid bigint comment '会员id'
,citycode int  comment '观影次数最近最多城市'
,city_count int  comment '观影最多城市的次数'
,fds string comment '分析日期'
)
comment '最常观影城市'
row format delimited fields terminated by '|'
stored as  textfile;


insert overwrite table  adl_place_watchmovie_city
select memberid,citycode,cou,'2015-02-09'
from
(
select memberid,citycode,cou,playtime,row_number() over (distribute by memberid sort by cou desc,playtime desc) rownum
from
(
select memberid,citycode,count(1) cou,max(to_date(playtime)) playtime
from idl_member_order_detail
group by memberid,citycode
) m
) t where t.rownum =1;


--2.最常观影影院*********************************
--影院权重1
 drop table if exists adl_memberid_cinemaid_weight_1;
create table if not exists adl_memberid_cinemaid_weight_1 (
memberid string comment '会员ID'
,cinemaid string comment '电影院ID'
,num int comment '观影次数'
,ishalfyear int comment '是否有半年内购票'
)
comment '会员电影院重权重详细表'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_memberid_cinemaid_weight_1 SET SERDEPROPERTIES('serialization.null.format' = '');

 insert overwrite table  adl_memberid_cinemaid_weight_1
 select
 memberid
 ,cinemaid
 ,cou
 ,case when half >0 then 1 else 0 end as ishalf
 from
 (select
 memberid
 ,cinemaid
 ,count(1) cou
 ,sum(ishalfyear) half
 from idl_member_order_detail
 group by memberid,cinemaid order by memberid,half desc) t
 ;

--影院权重2
--排序汇总前2名观影影院
  drop table if exists adl_memberid_cinemaid_weight_2;
create table if not exists adl_memberid_cinemaid_weight_2 (
memberid string comment '会员ID'
,cinemaid string comment '电影院ID'
,ishalfyear int comment '是否有半年内购票'
,num int comment '观影次数'
)
comment '会员电影院重权重详细表2'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_memberid_cinemaid_weight_2 SET SERDEPROPERTIES('serialization.null.format' = '');



insert overwrite table  adl_memberid_cinemaid_weight_2
select memberid,cinemaid,ishalfyear,num
from
(select row_number() over(partition by memberid  order by ishalfyear desc,num desc) rn,
memberid,cinemaid,ishalfyear,num  from adl_memberid_cinemaid_weight_1 ) a
where rn<=2  order by memberid,ishalfyear desc,num desc;

--影院权重3
--备注:排序汇总前2名观影影院
drop table if exists adl_place_watchmovie_cinema;
create table if not exists adl_place_watchmovie_cinema (
memberid string comment '会员ID'
,cinemaid1 string comment '最常观影影院1'
,count1 string comment '最常观影影院1次数'
,cinemaid2 string comment '最常观影影院2'
,count2 string comment '最常观影影院2次数'
)
comment '排序汇总前2名观影影院'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_place_watchmovie_cinema SET SERDEPROPERTIES('serialization.null.format' = '');

--行转列
create temporary function RowToCol as 'com.gewara.bigdata.udf.RowToCol';

insert overwrite table  adl_place_watchmovie_cinema
select b.memberid,split(b.nums,',')[0],split(b.nums,',')[1],split(b.nums,',')[2],split(b.nums,',')[3]
from (
 select memberid,max(RowToCol(memberid,cinemaid)) cinemaids,max(RowToCol(memberid,num)) nums
  from (
  select memberid,cinemaid ,ishalfyear,num from adl_memberid_cinemaid_weight_2
   order by memberid desc,ishalfyear desc,num desc
  ) a  group by memberid ) b ;


--3. 注册城市
drop table if exists adl_place_regcity;
create table if not exists adl_place_regcity (
memberid bigint comment '会员id'
,regcity string comment '注册城市'
,fds string comment '分析日期'
)
comment '注册城市'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite table  adl_place_regcity
select memberid ,fromcity ,'2015-02-09' from idl_member_detail;


--4.用户最近观影相关
drop table if exists adl_place_recently;
create table if not exists adl_place_recently (
memberid bigint comment '会员id'
,last_movieid bigint comment '最近观影电影id'
,last_playtime string comment '最近观影时间'
,last_citycode int comment '最近观影城市id'
,last_cinemaid bigint comment '最近观影影院id'
,fds string comment '分析日期'
)
comment '用户最近观影相关'
row format delimited fields terminated by '|'
stored as  textfile;


insert overwrite table  adl_place_recently
select memberid,movieid,playtime,citycode,cinemaid,'2014-09-22'
from
(
select memberid,movieid,playtime,citycode,cinemaid,row_number() over (distribute by memberid sort by playtime desc) rownum
from idl_member_order_detail
) t where t.rownum=1;



