# -*- coding:utf-8 -*-
import datetime
import time
import sys
import numpy as np

from sklearn.preprocessing import StandardScaler

from spark.datacenter.etl.hbase_client import HBaseClient
from spark.datacenter.etl.mongodb_client import MongodbClient
from userprofile.properties import Properties

__author__ = 'kevin'

sep = ','
sep2 = "_"


def main(argv):
    try:
        # 1.load and filter
        hBaseClient = HBaseClient()
        table = "up_dat"
        dat = argv[0]
        cfs = ['DF']
        rs = hBaseClient.scanByPrefix(table, dat, cfs)
        qualifiers = "buy_times,buy_quantity,amount,discount_amount,discount_times," \
                     "days,buy_cinemas,buy_cities,avg_time,avg_count".split(",")

        lines = []
        regex = r"[/.]"
        import re
        for r in rs:
            rowkey = r.row.split('#')[1]
            match = re.search(regex, rowkey)
            if match:
                continue
            arr = [rowkey]
            columns = r.columns
            for qualifier in qualifiers:
                value = '0'
                val = columns.get('DF:%s' % qualifier)
                if val is not None:
                    value = val.value
                arr.append(value)
            lines.append(sep.join(arr))

        print 'load lines:len', len(lines)

        # 2.scale features
        if len(lines) == 0:
            return
        dataset = np.loadtxt(lines, delimiter=sep)
        x1 = dataset[:, 1:len(lines) + 1]
        y1 = dataset[:, 0]

        scaler = StandardScaler()
        x2 = scaler.fit_transform(x1)
        y2 = map(int, y1)

        # 3.rating
        weight = 10
        rating = []
        for j in range(0, len(x2)):
            x = x2[j]
            score = 0
            userid = str(y2[j])
            avg_count = x[9]
            if avg_count > 0 and userid not in ('50000125', '50000949', '50000891', '55859667'):
                # print 'filter:special users: userid=%s,avg_count=%s' % (userid, avg_count)
                for i in range(0, len(x)):
                    value = x[i]
                    if i in (8, 9):
                        if value < -2:
                            score += weight
                    else:
                        if value > 2:
                            score += weight
            key = "%s%s%s" % (dat, sep2, userid)
            ele = {'_id': key, 'userid': userid, 'score': score}
            rating.append(ele)

        # 4.dump to mango
        print 'rate rating:', len(rating)
        conf_file = "../../../userprofile/config-mongodb.properties"
        prop = Properties()
        conf = prop.getProperties(conf_file)
        host = conf.get("bigdata.host")
        port = int(conf.get("bigdata.port"))
        username = conf.get("bigdata.username")
        password = conf.get("bigdata.password")
        dbname = conf.get("bigdata.dbname")

        mongodbClient = MongodbClient(host, port, dbname, username, password)
        colName = "rc_user_rating"
        mongodbClient.setCollection(colName)
        mongodbClient.insertMany(rating)
        print 'dump finish'

    except Exception, e:
        print 'exception happened:', e


if __name__ == '__main__':
    begin = time.time()
    if len(sys.argv) != 2:
        print 'user_rating.py <ym>'
        sys.exit(-1)
    print sys.argv
    main(sys.argv[1:])
    end = time.time()
    now = datetime.datetime.now()
    dat = now.strftime("%Y-%m-%d %H:%M:%S")
    print dat, 'total cost', round((end - begin) / 60, 3), 'minutes'
