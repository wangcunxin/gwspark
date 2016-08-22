**********************程序说明*********************************#
*功能: 订单主题,分为普通订单和预售订单
***************************************************************#

--包含预售订单的order  合计:13204644
drop table if exists idl_member_order_detail;
create table if not exists idl_member_order_detail (
memberid bigint comment  '会员id'
,tradeno  bigint comment '交易号'
,movieid bigint comment '电影id'
,citycode int comment '城市代码'
,cinemaid   string comment '影院id'
,paidtime   string comment '购票时间'
,playtime   string comment '放映时间'
,quantity   int comment '购买数量'
,discount   int comment '折扣'
,edition string comment '电影特效'
,itemfee  int comment '物品费用'
--,regcity string comment '注册城市'
,moviename string comment '电影名称'
,director string comment '导演'
,actors string comment '主演'
,type string comment '电影类型'
,premieretime string comment '首映时间'
,audiencefeature string comment '受众特征'
,audiencesex string comment '受众性别'
,audienceage string comment '受众年龄'
,relatedid string comment '见面会关联'
,ishalfyear string comment '是否半年内购票'
,isgoods string comment '是否是预售订单'
)
comment '会员订单详情表'
row format delimited fields terminated by '|'
stored as  textfile;

--先插普通订单             13145188条数据  14153464
insert overwrite table  idl_member_order_detail
select *
from (
select
t1.memberid
,t1.tradeno
,t1.itemid movieid
,t1.citycode
,t1.placeid cinemaid
,t1.paidtime
,t1.playtime  playtime
,t1.quantity
,t1.discount
,t1.edition
,t1.itemfee
,t2.moviename name
,t2.director
,t2.actors actors
,t2.type  type
,t2.premieretime
,t2.audiencefeature
,t2.audiencesex
,t2.audienceage
,t1.relatedid
,case when to_date(t1.playtime) > date_sub('2015-01-31',180) then 1 else 0 end
,0
from bdl_trade_ticket as t1
left outer join bdl_movie as t2
on t1.itemid =t2.recordid
where t1.itemid is not null
and t1.itemid <> 'null'
and t1.playtime is not null
and t1.playtime <> 'null'
) temp
where  temp.name is not null and temp.name <> 'null'
and temp.type is not null
and temp.premieretime is not null
and temp.actors is not null and temp.playtime is not null
and temp.playtime <> 'null'
and paidtime is not null

--select count(1) from idl_member_order_detail;