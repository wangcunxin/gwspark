--用户群体
--
--1.1忠实用户  1.4 潜力用户  根据trade中的 "近两月交易数"

--1.2.休眠用户 1.3边缘用户  根据trade中的 "近五月交易数"

--2.观影群体
drop table if exists adl_group_watchgroup;
create table if not exists adl_group_watchgroup (
memberid bigint comment '会员id'
,quantity_single_count int  comment '单身用户次数'
,quantity_couples_count int  comment '情侣用户次数'
,quantity_family_count int  comment '家庭用户次数'
,fds string comment '分析日期'
)
comment '观影群体'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite table adl_group_watchgroup
select
memberid
,sum(case when  quantity = 1 then 1 else 0 end ) as quantity_single_count
,sum(case when  quantity = 2 then 1 else 0 end ) as quantity_couples_count
,sum(case when  quantity >= 3 then 1 else 0 end ) as quantity_family_count
,'2015-01-05'
from idl_member_order_detail
group by memberid;

--3.是否价格敏感
drop table if exists adl_group_is_price_sensitive;
create table if not exists adl_group_is_price_sensitive (
memberid bigint comment '会员id'
,discount_count int  comment '参与特价活动购票次数'
,fds string comment '分析日期'
)
comment '是否价格敏感'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite table adl_group_is_price_sensitive
select
memberid
,sum(case when discount > 0 then 1 else 0 end) as discount_count
,'2015-01-05'
from idl_member_order_detail
group by memberid;

--4.是否卖品用户
drop table if exists adl_group_isgoods;
create table if not exists adl_group_isgoods (
memberid bigint comment '会员id'
,isgoods_count int  comment '购买卖品次数'
,fds string comment '分析日期'
)
comment '是否卖品用户'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite table adl_group_isgoods
select
memberid
,sum(case when  itemfee > 0 then 1 else 0 end ) as isgoods_count
,'2015-01-05'
from idl_member_order_detail
group by memberid;

--5.是否哇啦王

drop table if exists adl_wala_king_weight;
create table if not exists adl_wala_king_weight (
memberid string comment '会员ID'
,weight double comment '权重'
)
comment '会员权重'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_wala_king_weight SET SERDEPROPERTIES('serialization.null.format' = '');


--1 有被编辑推荐，权重加 3 不累加
 insert into table  adl_wala_king_weight
 select distinct memberid,3.0
 from  idl_member_wala_behavior where recommend_top is not null ;

--2 有长哇啦一条 权重加1 累加   >400
insert into table  adl_wala_king_weight
select  memberid ,1.0 from  idl_member_wala_behavior where body_length >400;

--3 有被回复超过10条的哇啦（暂定） 一条加1， 权重加1
insert into table  adl_wala_king_weight
select  memberid ,1.0 from idl_member_wala_behavior where replycount > 10;

--4 哇啦被点赞的数量过10一条加1
insert into table  adl_wala_king_weight
select memberid ,1.0 from  idl_member_wala_behavior where flowernum >10;

--哇啦王 权重汇总
drop table if exists adl_group_iswalaking;
create table if not exists adl_group_iswalaking (
memberid bigint comment '会员id'
,weight double comment '哇啦王权重'
)
comment '哇啦王'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_group_iswalaking SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table adl_group_iswalaking
select memberid,sum(weight)
 from  adl_wala_king_weight where memberid is not null group by memberid ;

--6.安装手机类型
drop table if exists adl_group_mobilesys;
create table if not exists adl_group_mobilesys (
memberid bigint comment '会员id'
,systemtype string comment '系统类型'
,addtime string comment '最后app登录时间'
)
comment '手机系统类型'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_group_mobilesys SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  adl_group_mobilesys
select memberid,ostype,addtime
from
(select row_number() over(partition by memberid  order by addtime desc) rn,
memberid,ostype,addtime  from idl_member_mobile ) a
where rn=1  order by memberid,addtime desc;

--7.APP用户
drop table if exists adl_group_isapp;
create table if not exists adl_group_isapp (
memberid bigint comment '会员id'
,isapp int comment '是否是app用户 1是,0不是'
,fds string comment '分析日期'
)
comment '是否app用户'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_group_isapp SET SERDEPROPERTIES('serialization.null.format' = '');


insert overwrite table  adl_group_isapp
select temp.id memberid
,case when sum(temp.is_app)>0 then '1' else '0' end isapp
,'2015-01-05'
from
(select
 m.memberid id
,case when a.memberid is null then '0' else '1' end is_app
from idl_member_detail m left outer
join idl_member_mobile a on  m.memberid = a.memberid ) temp
group by temp.id;



--9.用户性别  从idl_member主题中取

--10.是否预售控
drop table if exists adl_group_presalefan;
create table if not exists adl_group_presalefan (
memberid bigint comment '会员id'
,presalecount int comment '参与预售次数'
)
comment '预售控'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_group_presalefan SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table adl_group_presalefan
select
memberid,
count(1)
from idl_member_order_detail
where isgoods = 1
group by memberid ;

--11.是否哇啦白名单
--会员 哇啦白名单 权重
drop table if exists adl_wala_white_list_weight;
create table if not exists adl_wala_white_list_weight (
memberid string comment '会员ID'
,weight double comment '权重'
)
comment '会员权重'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_wala_white_list_weight SET SERDEPROPERTIES('serialization.null.format' = '');


-- 1 有购票的用户 权重2
 insert into table  adl_wala_white_list_weight
 select distinct memberid,2.0
 from  idl_member_order_detail ;

--2 有哇啦被赞（喜欢）的用户  权重1
insert into table  adl_wala_white_list_weight
select distinct memberid ,1.0 from  idl_member_wala_behavior where flowernum > 0;

--3 有哇啦获得编辑推荐的用户 权重3
insert into table  adl_wala_white_list_weight
select distinct memberid ,3.0 from  idl_member_wala_behavior where recommend_top is not null;

--4 哇啦被回复超过10条 权重1
insert into table  adl_wala_white_list_weight
select distinct memberid ,1.0 from  idl_member_wala_behavior where replycount >10;

--5 有长哇啦一条 权重加1
insert into table  adl_wala_white_list_weight
select distinct memberid ,1.0 from  idl_member_wala_behavior where body_length >400;

--6 有点击过喜欢按钮的用户 权重2
insert into table  adl_wala_white_list_weight
select distinct memberid ,2.0 from  idl_member_treasure_behavior ;

--7 领过红包的用户    权重0.5
insert into table  adl_wala_white_list_weight
select distinct memberid ,0.5 from  idl_member_point ;

--8 赞过其它用户的哇啦 权重1
--3978379
drop table if exists adl_group_wala_white_list;
create table if not exists adl_group_wala_white_list (
memberid string comment '会员ID'
,weight double comment '权重'
)
comment '会员权重'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_group_wala_white_list SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  adl_group_wala_white_list
 select memberid,sum(weight)
 from  adl_wala_white_list_weight where memberid is not null group by memberid ;


