
#**********************程序说明*********************************#
#*模块: IDL
#*功能: 会员 资源库
#*作者：yfp
#*时间：2014-12-29
#*备注：会员评分,会员性别,会员是否是app用户,会员喜欢,会员积分 ,
#******************************#******************#*************#

--会员详情表  old:11264206 new: 12037548
drop table if exists idl_member_detail;
create table if not exists idl_member_detail (
memberid string comment '会员ID'
,addtime string comment '创建时间'
,fromcity string comment '注册城市'
,invitetype string comment ''
,regfrom string comment '从哪注册:web,gewara'
,source string comment '注册来源:code,Email'
,sex string comment '性别'
,mobilemd5 string comment '手机号MD5'
)
comment '会员详细表'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite table idl_member_detail
select
bm.recordid,
bm.addtime,
bm.fromcity,
bm.invitetype,
bm.regfrom,
bm.source,
case when (bs.sex is null or trim(bs.sex)=='') then '无' else bs.sex  end ,
mobilemd5
from
bdl_member bm  --11264206
left outer join
bdl_sex bs  --8276
on
bm.recordid =bs.userid
and bs.userid is not null
;

--会员领积分详情表 --47305886条数据
drop table if exists idl_member_point;
create table if not exists idl_member_point (
addtime string  comment '创建时间'
,memberid string  comment '会员ID'
,point string  comment '积分'
)
comment '会员积分详情表'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite table idl_member_point
select
memberid,
point,
addtime
from bdl_point
;


--用户app详情 25799123 new: 42869376
drop table if exists idl_member_mobile;
create table if not exists idl_member_mobile (
memberid string comment '会员ID'
,mobiletype string comment '手机型号'
,ostype string comment  '系统类型'
,osversion string comment '系统版本'
,apptype string comment '使用软件类型:电影,运s动'
,addtime string comment '创建时间'
)
comment '用户app详细表'
row format delimited fields terminated by '|'
stored as  textfile;

insert into table idl_member_mobile
select
memberid
,mobiletype
,ostype
,osversion
,apptype
,addtime
from bdl_appsource  --42869376
;

--检查性别数据
select count(1) from idl_member_detail where sex != '无';
