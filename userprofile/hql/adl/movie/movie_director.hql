--1.导演喜好  7441
drop table if exists adl_movie_director_weight;
create table if not exists adl_movie_director_weight (
recordid string comment '电影ID'
,director string comment '导演'
,weight double comment '权重'
)
comment '电影导演序号权重详细表'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_movie_director_weight SET SERDEPROPERTIES('serialization.null.format' = '');

--create temporary function ExplodeDirectors as 'com.gewara.bigdata.udf.ExplodeDirectors';
insert into table  adl_movie_director_weight
 select m.recordid, mytable.col1, mytable.col2
from idl_movie m lateral view ExplodeDirectors(m.director) mytable as col1, col2
where not m.type like '%动画%';




--有导演号召力成员的电影ID
drop table if exists adl_movie_director_charisma;
create table if not exists adl_movie_director_charisma (
recordid string comment '电影ID'
)
comment '有导演号召力成员的电影ID'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_movie_director_charisma SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  adl_movie_director_charisma
 select im.recordid from adl_movie_director_weight im
LEFT outer JOIN idl_director_effect ba
 on im.director = ba.name
 where im.recordid is not null and ba.name is not null group by im.recordid;

--会员导演权重总表
 drop table if exists adl_movie_director_weight_2;
create table if not exists adl_movie_director_weight_2 (
memberid string comment '会员ID'
,recordid string comment '电影ID'
,director string comment '导演'
,weight double comment '权重'
)
comment '会员电影导演序号权重详细表'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_movie_director_weight_2 SET SERDEPROPERTIES('serialization.null.format' = '');

--1 添加订单的导演权重  27891488
 insert into table  adl_movie_director_weight_2
 select
 b.memberid
 ,a.recordid
 ,a.director
 ,a.weight
 from  idl_member_order_detail b LEFT outer JOIN
   adl_movie_director_weight a
on  b.movieid = a.recordid
where b.memberid is not null
and a.recordid is not null
and a.director is not null ;

-- 2 添加喜欢数据 关联导演号召力库的权重
 insert into table  adl_movie_director_weight_2
 select
 temp.memberid
 ,a.recordid
 ,a.director
 ,a.weight
 from
 ( select
 imtb.memberid  memberid
 ,m.recordid recordid
 ,m.director director
 from  idl_member_treasure_behavior imtb
 LEFT outer JOIN
 adl_movie_director_charisma c
 on  imtb.relatedid = c.recordid
 LEFT outer JOIN
 idl_movie m
 on  c.recordid = m.recordid
 where imtb.memberid is not null
 and m.director is not null ) temp
 LEFT outer JOIN
   adl_movie_director_weight a
on  temp.recordid = a.recordid
where temp.memberid is not null and a.recordid is not null and a.director is not null ;

--4 添加0点场或第一天  并且存在导演号召力库权重
 insert into table  adl_movie_director_weight_2
 select
 temp.memberid
 ,a.recordid
 ,a.director
 ,a.weight
 from
( select
 b.memberid  memberid
 ,m.recordid recordid
 ,m.director director
 from
 (
  select memberid ,itemid
    from
  (
    select
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
 adl_movie_director_charisma c
 on  b.itemid = c.recordid
 LEFT outer JOIN
 idl_movie m
 on  c.recordid = m.recordid
 where b.memberid is not null
 and m.director is not null ) temp
LEFT outer JOIN
   adl_movie_director_weight a
on  temp.recordid = a.recordid
where temp.memberid is not null
 and a.recordid is not null
 and a.director is not null ;


--会员导演权重汇总1
--备注：汇总导演权重
 drop table if exists adl_movie_director_weight_3;
create table if not exists adl_movie_director_weight_3 (
memberid string comment '会员ID'
,director string comment '导演'
,weight double comment '权重'
)
comment '会员导演权重汇总'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_movie_director_weight_3 SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  adl_movie_director_weight_3
 select memberid id, director dir ,sum(weight)  cou
  from adl_movie_director_weight_2
 group by memberid,director order by cou desc;



--会员演员权重汇总2
--备注：汇总导演前2名

drop table if exists adl_movie_director_weight_4;
create table if not exists adl_movie_director_weight_4 (
memberid string comment '会员ID'
,director string comment '演员'
,weight double comment '权重'
)
comment '会员导演权重汇总'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_movie_director_weight_4 SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  adl_movie_director_weight_4
select memberid,director,weight
from
(select row_number() over(partition by memberid  order by weight desc) rn,
memberid,director,weight  from adl_movie_director_weight_3 ) a
where rn<=2  order by memberid,weight desc ;

--会员演员权重汇总3
--备注：会员导演前2名 多行转多列
--导演喜好  3309682
drop table if exists adl_movie_director;
create table if not exists adl_movie_director (
memberid string comment '会员ID'
,director1 string comment '一号导演'
,director2 string comment '二号导演'
)
comment '会员导演权重汇总'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_movie_director SET SERDEPROPERTIES('serialization.null.format' = '');

--create temporary function RowToCol as 'com.gewara.bigdata.udf.RowToCol';
insert overwrite table  adl_movie_director
select b.memberid,split(b.directors,',')[0],split(b.directors,',')[1]
from (
 select memberid,max(RowToCol(memberid,director)) directors
  from (
   select memberid,director,weight from adl_movie_director_weight_4 order by memberid,weight desc
  ) a  group by memberid) b ;
