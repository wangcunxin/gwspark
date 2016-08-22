#**********************程序说明*********************************#
#*功能: 影片库主题,以及相关一些movie信息表
#***************************************************************#

--影片库主题  7162
drop table if exists idl_movie;
create table if not exists idl_movie (
recordid string comment '记录名称'
,moviename string comment '电影名称'
,director string comment '导演'
,actors string comment '主演'
,type string comment '电影类型'
,premieretime string comment '放映时间'
,audiencefeature string comment '受众特征'
,audiencesex string comment '受众性别'
,audienceage string comment '受众年龄'
)
comment '电影库表'
row format delimited fields terminated by '|'
stored as  textfile;

alter table idl_movie SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  idl_movie
select * from bdl_movie

#**********************程序说明*********************************#
#*模块: IDL-movie主题
#*功能: 演员影响力号召库
#***************************************************************#
            758
drop table if exists idl_actor_effect;
create table if not exists idl_actor_effect (
name string  comment '名称'
)
comment '演员号召库'
row format delimited fields terminated by '|'
stored as  textfile;

alter table bdl_actor SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  idl_actor_effect
select * from bdl_charisma_actor;


#**********************程序说明*********************************#
#*模块: IDL-movie主题
#*功能: 导演影响力号召库
#***************************************************************#
373
drop table if exists idl_director_effect;
create table if not exists idl_director_effect (
name string  comment '名称'
)
comment '导演号召库'
row format delimited fields terminated by '|'
stored as  textfile;

alter table bdl_director SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  idl_director_effect
select * from bdl_charisma_director;