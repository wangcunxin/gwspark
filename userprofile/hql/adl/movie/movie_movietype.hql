
--行转列
create temporary function rowtocol as 'com.gewara.bigdata.udf.RowToCol';
--给所有电影添加基本权重
create temporary function addbaseweight as 'com.gewara.bigdata.udf.AddBaseWeight';
--加辅助权重值
create temporary function generalweight as 'com.gewara.bigdata.udf.GeneralWeight';
--匹配明星,导演号召库
create temporary function matchda as 'com.gewara.bigdata.udf.MatchDA';
--获取权重值
create temporary function splittypeweight as 'com.gewara.bigdata.udf.SplitTypeWeight';

--3.影片类型喜好
--会员 电影类型 权重

--表说明:从idl_movie表中,切出
--电影类型表 --
drop table if exists movie_type;
create table if not exists movie_type (
movieid string comment '电影id'
,types array<String> comment '电影类型'
)
comment '电影类型表'
row format delimited fields terminated by '|'
stored as  textfile;

alter table movie_type SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  movie_type
select recordid, split(type,"/") as types  from idl_movie ;


---电影类型权重对应表
drop table if exists movie_type_weight;
create table if not exists movie_type_weight (
movieid string comment '电影id'
,types map<String,Double> comment '类型-权重'
)
comment '电影类型权重对应表'
row format delimited fields terminated by '|'
stored as  textfile;

alter table movie_type_weight SET SERDEPROPERTIES('serialization.null.format' = '');

create temporary function addbaseweight as 'com.gewara.bigdata.udf.AddBaseWeight';
insert overwrite table  movie_type_weight
select movieid,case when( types is null or types[0]=='0') then map('无',0.0) else addbaseweight(types) end
from movie_type ;

--导演,演员表
drop table if exists dic_actors;
create table if not exists dic_actors (
movieid string comment '电影id'
,directors array<String> comment '导演列表'
,actors array<String> comment '演员列表'
)
comment '导演演员表'
row format delimited fields terminated by '|'
stored as  textfile;

alter table dic_actors SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table dic_actors
select recordid,split(director,"/") ,split(actors,"/")  from idl_movie ;

--无导演,演员号召电影列表
--无号召电影表,通用 7162条数据 idl_member_treasure_behavior 685242条
drop table if exists noeffect_movie;
create table if not exists noeffect_movie
(
movieid string comment '电影id'
)
comment '无号召电影表'
row format delimited fields terminated by '|'
stored as  textfile;

alter table noeffect_movie SET SERDEPROPERTIES('serialization.null.format' = '');

--匹配明星,导演号召库
create temporary function matchda as 'com.gewara.bigdata.udf.MatchDA';
insert overwrite table noeffect_movie
select case when(matchda(da.actors,da.directors) < 1 ) then da.movieid else 0 end as noeffectid from dic_actors da ;

--无号召电影表,过滤掉0  有4655 条
drop table if exists noeffect_movie1;
create table if not exists noeffect_movie1
(
movieid string comment '电影id'
)
comment '无号召电影表1'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite table noeffect_movie1
select * from noeffect_movie where movieid != 0 ;

--基础会员电影类型权重表
--字段:memberid,movieid,type_weight

drop table if exists base_member_typeweight;
create table if not exists base_member_typeweight(
memberid string comment '用户id',
movieid string comment '电影id',
type_weight map<string,double> comment'电影对应类型权重'
)
comment '购票用户类型基本权重表'
row format delimited fields terminated by '|'
stored as  textfile;

--从订单表中取出用户看的movieid,和电影类型权重表关联查询,求出用户看的电影和对应的电影的类型权重
insert overwrite table base_member_typeweight
select
imtd.memberid,
mtw.movieid,
mtw.types
from idl_member_order_detail imtd
left outer join
movie_type_weight mtw
on  imtd.movieid = mtw.movieid
where mtw.movieid is not null ;

--表说明:用户点击喜欢,并该电影无任何号召明星和导演 满足该条件的电影列表
--字段:memberid,movieid,type_weight
drop table if exists base_member_treasure_typeweight;
create table if not exists base_member_treasure_typeweight(
memberid string comment '用户id',
movieid string comment '电影id',
type_weight map<string,double> comment'电影对应类型权重'
)
comment '喜欢加权重表'
row format delimited fields terminated by '|'
stored as  textfile;


--加辅助权重值
insert overwrite table base_member_treasure_typeweight
select
t.mbid,
t.rid,
--t.mvid,
--mtw.movieid,
generalweight(mtw.types)
from
(select
imtb.memberid as mbid,
imtb.relatedid as rid
--nm.movieid as mvid
from
idl_member_treasure_behavior imtb  --喜欢表
left outer join
noeffect_movie1 nm --none表
on imtb.relatedid=nm.movieid
where nm.movieid is not null --limit 10
)t
left outer join
movie_type_weight mtw
on t.rid = mtw.movieid
where mtw.movieid is not null ;


--表说明:用户购票观影场次为0点场和第一天的电影,并该电影无任何号召明星和导演
--字段:memberid,movieid,type_weight
--用户,购票时间为0点场的电影列表    1632910
drop table if exists zero_movieid;
create table if not exists zero_movieid(
memberid string comment '用户id',
movieid string comment '电影id'
)
comment '0点场加权重'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite table zero_movieid
select
t.memberid,
t.res from
(
select
memberid,
case when(datediff(playtime,premieretime) = 0 or  playtime <= premieretime)  then movieid else 0 end  as res
from idl_member_order_detail
) t
where res != 0
;
--表说明:用户购票观影场次为0点场和第一天的电影,并该电影无任何号召明星和导演
--字段:  memberid,movieid,type_weight  90195

drop table if exists base_member_zero_typeweight;
create table if not exists base_member_zero_typeweight(
memberid string comment '用户id',
movieid string comment '电影id',
type_weight map<string,double> comment'电影对应类型权重'
)
comment '购票用户类型基本权重表+0点场'
row format delimited fields terminated by '|'
stored as  textfile;

----加辅助权重值
insert overwrite table base_member_zero_typeweight
select
t.mbid,
t.mid,
generalweight(mtw.types)
from
(select
zm.memberid as mbid,
zm.movieid as mid
from
zero_movieid zm  --0点场
left outer join
noeffect_movie1 nm --none表
on zm.movieid=nm.movieid
where nm.movieid is not null
)t
left outer join
movie_type_weight mtw
on t.mid = mtw.movieid
where mtw.movieid is not null
;

insert into table base_member_typeweight  --14161807
select * from   base_member_zero_typeweight --1726827
;
insert into table base_member_typeweight
select * from   base_member_treasure_typeweight  --678031
;

--表说明:从表base_member_typeweight中type_weight字段切割出电影类型对应的权重值.
--字段:memberid,movieid,type_weight
--电影类型权重明细表  13148520
drop table if exists movie_typeweight_detail;
create table if not exists movie_typeweight_detail(
memberid string comment '用户id',
movieid string comment '电影id',
action double comment '动作',
strange double comment '奇幻',
risk double comment '冒险',
disaster double comment '灾难',
offence double comment '犯罪',
story  double comment '剧情',
cliffhang double comment '悬疑',
wuxia double comment '武侠',
history double comment '历史',
3d double comment '3D',
animation double comment '动画',
science  double comment '科幻',
magical double comment '魔幻',
love  double comment '爱情',
gunplay double comment '枪战',
war double comment '战争',
record double comment '纪录',
gz double comment '古装',
panic double comment '惊悚',
family double comment '家庭',
child double comment '儿童',
comedy double comment '喜剧'
)
comment '电影详情'
row format delimited fields terminated by '|'
stored as  textfile;


--获取权重值
create temporary function splittypeweight as 'com.gewara.bigdata.udf.SplitTypeWeight';
insert overwrite  table movie_typeweight_detail
select
t.mbid,
t.mvid,
t.weights[0],
t.weights[1],
t.weights[2],
t.weights[3],
t.weights[4],
t.weights[5],
t.weights[6],
t.weights[7],
t.weights[8],
t.weights[9],
t.weights[10],
t.weights[11],
t.weights[12],
t.weights[13],
t.weights[14],
t.weights[15],
t.weights[16],
t.weights[17],
t.weights[18],
t.weights[19],
t.weights[20],
t.weights[21]
from
(
select memberid mbid,movieid mvid,splittypeweight(type_weight) as weights from base_member_typeweight
) t ;


--表说明:用户看的电影的类型权重  类型与权重一一对应  49175201

drop table if exists member_total_weight;
create table if not exists member_total_weight(
memberid string comment '用户id',
action double comment '动作',
strange double comment '奇幻',
risk double comment '冒险',
disaster double comment '灾难',
offence double comment '犯罪',
story  double comment '剧情',
cliffhang double comment '悬疑',
wuxia double comment '武侠',
history double comment '历史',
3d double comment '3D',
animation double comment '动画',
science  double comment '科幻',
magical double comment '魔幻',
love  double comment '爱情',
gunplay double comment '枪战',
war double comment '战争',
record double comment '纪录',
gz double comment '古装',
panic double comment '惊悚',
family double comment '家庭',
child double comment '儿童',
comedy double comment '喜剧'
)
comment '会员类型权重总表'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite table member_total_weight
select memberid,sum(action) as action,sum(strange) as strange,sum(risk) as risk,sum(disaster) as disaster,sum(offence) as offence,sum(story) as story,sum(cliffhang) as cliffhang,
sum(wuxia) as wuxia,sum(history) as history,sum(3d) as 3d,sum(animation) as animation,sum(science) as science,sum(magical) as magical,sum(love) as love,sum(gunplay) as gunplay,
sum(war) as war,sum(record) as record,sum(gz) as gz,sum(panic) as panic,sum(family) as family,sum(child) as child,sum(comedy) as comedy
from movie_typeweight_detail group by memberid;

--表说明:临时表,用户看的电影,和类型权重最高的2个类型
drop table if exists adl_usertag_movietype1;
create table if not exists adl_usertag_movietype1 (
memberid bigint comment '会员id',
movietype string comment '类型',
type_weight double comment '电影类型'
)
comment '类型'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite  table adl_usertag_movietype1
select
t1.mid,
case when t1.type_weight == 0.0 then '无' else  t1.tname end,
t1.type_weight
from
(select
t.memberid mid ,
t.typename tname,
t.type type_weight,
row_number() over(partition by t.memberid  order by t.type desc) rn
from
(select memberid,'动作' as typename,action  as type from member_total_weight
union all
select memberid,'奇幻' as typename ,strange  as type from member_total_weight
union all
select memberid,'冒险' as typename ,risk  as type from member_total_weight
union all
select memberid,'灾难' as typename ,disaster  as type from member_total_weight
union all
select memberid,'犯罪' as typename ,offence  as type from member_total_weight
union all
select memberid,'剧情' as typename ,story  as type from member_total_weight
union all
select memberid,'悬疑' as typename ,cliffhang  as type from member_total_weight
union all
select memberid,'武侠' as typename ,wuxia  as type from member_total_weight
union all
select memberid,'历史' as typename ,history  as type from member_total_weight
union all
select memberid,'3D' as typename ,3d  as type from member_total_weight
union all
select memberid,'动画' as typename ,animation  as type from member_total_weight
union all
select memberid,'科幻' as typename ,science  as type from member_total_weight
union all
select memberid,'魔幻' as typename ,magical  as type from member_total_weight
union all
select memberid,'爱情' as typename ,love  as type from member_total_weight
union all
select memberid,'枪战' as typename ,gunplay  as type from member_total_weight
union all
select memberid,'战争' as typename ,war  as type from member_total_weight
union all
select memberid,'纪录' as typename ,record  as type from member_total_weight
union all
select memberid,'古装' as typename ,gz  as type from member_total_weight
union all
select memberid,'惊悚' as typename ,panic  as type from member_total_weight
union all
select memberid,'家庭' as typename ,family  as type from member_total_weight
union all
select memberid,'儿童' as typename ,child  as type from member_total_weight
union all
select memberid,'喜剧' as typename ,comedy  as type from member_total_weight
)t 
)t1
where t1.rn<=2  order by t1.mid ,t1.type_weight desc ;

--表说明:最终用户喜欢电影类型,权重最高的2个  3153216
drop table if exists adl_movie_movietype;
create table if not exists adl_movie_movietype (
memberid bigint comment '会员id'
,movietype1 string comment '类型1'
,movietype2 string comment '类型2'
)
comment '类型'
row format delimited fields terminated by '|'
stored as  textfile;

--创建函数
create temporary function RowToCol as 'com.gewara.bigdata.udf.RowToCol';

insert overwrite table  adl_movie_movietype
select b.memberid,split(b.types,',')[0],split(b.types,',')[1]
from
(
select memberid,max(RowToCol(memberid,movietype)) types
from
(
select memberid,movietype ,type_weight from adl_usertag_movietype1 order by memberid,type_weight desc
) a
 group by memberid
) b ;