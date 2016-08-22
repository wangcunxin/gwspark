drop table if exists bdl_goods;
create  table if not exists bdl_goods (
recordid string  comment '记录ID'
,tag string comment '场馆类型'
,relatedid  string comment '场馆ID'
,goodsname  string  comment '商品名称'
,unitprice  string comment '单价'
,costprice  string comment '成本价'
,feetype  string comment '业务模式'
,category  string comment '业务模式'
,itemid   string comment '项目ID'
,addtime   string comment '创建时间'
,goodstype   string comment '物品类型'
,servicetype   string comment '服务板块 movie,drama,sport,activity'
,fromtime   string comment '开卖时间'
,totime   string comment '结束时间'
,fromvalidtime   string comment '通票入场时间'
,tovalidtime   string comment '通票入场结束时间'
,period    string comment '是否有时段'
,spcounterid    string comment '使用数量控制器的ID'
,smalltype    string comment '分类：爆米花 衍生品'
,smallid    string comment '预售批次  活动ID'
,pretype    string comment '预售类型'
,settleid    string comment '结算ID'
) 
comment '预售数据表'
row format delimited fields terminated by '|'
stored as textfile
;

alter table bdl_goods SET SERDEPROPERTIES('serialization.null.format' = '');


insert overwrite table  bdl_goods 
select 
trim(recordid) recordid
,trim(tag) tag
,trim(relatedid) relatedid
,trim(goodsname) goodsname
,trim(unitprice) unitprice
,trim(costprice) costprice
,trim(feetype) feetype
,trim(category) category
,trim(itemid) itemid
,trim(addtime) addtime
,trim(goodstype) goodstype
,trim(servicetype) servicetype
,trim(fromtime) fromtime
,trim(totime) totime
,trim(fromvalidtime) fromvalidtime
,trim(tovalidtime) tovalidtime
,trim(period) period
,trim(spcounterid) spcounterid
,trim(smalltype) smalltype
,trim(smallid) smallid
,trim(pretype) pretype
,trim(settleid) settleid
from odl_base_goods ; 
################# 后续加条件判断 where pretype='movie' ; 

