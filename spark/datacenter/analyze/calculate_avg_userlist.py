# -*- coding:utf-8 -*-

import numpy as np

__author__ = 'kevin'

if __name__ == '__main__':
    '''
    0.avg
    1.make a list
    '''
    sep = ","
    weight = 10
    try:
        path = "/home/kevin/temp/users.csv"
        fis = open(path, "r")
        fin = open(path, "r")
        fos_avg = open("/home/kevin/temp/users-avg.csv", "w")
        fos_rating = open("/home/kevin/temp/users-rating.csv", "w")
        try:
            matrix = np.loadtxt(fis, delimiter=",", skiprows=0)
            # avg column
            avgs = np.mean(matrix, axis=0)

            arr = []
            for i in range(0, len(avgs)):
                avg = round(avgs[i], 2)
                arr.append("%d\t%s\n" % (i, avg))
            print(arr)
            fos_avg.writelines(arr)

            qualifiers = "label,userid," \
                         "buy_times,buy_quantity,amount,discount_amount,discount_times," \
                         "days,buy_cinemas,buy_cities,ip_cities,match_num," \
                         "refund_times,avg_time,avg_count".split(sep)
            rating = []
            for line in fin.readlines():
                row = line.strip().split(sep)
                if len(row) < 3:
                    continue
                score = 0
                for i in range(2, len(row)):
                    if i in (12, 10, 11):
                        continue
                    value = float(row[i])
                    if value > float(avgs[i]):
                        score += weight
                new_line = "%s\t%d\n" % (row[1], score)
                rating.append(new_line)

            fos_rating.writelines(rating)

        finally:
            fis.close()
            fin.close()
            fos_avg.close()
            fos_rating.close()

    except Exception, e:
        print(e)
