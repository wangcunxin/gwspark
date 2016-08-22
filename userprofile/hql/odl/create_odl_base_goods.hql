drop table if exists odl_base_goods;
create external table if not exists odl_base_goods (
recordid string  comment '记录ID'
,tag string comment '分类'
,relatedid  string comment '分类ID'
,goodsname  string  comment '商品名称'
,unitprice  string comment '单价'
,costprice  string comment '成本价'
,feetype  string comment '业务模式'
,category  string comment '业务模式'
,itemid   string comment '项目ID'
,addtime   string comment '创建时间'
,goodstype   string comment ''
,servicetype   string comment '服务板块'
,fromtime   string comment '开卖时间'
,totime   string comment '结束时间'
,fromvalidtime   string comment '演出开始时间'
,tovalidtime   string comment '演出结束时间'
,period    string comment 'Y固定时间 N 通票'
,spcounterid    string comment '使用数量控制器的ID'
,smalltype    string comment '分类：爆米花 衍生品'
,smallid    string comment '预售批次  活动ID'
,pretype    string comment '预售类型'
,settleid    string comment '结算ID'
) 
comment '预售数据表'
row format delimited fields terminated by '|'
stored as textfile
location '/user/sqoop/goods/'
;

alter table odl_base_goods SET SERDEPROPERTIES('serialization.null.format' = '');

