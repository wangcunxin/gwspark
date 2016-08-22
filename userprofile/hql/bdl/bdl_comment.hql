#-*-coding: UTF-8 -*-

#**********************程序说明*********************************#
#*模块: BDL
#*功能: wala基础表
#*作者：jys
#*时间：2014-12-22
#*备注：
#***************************************************************#

#导入相关模块
#***********************模块说明********************************#
#conn_db模块,封装了mysql、hive数据库接口
#***************************************************************#

drop table if exists bdl_comment;
create table if not exists bdl_comment (
recordid string  comment '记录ID'
,memberid string comment '会员id'
,nickname string comment '昵称'
,addtime string  comment '添加时间'
,body_length string comment 'wala长度'
,replycount string comment '回复数量'
,flowernum string comment '点赞数量'
,recommend_top string comment 'wala推荐标示'
,fds       string comment '数据日期'
)
comment 'wala基础数据表'
partitioned by (ds  string  comment '数据日期')
row format delimited fields terminated by '|'
stored as  textfile;

alter table bdl_comment SET SERDEPROPERTIES('serialization.null.format' = '');


insert overwrite table  bdl_comment partition  (ds='$runday')
select 
trim(recordid) recordid
,trim(memberid) memberid
,trim(nickname) nickname
,trim(addtime) addtime
,trim(body_length) body_length
,trim(replycount) replycount
,trim(flowernum) flowernum
,trim(recommend_top) recommend_top
,'$runday' fds
from odl_base_comment where ds='$runday'  ; 