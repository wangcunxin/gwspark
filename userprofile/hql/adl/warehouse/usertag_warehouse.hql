
--#**********************程序说明*********************************#
--#*模块: ADL
--#*功能: 用户标签仓库统计表
--#*作者：yn
--#*时间：2014-09-05
--#*备注：导入数据由tem_table执行
--#***************************************************************#
-- 3453577
drop table if exists adl_usertag_warehouse;
create table if not exists adl_usertag_warehouse (
memberid bigint comment '会员id'
,all_count int  comment '总交易数'
,two_month_count int comment '近两月交易数'
,five_month_count int comment '近五月交易数'
,playtime_day_range_1 int  comment '观影时间按天(6~12)'
,playtime_day_range_2  int  comment '观影时间按天(12~18)'
,playtime_day_range_3 int comment '观影时间按天(18~24)'
,playtime_day_range_4 int  comment '观影时间按天(0~6)'
,playtime_day_range_5 int  comment '观影时间按天(黄金场)'
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
,quantity_single_count int  comment '单身用户次数'
,quantity_couples_count int  comment '情侣用户次数'
,quantity_family_count int  comment '家庭用户次数'
,isgoods_count int  comment '购买卖品次数'
,discount_count int  comment '参与特价活动购票次数'
,citycode int  comment '观影次数最近最多城市'
,city_count int  comment '观影最多城市的次数'
,first_cinemaid bigint  comment '观影第一影院'
,first_cinema_count int  comment '观影第一影院次数'
,second_cinemaid bigint  comment '观影第二影院'
,second_cinema_count int  comment '观影第二影院次数'
,last_movieid bigint comment '最近观影电影id'
,last_playtime string comment '最近观影时间'
,last_citycode int comment '最近观影城市id'
,last_cinemaid bigint comment '最近观影影院id'
,edition_normal_2d int comment '2D次数'
,edition_normal_3d int comment '3D次数'
,edition_jumu int comment '巨幕次数'
,edition_imax int comment 'imax次数'
,edition_4d int comment '4d次数'
,edition_4k int comment '4k次数'
,edition_sound int comment '声效次数'
,audience_feature_first string comment '受众特征一'
,audience_feature_first_count int comment '受众特征一的次数'
,audience_feature_second string comment '受众特征二'
,audience_feature_second_count int comment '受众特征二的次数'
,audience_sex_first string comment '受众性别一'
,audience_sex_first_count int comment '受众性别一的次数'
,audience_sex_second string comment '受众性别二'
,audience_sex_second_count int comment '受众性别二的次数'
,audience_age_first string comment '受众年龄一'
,audience_age_first_count int comment '受众年龄一的次数'
,audience_age_second string comment '受众年龄二'
,audience_age_second_count int comment '受众年龄二的次数'
,regcity string comment '注册城市'
,wala_king string comment '哇啦王权重'
,mobile_type string comment '手机类型'
,is_app string comment 'APP用户'
--,no_consume string comment '未消费'
,presalecount string comment '预售次数'
,director1 string comment '导演1'
,director2 string comment '导演2'
,actor1 string comment '演员1'
,actor2 string comment '演员2'
,actor3 string comment '演员3'
,movietype1 string comment '电影类型1'
,movietype2 string comment '电影类型2'
,sex string comment '会员性别'
,wala_white_list_weight string comment 'wala白名单权重'
,mobilemd5 string comment '手机号MD5'
,fds string comment '分析日期'
)
comment '用户标签交易主题仓库库'
partitioned by (
  ds     string  comment '分析日期'
)
row format delimited fields terminated by '|'
stored as  textfile;

alter table adl_usertag_warehouse SET SERDEPROPERTIES('serialization.null.format' = '');



insert overwrite table  adl_usertag_warehouse  partition  (ds='2015-03-12')
select
att.memberid
,coalesce(att.all_count,0) all_count
,coalesce(attm.two_month_count,0) two_month_count
,coalesce(atfm.five_month_count,0) five_month_count
,atw.playtime_day_range_1
,atw.playtime_day_range_2
,atw.playtime_day_range_3
,atw.playtime_day_range_4
,atg.playtime_day_range_5
,atwft.playtime_week_range_1
,atwft.playtime_week_range_2
,atwft.playtime_week_range_3
,atwh.playtime_is_weekend
,atp.paidtime_range_1
,atp.paidtime_range_2
,atp.paidtime_range_3
,atp.paidtime_range_4
,atp.paidtime_range_5
,atpp.paidtime_palytime_range_0
,atpp.paidtime_palytime_range_1
,atpp.paidtime_palytime_range_2
,atpp.paidtime_palytime_range_3
,atpp.paidtime_palytime_range_4
,atpp.paidtime_palytime_range_5
,atpp.paidtime_palytime_range_6
,atpp.paidtime_palytime_range_7
,atpp.paidtime_palytime_range_8
,atpp.paidtime_palytime_range_9
,atpp.paidtime_palytime_range_10
,atpp.paidtime_palytime_range_11
,atpp.paidtime_palytime_range_12
,atpp.paidtime_palytime_range_24
,atpp.paidtime_palytime_range_48
,atpp.paidtime_palytime_range_49
,agwg.quantity_single_count
,agwg.quantity_couples_count
,agwg.quantity_family_count
,agig.isgoods_count
,agips.discount_count
,coalesce(apwc.citycode,0)  citycode
,coalesce(apwc.city_count,0) city_count
,coalesce(apwmc.cinemaid1,0) first_cinemaid
,coalesce(apwmc.count1,0) first_cinemaid_count
,coalesce(apwmc.cinemaid2,0) second_cinemaid
,coalesce(apwmc.count2,0) second_cinemaid_count
,apry.last_movieid
,apry.last_playtime
,apry.last_citycode
,apry.last_cinemaid
,amge.edition_normal_2d
,amge.edition_normal_3d
,amge.edition_jumu
,amge.edition_imax
,amse.edition_4d
,amse.edition_4k
,amse.edition_sound
,case when (amaf1.audience_feature_first is null or trim(amaf1.audience_feature_first)=='') then '无' else amaf1.audience_feature_first end audience_feature_first
,coalesce(amaf1.audience_feature_first_count,0)  audience_feature_first_count
,case when (amaf2.audience_feature_second is null or trim(amaf2.audience_feature_second)=='') then '无' else amaf2.audience_feature_second end audience_feature_second
,coalesce(amaf2.audience_feature_second_count,0) audience_feature_second_count
,case when (amas1.audience_sex_first is null or trim(amas1.audience_sex_first)=='') then '无' else amas1.audience_sex_first end audience_sex_first
,coalesce(amas1.audience_sex_first_count,0) audience_sex_first_count
,case when (amas2.audience_sex_second is null or trim(amas2.audience_sex_second)=='') then '无' else amas2.audience_sex_second end audience_sex_second
,coalesce(amas2.audience_sex_second_count,0) audience_sex_second_count
,case when (amaa1.audience_age_first is null or trim(amaa1.audience_age_first)=='') then '无' else amaa1.audience_age_first end audience_age_first
,coalesce(amaa1.audience_age_first_count,0) audience_age_first_count
,case when (amaa2.audience_age_second is null or trim(amaa2.audience_age_second)=='') then '无' else amaa2.audience_age_second end audience_age_second
,coalesce(amaa2.audience_age_second_count,0) audience_age_second_count
,apr.regcity
,agiwk.weight wala_king
,agms.systemtype mobile_type
,aui.isapp is_app
--,aun.isconsume no_consume
,aup.presalecount presalecount
,aud.director1 director1
,aud.director2 director2
,aua.actor1 actor1
,aua.actor2 actor2
,aua.actor3 actor3
,aumt.movietype1 movietype1
,aumt.movietype2 movietype2
,imd.sex
,awwl.weight
,imd.mobilemd5
,'2015-03-12'
from adl_trade_total att			--总交易次数
left outer join adl_trade_twomonth attm  --近两月交易次数
on att.memberid = attm.memberid
left outer join adl_place_watchmovie_city apwc  --最常观影城市
on att.memberid = apwc.memberid
left outer join adl_place_recently apry    --用户最近观影相关
on att.memberid = apry.memberid
left outer join adl_trade_fivemonth atfm  --近5月交易次数
on att.memberid = atfm.memberid
left outer join adl_movie_audiencefeature1 amaf1	--电影受众特征1
on att.memberid = amaf1.memberid
left outer join adl_movie_audiencefeature2 amaf2	--电影受众特征2
on att.memberid = amaf2.memberid
left outer join adl_movie_audiencesex1 amas1		--电影受众性别1
on att.memberid = amas1.memberid
left outer join adl_movie_audiencesex2 amas2		--电影受众性别2
on att.memberid = amas2.memberid
left outer join adl_movie_audienceage1 amaa1		--电影受众年龄1
on att.memberid = amaa1.memberid
left outer join adl_movie_audienceage2 amaa2		--电影受众年龄2
on att.memberid = amaa2.memberid
left outer join adl_place_regcity apr
on att.memberid = apr.memberid
left outer join adl_group_iswalaking agiwk	--是否是哇啦王
on att.memberid = agiwk.memberid
left outer join adl_group_mobilesys agms		--用户使用系统类型
on att.memberid = agms.memberid
left outer join adl_group_isapp aui			--是否是app用户
on att.memberid = aui.memberid
left outer join adl_group_presalefan aup	--预售控
on att.memberid = aup.memberid
left outer join adl_movie_director aud		--导演喜好
on att.memberid = aud.memberid
left outer join adl_movie_actor aua			--演员喜好
on att.memberid = aua.memberid
left outer join adl_movie_movietype aumt	--电影类型
on att.memberid = aumt.memberid
left outer join idl_member_detail imd		--用户基本信息
on att.memberid = imd.memberid
left outer join adl_group_wala_white_list awwl	--哇啦白名单
on att.memberid = awwl.memberid
left outer join adl_place_watchmovie_cinema apwmc --最常观影影院
on att.memberid = apwmc.memberid
left outer join	adl_time_withday atw	--观影时间按天
on att.memberid = atw.memberid
left outer join	adl_time_gold atg	--黄金场
on att.memberid = atg.memberid
left outer join	adl_time_withfirstweek atwft	--观影时间按首周
on att.memberid = atwft.memberid
left outer join	adl_time_withweek atwh	--观影时间按周
on att.memberid = atwh.memberid
left outer join	adl_time_paidtime atp	--购票时间类型
on att.memberid = atp.memberid
left outer join	adl_time_paidtime_near_playtime atpp	--放映前购票时段
on att.memberid = atpp.memberid
left outer join	adl_group_watchgroup agwg	--观影群体
on att.memberid = agwg.memberid
left outer join	adl_group_isgoods agig	--购买卖品次数
on att.memberid = agig.memberid
left outer join	adl_group_is_price_sensitive agips	--参与特价活动购票次数
on att.memberid = agips.memberid
left outer join	adl_movie_genera_edition amge	--常规型特效
on att.memberid = amge.memberid
left outer join	adl_movie_spec_edition amse	--常规型特效
on att.memberid = amse.memberid;
