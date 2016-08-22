#-*-coding: UTF-8 -*-

#**********************程序说明*********************************#
#*模块: BDL
#*功能: trade基础表
#*作者：yn
#*时间：2014-09-05
#*备注：
#***************************************************************#

#导入相关模块
#***********************模块说明********************************#
#conn_db模块,封装了mysql、hive数据库接口
#***************************************************************#

--预售订单  716395 条数据
drop table if exists bdl_goods_trade;
create table if not exists bdl_goods_trade (
tradeno string comment '记录id'
,memberid string comment '会员id'
,itemid string comment '电影id'
,paidtime string comment '购票时间'
,playtime string comment '放映时间'
,citycode string comment '城市代码'
,placeid string comment '影院id'
,quantity string comment '购票数量'
,discount string comment '折扣'
,edition string comment '电影特效'
,itemfee string comment '卖品费用'
,relatedid string comment '见面会关联'
) 
comment '交易电影表'
row format delimited fields terminated by '|'
stored as  textfile;

alter table bdl_goods_trade SET SERDEPROPERTIES('serialization.null.format' = '');

insert overwrite table  bdl_goods_trade
select 
trim(tradeno) tradeno
,trim(memberid) tradeno
,trim(itemid) itemid
,trim(paidtime) paidtime
,trim(playtime) playtime
,trim(citycode) citycode
,trim(placeid) placeid
,trim(quantity) quantity
,trim(discount) discount
,trim(edition) edition
,trim(itemfee) itemfee
,trim(relatedid) relatedid
from odl_goods_trade  ;