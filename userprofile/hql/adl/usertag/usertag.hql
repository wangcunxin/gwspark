create temporary function DividedPercent as 'com.gewara.bigdata.udf.DividedPercent';

drop table if exists adl_usertag; --3750298  
create table if not exists adl_usertag (
memberid bigint comment '会员id'
,all_count int  comment '总交易数'
,two_month_count int comment '近两月交易数'
,five_month_count int comment '近五月交易数'
,playtime_day_range_1 int  comment '早场：观影时间按天(6~12)'
,playtime_day_range_2  int  comment '午场：观影时间按天(12~18)'
,playtime_day_range_3 int comment '晚场：观影时间按天(18~24)'
,playtime_day_range_4 int  comment '午夜场：观影时间按天(0~6)'
,playtime_day_range_5 int  comment '黄金场：略'
,playtime_week_range_1 int  comment '首映场'
,playtime_week_range_2 int  comment '上映第一天'
,playtime_week_range_3 int  comment '上映首周末'
,playtime_is_weekend int  comment '周末场'
,paidtime_range_1 int  comment '上下班途中'
,paidtime_range_2 int  comment '睡觉前'
,paidtime_range_3 int  comment '工作中'
,paidtime_range_4 int  comment '周末'
,paidtime_range_5 int  comment '午休'
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
,use_type_faithful int  comment '忠实用户'
,use_type_sleep int  comment '休眠用户'
,use_type_edge  int  comment '边缘用户'
,use_type_potential int  comment '潜力用户'
,quantity_single int  comment '单身用户标签'
,quantity_couples int  comment '情侣用户标签'
,quantity_family int  comment '家庭用户标签'
,isgoods int  comment '购买卖品标签'
,is_price_sensitive int  comment '价格敏感标签'
,citycode int  comment '观影次数最近最多城市标签' 
,first_cinemaid bigint  comment '观影次数第一最多影院标签'
,second_cinemaid bigint  comment '观影次数第二最多影院标签'
,edition_normal_3d int comment '3D标签'
,edition_jumu int comment '巨幕标签'
,edition_imax int comment 'imax标签'
,edition_4d int comment '4d标签'
,edition_4k int comment '4k标签'
,edition_sound int comment '声效标签'
,audience_feature_first string comment '受众特征一'
,audience_feature_second string comment '受众特征二'
,audience_sex string comment '受众性别'
,audience_age string comment '受众年龄'
,regcity int comment '注册城市'
,wala_king int comment '哇啦王'
,mobile_type string comment '手机类型 ' 
,is_app int comment 'APP用户'
,no_consume int comment '是否未消费'
,ispresale int comment '是否预售控'
,director1 string comment '导演1'
,director2 string comment '导演2'
,actor1 string comment '演员1'
,actor2 string comment '演员2'
,actor3 string comment '演员3'
,wala_white_list int comment '是否哇啦白名单'
,movie_type1 string comment '电影类型1'
,movie_type2 string comment '电影类型2'
,sex string comment '会员性别'
,mobile_md5 string comment '手机号MD5'
,fds string comment '分析日期'
)
comment '用户标签库'
partitioned by (
 ds     string  comment '分析日期'
 )
row format delimited fields terminated by '|'
stored as  textfile
location '/user/sqoop/adl_usertag/ds=2015-03-12/'
;

alter table adl_usertag SET SERDEPROPERTIES('serialization.null.format' = '');



insert overwrite table  adl_usertag partition  (ds='2015-03-12')
select 
memberid  
,case when all_count is null then 0 else all_count end all_count
,case when two_month_count is null then 0 else two_month_count end two_month_count
,case when five_month_count is null then 0 else five_month_count end five_month_count
,case when DividedPercent(playtime_day_range_1,all_count,1) >= 80.0 then 1 else 0 end playtime_day_range_1
,case when DividedPercent(playtime_day_range_2,all_count,1) >= 80.0 then 1 else 0 end playtime_day_range_2
,case when DividedPercent(playtime_day_range_3,all_count,1) >= 80.0 then 1 else 0 end playtime_day_range_3
,case when playtime_day_range_4  > 2 then 1 else 0 end playtime_day_range_4
,case when DividedPercent(playtime_day_range_5,all_count,1) >= 80.0 then 1 else 0 end playtime_day_range_5
,case when playtime_week_range_1  > 2 then 1 else 0 end playtime_week_range_1
,case when DividedPercent(playtime_week_range_2,all_count,1) >= 80.0 then 1 else 0 end playtime_week_range_2
,case when DividedPercent(playtime_week_range_3,all_count,1) >= 80.0 then 1 else 0 end playtime_week_range_3 
,case when DividedPercent(playtime_is_weekend,all_count,1) >= 80.0 then 1 else 0 end playtime_is_weekend
,case when DividedPercent(paidtime_range_1,all_count,1) >= 60.0 then 1 else 0 end paidtime_range_1
,case when DividedPercent(paidtime_range_2,all_count,1) >= 60.0 then 1 else 0 end paidtime_range_2
,case when DividedPercent(paidtime_range_3,all_count,1) >= 60.0 then 1 else 0 end paidtime_range_3
,case when DividedPercent(paidtime_range_4,all_count,1) >= 60.0 then 1 else 0 end paidtime_range_4
,case when DividedPercent(paidtime_range_5,all_count,1) >= 60.0 then 1 else 0 end paidtime_range_5
,case when DividedPercent(paidtime_palytime_range_0,all_count,1) >= 80.0 then 1 else 0 end paidtime_palytime_range_0
,case when DividedPercent(paidtime_palytime_range_1,all_count,1) >= 80.0 then 1 else 0 end paidtime_palytime_range_1
,case when DividedPercent(paidtime_palytime_range_2,all_count,1) >= 80.0 then 1 else 0 end paidtime_palytime_range_2
,case when DividedPercent(paidtime_palytime_range_3,all_count,1) >= 80.0 then 1 else 0 end paidtime_palytime_range_3
,case when DividedPercent(paidtime_palytime_range_4,all_count,1) >= 80.0 then 1 else 0 end paidtime_palytime_range_4
,case when DividedPercent(paidtime_palytime_range_5,all_count,1) >= 80.0 then 1 else 0 end paidtime_palytime_range_5
,case when DividedPercent(paidtime_palytime_range_6,all_count,1) >= 80.0 then 1 else 0 end paidtime_palytime_range_6
,case when DividedPercent(paidtime_palytime_range_7,all_count,1) >= 80.0 then 1 else 0 end paidtime_palytime_range_7
,case when DividedPercent(paidtime_palytime_range_8,all_count,1) >= 80.0 then 1 else 0 end paidtime_palytime_range_8
,case when DividedPercent(paidtime_palytime_range_9,all_count,1) >= 80.0 then 1 else 0 end paidtime_palytime_range_9
,case when DividedPercent(paidtime_palytime_range_10,all_count,1) >= 80.0 then 1 else 0 end paidtime_palytime_range_10
,case when DividedPercent(paidtime_palytime_range_11,all_count,1) >= 80.0 then 1 else 0 end paidtime_palytime_range_11
,case when DividedPercent(paidtime_palytime_range_12,all_count,1) >= 80.0 then 1 else 0 end paidtime_palytime_range_12
,case when DividedPercent(paidtime_palytime_range_24,all_count,1) >= 80.0 then 1 else 0 end paidtime_palytime_range_24
,case when DividedPercent(paidtime_palytime_range_48,all_count,1) >= 80.0 then 1 else 0 end paidtime_palytime_range_48  
,case when DividedPercent(paidtime_palytime_range_49,all_count,1) >= 80.0 then 1 else 0 end paidtime_palytime_range_49
,case when (two_month_count > 0 and (all_count - two_month_count) >= 3) then 1 else 0 end  use_type_faithful
,case when (five_month_count =0 and all_count >=3) then 1 else 0 end use_type_sleep
,case when (five_month_count =0 and all_count <=3) then 1 else 0 end use_type_edge
,case when (two_month_count > 0 and (all_count - two_month_count) < 3) then 1 else 0 end use_type_potential
,case when DividedPercent(quantity_single_count,all_count,1) >= 80.0 then 1 else 0 end quantity_single
,case when DividedPercent(quantity_couples_count,all_count,1) >= 80.0 then 1 else 0 end quantity_couples
,case when DividedPercent(quantity_family_count,all_count,1) >= 80.0 then 1 else 0 end quantity_family
,case when DividedPercent(isgoods_count,all_count,1) >= 60.0 then 1 else 0 end isgoods
,case when DividedPercent(discount_count,all_count,1) >= 80.0 then 1 else 0 end is_price_sensitive  
,case when citycode is null then 0 else citycode end ecitycode
,case when first_cinemaid is null then 0 else first_cinemaid end first_cinemaid
,case when second_cinemaid is null then 0 else second_cinemaid end second_cinemaid
,case when DividedPercent(edition_normal_3d,all_count,1) >= 60.0 then 1 else 0 end edition_normal_3d  
,case when edition_jumu  >= 2 then 1 else 0 end edition_jumu
,case when  edition_imax >= 2 then 1 else 0 end edition_imax
,case when  edition_4d >= 2 then 1 else 0 end edition_4d
,case when DividedPercent(edition_4k,all_count,1) >= 60.0 then 1 else 0 end edition_4k
,case when  edition_sound > 2 then 1 else 0 end edition_sound
,case when (audience_feature_first is null or trim(audience_feature_first)=='') then '无' else audience_feature_first end audience_feature_first
,case when (audience_feature_second is null or trim(audience_feature_second)=='') then '无' else audience_feature_second end  audience_feature_second
,case when audience_sex_first =='无' and audience_sex_second=='无'
      then '无'  
      when audience_sex_first <> '无' and audience_sex_second=='无' 
      then audience_sex_first  
      when audience_sex_first =='无' and audience_sex_second <> '无' 
      then audience_sex_second  
      when (audience_sex_first_count > audience_sex_second_count)
      then audience_sex_first  
      else audience_sex_second 
      end audience_sex
,case when audience_age_first_count>audience_age_second_count  then  audience_age_first else '无' end audience_age
,case when regcity is null then 0 else regcity end  regcity
,case when wala_king >3.0  then '1' else '0' end  wala_king 
,case when (mobile_type is null or trim(mobile_type)=='' or trim(mobile_type)=='null' )  then  '无'  else mobile_type end  mobile_type
,case when is_app is null then 0 else is_app end  is_app
,'0'
,case when presalecount > 2 then '1' else '0' end  ispresale
,case when director1 is not null then director1 else '无' end  director1
,case when director2 is not null then director2 else '无' end  director2
,case when actor1 is not null then actor1 else '无' end  actor1
,case when actor2 is not null then actor2 else '无' end  actor2
,case when actor3 is not null then actor3 else '无' end  actor3
,case when wala_white_list_weight > 3.0 then 1 else 0 end  wala_white_list
,case when movietype1 is null or trim(movietype1)=='' or trim(movietype1)=='null' then '无'  else movietype1 end movie_type1
,case when movietype2 is null or trim(movietype2)=='' or trim(movietype2)=='null' then '无'  else movietype2 end movie_type2
,case when sex == '无'  then '无'  else (case when sex==0 then '男' else '女' end) end  sex
,case when mobilemd5 is null or trim(mobilemd5)=='' or trim(mobilemd5)=='null' then '无'  else mobilemd5 end mobilemd5
,'2015-03-12'
from adl_usertag_warehouse where ds='2015-03-12';


--8.未消费用户
drop table if exists adl_group_noconsum_memberid;
create table if not exists adl_group_noconsum_memberid (
memberid bigint comment '未消费会员ID'
)
comment '未消费的用户'
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_group_noconsum_memberid SET SERDEPROPERTIES('serialization.null.format' = '');


insert overwrite table  adl_group_noconsum_memberid
select t.bid from
(
SELECT b.memberid bid , a.memberid aid
FROM idl_member_detail b
left outer join adl_usertag a
on b.memberid = a.memberid
) t
where t.aid is null;

--插入未消费的用户
insert into table adl_usertag  partition  (ds='2015-03-09')
select
memberid
,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
,0,0,0,0,0,0,0,'无','无','无','无','0','0','无','0'
,'1'
,'0','无','无','无','无','无','0','无','无','无','2015-03-09'
from adl_group_noconsum_memberid ;
