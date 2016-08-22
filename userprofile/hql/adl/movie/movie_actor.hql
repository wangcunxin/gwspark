
--2.演员喜好
drop table if exists adl_movie_actor_weight;
create table if not exists adl_movie_actor_weight (
recordid string comment '电影ID'
,actor string comment '演员'
,weight double comment '权重'
)
comment '电影演员序号权重详细表'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_movie_actor_weight SET SERDEPROPERTIES('serialization.null.format' = '');

--create temporary function ExplodeActors as 'com.gewara.bigdata.udf.ExplodeActors';
insert overwrite table  adl_movie_actor_weight
select m.recordid, mytable.col1, mytable.col2
from idl_movie m lateral view ExplodeActors(m.actors) mytable as col1, col2
where not m.type like '%动画%' and m.actors is not null and m.actors <> 'null' ;


--有明星号召力成员的电影ID
drop table if exists adl_movie_actor_charisma;
create table if not exists adl_movie_actor_charisma (
recordid string comment '电影ID'
)
comment '有明星号召力成员的电影ID'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_movie_actor_charisma SET SERDEPROPERTIES('serialization.null.format' = '');

insert into table  adl_movie_actor_charisma
 select im.recordid from adl_movie_actor_weight im
LEFT outer JOIN idl_actor_effect ba
 on im.actor = ba.name
 where im.recordid is not null and ba.name is not null group by im.recordid;

--明星见面会数据
 drop table if exists adl_member_actor_meeting;
create table if not exists adl_member_actor_meeting (
memberid string comment '会员ID'
,movieid string comment '明星见面会对应电影'
)
comment '会员明星见面会数据'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_member_actor_meeting SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  adl_member_actor_meeting
select t2.memberid,t1.movieid
from
(
select mpid , movieid from  open_playitem  where mpid is not null
) t1
left join idl_member_order_detail t2
on t1.mpid=t2.relatedid ;


--会员演员权重总表
 drop table if exists adl_movie_actor_weight_2;
create table if not exists adl_movie_actor_weight_2 (
memberid string comment '会员ID'
,recordid string comment '电影ID'
,actor string comment '演员'
,weight string comment '权重'
)
comment '会员电影演员序号权重详细表'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_movie_actor_weight_2 SET SERDEPROPERTIES('serialization.null.format' = '');

--1 添加订单的演员权重
 insert into table  adl_movie_actor_weight_2
 select
 b.memberid
 ,a.recordid
 ,a.actor
 ,a.weight
 from  idl_member_order_detail b LEFT outer JOIN
   adl_movie_actor_weight a
on  b.movieid = a.recordid
where b.memberid is not null
and a.recordid is not null
and a.actor is not null ;

--2 添加喜欢数据 关联明星号召力库的权重
 insert into table  adl_movie_actor_weight_2
 select
 temp.memberid
 ,a.recordid
 ,a.actor
 ,a.weight
 from
 ( select
 imtb.memberid  memberid
 ,m.recordid recordid
 ,m.actors actors
 from  idl_member_treasure_behavior imtb
 LEFT outer JOIN
 adl_movie_actor_charisma c
 on  imtb.relatedid = c.recordid
 LEFT outer JOIN
 idl_movie m
 on  c.recordid = m.recordid
 where imtb.memberid is not null) temp
 LEFT outer JOIN
   adl_movie_actor_weight a
on  temp.recordid = a.recordid
where temp.memberid is not null and a.recordid is not null and a.actor is not null ;


--3 添加明星见面会权重

insert into table  adl_movie_actor_weight_2
 select
 mm.memberid
 ,a.recordid
 ,a.actor
 ,5.0
 from  adl_member_actor_meeting mm LEFT outer JOIN
   adl_movie_actor_weight a
on  mm.movieid = a.recordid
where mm.memberid is not null
and mm.movieid is not null
 and a.actor is not null ;


--4 添加0点场或第一天  并且存在明星号召力库明星权重
 insert into table  adl_movie_actor_weight_2
 select
 temp.memberid
 ,a.recordid
 ,a.actor
 ,a.weight
 from
(
 select
 b.memberid  memberid
 ,m.recordid recordid
 ,m.actors actors
 from
 (select memberid ,itemid
    from(select
    btt.memberid  memberid
 ,btt.movieid  itemid
,btt.playtime  playtime
,m.premieretime  premieretime
from  idl_member_order_detail btt
 left outer join
    idl_movie m
     on btt.movieid = m.recordid
    ) temp2
       where hour(temp2.playtime)=0 or datediff(temp2.playtime,temp2.premieretime) =0
   ) b
 LEFT outer JOIN
 adl_movie_actor_charisma c
 on  b.itemid = c.recordid
 LEFT outer JOIN
 idl_movie m
 on  c.recordid = m.recordid
 where b.memberid is not null) temp
LEFT outer JOIN
   adl_movie_actor_weight a
on  temp.recordid = a.recordid
where temp.memberid is not null
 and a.recordid is not null
 and a.actor is not null ;

--会员演员权重汇总1
--备注：汇总并过滤明星号召力库
 drop table if exists adl_movie_actor_weight_3;
create table if not exists adl_movie_actor_weight_3 (
memberid string comment '会员ID'
,actor string comment '演员'
,weight double comment '权重'
)
comment '会员演员权重汇总'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_movie_actor_weight_3 SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  adl_movie_actor_weight_3
 select  temp.id,temp.act,temp.cou
  from
 (select memberid id, actor act ,sum(weight)  cou from adl_movie_actor_weight_2
 group by memberid,actor order by cou desc  ) temp  left outer join idl_actor_effect bca
 on temp.act = bca.name where  bca.name is not null ;



--会员演员权重汇总2
--备注：会员获取前3名演员

drop table if exists adl_movie_actor_weight_4;
create table if not exists adl_movie_actor_weight_4 (
memberid string comment '会员ID'
,actor string comment '演员'
,weight double comment '权重'
)
comment '会员演员权重汇总'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_movie_actor_weight_4 SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  adl_movie_actor_weight_4
select memberid,actor,weight
from
(select row_number() over(partition by memberid  order by weight desc) rn,
memberid,actor,weight  from adl_movie_actor_weight_3 ) a
where rn<=3  order by memberid,weight desc ;

--会员演员权重汇总3
--备注：会员获取前3名演员 多行转多列   3256843
drop table if exists adl_movie_actor;
create table if not exists adl_movie_actor (
memberid string comment '会员ID'
,actor1 string comment '一号演员'
,actor2 string comment '二号演员'
,actor3 string comment '三号演员'
)
comment '会员演员权重汇总'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_movie_actor SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  adl_movie_actor
select b.memberid,split(b.actors,',')[0],split(b.actors,',')[1], split(b.actors,',')[2]
from (
 select memberid,max(RowToCol(memberid,actor)) actors
  from (
   select memberid,actor,weight from adl_movie_actor_weight_4 order by memberid,weight desc
  ) a  group by memberid) b ;






