# -*- coding:utf-8 -*-
from spark.datacenter.etl.hbase_client import HBaseClient
from sklearn.preprocessing import StandardScaler
import numpy as np
from spark.datacenter.etl.mongodb_client import MongodbClient
from userprofile.properties import Properties

__author__ = 'kevin'

sep = ','
sep2 = "_"

if __name__ == '__main__':
    try:
        # 1.load and filter
        hBaseClient = HBaseClient()
        table = "up_dat"
        dat = "201608"
        cfs = ['DF']
        rs = hBaseClient.scanByPrefix(table, dat, cfs)
        qualifiers = "buy_times,buy_quantity,amount,discount_amount,discount_times," \
                     "days,buy_cinemas,buy_cities,avg_time,avg_count".split(",")
        print 'rs:len', rs.__len__()
        lines = []
        for r in rs:
            rowkey = r[0].row.split('#')[1]
            tmp = r[0].columns.get('DF:avg_count')
            avg_count = 0
            if tmp is not None:
                avg_count = tmp.value

            if avg_count == 0 or rowkey == '55859667':
                print 'filter:special users: rowkey=%s,avg_count=%s' % (rowkey, avg_count)
                continue

            arr = []
            arr.append(rowkey)
            columns = r[0].columns
            for qualifier in qualifiers:
                value = '0'
                val = columns.get('DF:%s' % qualifier)
                if val is not None:
                    value = val.value
                arr.append(value)
            lines.append(sep.join(arr))

        print 'lines:len', lines.__len__()

        # 2.scale features
        dataset = np.loadtxt(lines, delimiter=",")
        x1 = dataset[:, 1:len(lines) + 1]
        y1 = dataset[:, 0]
        y2 = map(int, y1)

        scaler = StandardScaler()
        x2 = scaler.fit_transform(x1)

        # 3.rating
        weight = 10
        rating = []
        for j in range(0, len(x2)):
            x = x2[j]
            score = 0
            for i in range(0, len(x)):
                value = x[i]
                if i in (8, 9):
                    if value < -2:
                        score += weight
                else:
                    if value > 2:
                        score += weight
            key = "%s%s%s" % (dat, sep2, y2[j])
            ele = {'_id': key, 'score': score}
            rating.append(ele)

        # 4.dump to mango
        print 'rating:len', rating.__len__()
        conf_file = "../../../userprofile/config-mongodb.properties"
        prop = Properties()
        conf = prop.getProperties(conf_file)
        host = conf.get("bigdata.host")
        port = int(conf.get("bigdata.port"))
        username = conf.get("bigdata.username")
        password = conf.get("bigdata.password")
        dbname = conf.get("bigdata.dbname")

        mongodbClient = MongodbClient(host, port, dbname, username, password)
        colName = "user_score"
        mongodbClient.setCollection(colName)
        col = mongodbClient.insertMany(rating)
    except Exception, e:
        print e
