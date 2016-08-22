--观影时间


--1.观影时间按天  3164897条数据   3467608
drop table if exists adl_time_withday;
create table if not exists adl_time_withday (
memberid bigint comment '会员id'
,playtime_day_range_1 int  comment '观影时间按天(6~12)'
,playtime_day_range_2  int  comment '观影时间按天(12~18)'
,playtime_day_range_3 int comment '观影时间按天(18~24)'
,playtime_day_range_4 int  comment '观影时间按天(0~6)'
,fds string comment '分析日期'
)
comment '观影时间按天'
row format delimited fields terminated by '|'
stored as  textfile;


insert overwrite table  adl_time_withday
select memberid
,sum(case when (hour(playtime) >=6  and  hour(playtime) < 12)  then 1 else 0 end ) as playtime_day_range_1
,sum(case when (hour(playtime) >=12 and  hour(playtime) < 18)  then 1 else 0 end ) as playtime_day_range_2
,sum(case when (hour(playtime) >=18 and  hour(playtime) < 24)  then 1 else 0 end ) as playtime_day_range_3
,sum(case when (hour(playtime) >=0  and  hour(playtime) < 6)   then 1 else 0 end ) as playtime_day_range_4
,'2015-02-11'
from idl_member_order_detail
group by memberid;

--2.观影时间按首周  3164897条数据
drop table if exists adl_time_withfirstweek;
create table if not exists adl_time_withfirstweek (
memberid bigint comment '会员id'
,playtime_week_range_1 int  comment '首映场'
,playtime_week_range_2 int  comment '上映第一天'
,playtime_week_range_3 int  comment '上映首周末'
,fds string comment '分析日期'
)
comment '观影时间按首周'
row format delimited fields terminated by '|'
stored as  textfile;


insert overwrite table  adl_time_withfirstweek
select memberid
,sum(case when (datediff(playtime,premieretime) =0 and hour(playtime)=0)   then 1 else 0 end ) as playtime_week_range_1
,sum(case when (datediff(playtime,premieretime) =0 and hour(playtime)>0)   then 1 else 0 end ) as playtime_week_range_2
,sum(case when (datediff(playtime,premieretime) <7 and DayOfWeek(playtime) in (6,0)) then 1 else 0 end ) as playtime_week_range_3
,'2015-02-11'
from idl_member_order_detail
group by memberid;


--3.观影时间按周 3164897条数据
drop table if exists adl_time_withweek;
create table if not exists adl_time_withweek (
memberid bigint comment '会员id'
,playtime_is_weekend int  comment '周末场'
,fds string comment '分析日期'
)
comment '观影时间按周'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite table  adl_time_withweek
select memberid
,sum(case when  DayOfWeek(playtime) in (6,0) then 1 else 0 end) as playtime_is_weekend
,'2015-02-11'
from idl_member_order_detail
group by memberid;

--4.黄金场
drop table if exists adl_time_gold;
create table if not exists adl_time_gold (
memberid bigint comment '会员id'
,playtime_day_range_5 int  comment '黄金场:观影时间按天(0~6)'
,fds string comment '分析日期'
)
comment '黄金场'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite table adl_time_gold
select
memberid
,sum(case when ((DayOfWeek(paidtime) in (1,2,3,4,5) and (hour(playtime) >=18  and  hour(playtime)<=21)) or (DayOfWeek(paidtime) in (6,0))) then 1 else 0 end )as playtime_day_range_5
,'2015-02-11'
from idl_member_order_detail
group by memberid;

--5.购票时间类型
drop table if exists adl_time_paidtime;
create table if not exists adl_time_paidtime (
memberid bigint comment '会员id'
,paidtime_range_1 int  comment '上下班途中'
,paidtime_range_2 int  comment '睡觉前'
,paidtime_range_3 int  comment '工作中'
,paidtime_range_4 int  comment '周末'
,paidtime_range_5 int  comment '午休'
,fds string comment '分析日期'
)
comment '购票时间类型'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite table adl_time_paidtime
select
memberid
,sum(case when  DayOfWeek(paidtime) in (1,2,3,4,5) and ((hour(paidtime) >=6 and hour(paidtime) <9) or (hour(paidtime) >= 17 and hour(paidtime) < 20)) then 1 else 0 end) as paidtime_range_1
,sum(case when  DayOfWeek(paidtime) in (1,2,3,4,5) and (hour(paidtime) >= 21 and hour(paidtime) <=23)  then 1 else 0 end) as paidtime_range_2
,sum(case when  DayOfWeek(paidtime) in (1,2,3,4,5) and ((hour(paidtime) >= 10 and hour(paidtime) < 12) or (hour(paidtime) >= 14 and hour(paidtime) <17)) then 1 else 0 end) as paidtime_range_3
,sum(case when  DayOfWeek(paidtime) in (6,0)  then 1 else 0 end) as paidtime_range_4
,sum(case when  DayOfWeek(paidtime) in (1,2,3,4,5) and (hour(paidtime) >= 12 and hour(paidtime) <13) then 1 else 0 end) as paidtime_range_5
,'2015-02-11'
from idl_member_order_detail
group by memberid;

--6.放映前购票时段
drop table if exists adl_time_paidtime_near_playtime;
create table if not exists adl_time_paidtime_near_playtime (
memberid bigint comment '会员id'
,paidtime_palytime_range_0 int  comment '购票时间距离放映时间30分钟'
,paidtime_palytime_range_1 int  comment '购票时间距离放映时间1小时'
,paidtime_palytime_range_2 int  comment '购票时间距离放映时间2小时'
,paidtime_palytime_range_3 int  comment '购票时间距离放映时间3小时'
,paidtime_palytime_range_4 int  comment '购票时间距离放映时间4小时'
,paidtime_palytime_range_5 int  comment '购票时间距离放映时间5小时'
,paidtime_palytime_range_6 int  comment '购票时间距离放映时间6小时'
,paidtime_palytime_range_7 int  comment '购票时间距离放映时间7小时'
,paidtime_palytime_range_8 int  comment '购票时间距离放映时间8小时'
,paidtime_palytime_range_9 int  comment '购票时间距离放映时间9小时'
,paidtime_palytime_range_10 int  comment '购票时间距离放映时间10小时'
,paidtime_palytime_range_11 int  comment '购票时间距离放映时间11小时'
,paidtime_palytime_range_12 int  comment '购票时间距离放映时间12小时'
,paidtime_palytime_range_24 int  comment '购票时间距离放映时间24小时'
,paidtime_palytime_range_48 int  comment '购票时间距离放映时间48小时'
,paidtime_palytime_range_49 int  comment '购票时间距离放映时间48小时以上'
,fds string comment '分析日期'
)
comment '放映前购票时段'
row format delimited fields terminated by '|'
stored as  textfile;

insert overwrite table adl_time_paidtime_near_playtime
select
memberid
,sum(case when (minutediff(paidtime,playtime)<=30) then 1 else 0 end) as paidtime_palytime_range_0
,sum(case when (hourdiff(paidtime,playtime) = 1 and minutediff(paidtime,playtime)>30) then 1 else 0 end) as paidtime_palytime_range_1
,sum(case when hourdiff(paidtime,playtime) = 2 then 1 else 0 end) as paidtime_palytime_range_2
,sum(case when hourdiff(paidtime,playtime) = 3 then 1 else 0 end) as paidtime_palytime_range_3
,sum(case when hourdiff(paidtime,playtime) = 4 then 1 else 0 end) as paidtime_palytime_range_4
,sum(case when hourdiff(paidtime,playtime) = 5 then 1 else 0 end) as paidtime_palytime_range_5
,sum(case when hourdiff(paidtime,playtime) = 6 then 1 else 0 end) as paidtime_palytime_range_6
,sum(case when hourdiff(paidtime,playtime) = 7 then 1 else 0 end) as paidtime_palytime_range_7
,sum(case when hourdiff(paidtime,playtime) = 8 then 1 else 0 end) as paidtime_palytime_range_8
,sum(case when hourdiff(paidtime,playtime) = 9 then 1 else 0 end) as paidtime_palytime_range_9
,sum(case when hourdiff(paidtime,playtime) = 10 then 1 else 0 end) as paidtime_palytime_range_10
,sum(case when hourdiff(paidtime,playtime) = 11 then 1 else 0 end) as paidtime_palytime_range_11
,sum(case when hourdiff(paidtime,playtime) = 12 then 1 else 0 end) as paidtime_palytime_range_12
,sum(case when hourdiff(paidtime,playtime) > 12 and hourdiff(paidtime,playtime) <= 24 then 1 else 0 end) as paidtime_palytime_range_24
,sum(case when hourdiff(paidtime,playtime) > 24 and hourdiff(paidtime,playtime) <= 48 then 1 else 0 end) as paidtime_palytime_range_48
,sum(case when hourdiff(paidtime,playtime) > 48 then 1 else 0 end) as paidtime_palytime_range_49
,'2015-02-11'
from idl_member_order_detail
group by memberid;

