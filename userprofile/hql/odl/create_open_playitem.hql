drop  table if exists open_playitem; 
create external table if not exists open_playitem(
recordid string comment '记录id'
,mpid string comment '场次id'
,cinemaid string comment '影院id'
,movieid string comment '电影id'
,citycode string comment '城市id'
,opentype string comment 'opentype'
,playtime string comment '放映时间'
,edition string comment '特效'
,language string comment 'language'
,price string comment 'price'
,costprice string comment 'costprice'
,gewaprice string comment 'gewaprice'
,createuser string comment 'createuser'
,createtime string comment 'createtime'
,delaymin string comment 'delaymin'
,opentime string comment 'opentime'
,openuser string comment 'openuser'
,playopendelay string comment 'playopendelay'
,playcreatedelay string comment 'playcreatedelay'
,isfirst string comment 'isfirst'
,synlasttime string comment 'synlasttime'
,synstatus string comment 'synstatus'
,roomname string comment 'roomname'
,roomid string comment 'roomid'
,realprice string comment 'realprice'
,actualprice string comment 'actualprice'
,totalcost string comment 'totalcost'
,seatnum string comment 'seatnum'
,remark string comment 'remark'
,status string comment 'status'
,otherinfo string comment 'otherinfo'
,settype string comment 'settype'
,locknum string comment 'locknum'
,buyopentime string comment 'buyopentime'
,buyclosetime string comment 'buyclosetime'
)
comment '场次表'
row format delimited fields terminated by '|'
stored as textfile
location '/user/sqoop/playitem'
;
alter table open_playitem SET SERDEPROPERTIES('serialization.null.format' = '');

--取明星见面会的会员id列表
select t2.memberid,t2.relatedid,t1.mpid 
from
(
select mpid from  open_playitem 
) t1
left join odl_trade t2
on t1.mpid=t2.relatedid;


