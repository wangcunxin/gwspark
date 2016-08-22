#**********************程序说明*********************************#
#*模块: IDL
#*功能: 用户行为主题 包含3种行为:wala,打分,喜欢
#******************************#******************#*************#
--wala行为  --5865095条  6820551
drop table if exists idl_member_wala_behavior;
create external table if not exists idl_member_wala_behavior (
memberid string comment '会员id',
nickname string comment '昵称',
body_length string comment 'wala长度',
replycount string comment '回复数量',
flowernum string comment '点赞数量',
recommend_top string comment 'wala推荐标示'
)
comment 'wala行为数据'
row format delimited fields terminated by '|'
stored as textfile
;

insert overwrite table idl_member_wala_behavior
select
memberid,
nickname,
body_length,
replycount,
flowernum,
recommend_top
from bdl_comment ; --5865095条数据

--打分行为数据  616051条数据 new :761994
drop table if exists idl_member_mark_behavior;
create external table if not exists idl_member_mark_behavior (
memberid string comment '会员id',
relatedid string comment '评分类型对应数据ID',
markvalue string  comment '评分值'
)
comment '评分数据'
row format delimited fields terminated by '|'
stored as textfile;


insert overwrite table idl_member_mark_behavior
select
memberid,
relatedid,
markvalue
from bdl_membermark  --761994条数据

--喜欢行为数据 685242条数据 new:685242
drop table if exists idl_member_treasure_behavior;
create external table if not exists idl_member_treasure_behavior (
memberid string comment '会员id',
relatedid string  comment '类型对应数据ID'
)
comment '喜欢数据'
row format delimited fields terminated by '|'
stored as textfile;

insert overwrite table idl_member_treasure_behavior
select
memberid,
relatedid
from bdl_treasure --685242条数据