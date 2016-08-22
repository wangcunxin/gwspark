--用户交易相关的表
--1.总交易数  3164897  3467608
drop table if exists adl_trade_total;
create table if not exists adl_trade_total (
memberid bigint comment '会员id'
,all_count int  comment '总交易数'
,fds string comment '分析日期'
)
comment '总交易数'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite table  adl_trade_total
select memberid,count(1) as all_count,'2015-02-09'
from idl_member_order_detail
group by memberid;


--2.近两月交易数  1025704 new:1456804
drop table if exists adl_trade_twomonth;
create table if not exists adl_trade_twomonth (
memberid bigint comment '会员id'
,two_month_count int comment '近两月交易数'
,fds string comment '分析日期'
)
comment '近两月交易数'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite table  adl_trade_twomonth
select memberid,count(1) as two_month_count,'2014-09-22'
from idl_member_order_detail
where to_date(playtime) > date_sub('2015-01-31',60)
group by memberid;

--3.近五月交易数  1649234 2008788
drop table if exists adl_trade_fivemonth;
create table if not exists adl_trade_fivemonth (
memberid bigint comment '会员id'
,five_month_count int comment '近五月交易数'
,fds string comment '分析日期'
)
comment '近五月交易数'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite table  adl_trade_fivemonth
select memberid,count(1) as five_month_count,'2014-09-24'
from idl_member_order_detail
where to_date(playtime) > date_sub('2015-01-31',150)
group by memberid;
