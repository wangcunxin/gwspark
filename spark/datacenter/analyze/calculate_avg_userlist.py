# -*- coding:utf-8 -*-

import numpy as np

__author__ = 'kevin'

sep = ","


def prepare():
    try:
        path = "/home/kevin/temp/users.csv"
        pre_path = "/home/kevin/temp/users-pre.csv"
        fin = open(path, "r")
        fos = open(pre_path, "w")
        try:
            lines = []
            for line in fin.readlines():
                row = line.strip().split(sep)
                # label=1 avg_count>0
                if float(row[0]) == 0 or float(row[14]) == 0:
                    continue
                lines.append(line)
            fos.writelines(lines)
        finally:
            fin.close()
            fos.close()
    except Exception, e:
        print(e)


def make_list():
    """
    0.avg
    1.make a list
    """
    weight = 10
    try:
        path = "/home/kevin/temp/users.csv"
        pre_path = "/home/kevin/temp/users-pre.csv"
        fis = open(pre_path, "r")
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


def prepare2():
    try:
        path = "/home/kevin/temp/users.csv"
        pre_path = "/home/kevin/temp/users-pre2.csv"
        fis = open(path, "r")
        fos = open(pre_path, "w")
        try:
            lines = []
            for line in fis.readlines():
                row = line.strip().split(sep)
                # buy_times=0 avg_count=0 ->45w
                if float(row[2]) == 0 or float(row[14]) == 0 or row[1] == '55859667':
                    continue
                lines.append(line)
            fos.writelines(lines)
        finally:
            fis.close()
            fos.close()
    except Exception, e:
        print(e)


def prepare3():
    try:
        path = "/home/kevin/temp/users-pre2.csv"
        pre_path = "/home/kevin/temp/users-pre3.csv"
        fis = open(path, "r")
        fis2 = open(path, "r")
        fos = open(pre_path, "w")
        import numpy as np
        dataset = np.loadtxt(fis, delimiter=",")
        qualifiers = "label,userid," \
                     "buy_times,buy_quantity,amount,discount_amount,discount_times," \
                     "days,buy_cinemas,buy_cities,ip_cities,match_num," \
                     "refund_times,avg_time,avg_count".split(sep)
        X = dataset[:, 2:15]
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        x = scaler.fit_transform(X)
        try:
            lines = []
            i = 0
            for line in fis2.readlines():
                s = ','.join(str(i) for i in x[i])
                row = line.strip().split(sep)
                new_line = "%s,%s,%s\n" % (row[0], row[1], s)
                lines.append(new_line)
                i += 1
            fos.writelines(lines)
        finally:
            fis.close()
            fis2.close()
            fos.close()
    except Exception, e:
        print(e)


def make_list2():
    weight = 10
    try:
        pre_path = "/home/kevin/temp/users-pre3.csv"
        fis = open(pre_path, "r")
        fos_rating = open("/home/kevin/temp/users-rating2.csv", "w")
        try:

            rating = []
            for line in fis.readlines():
                row = line.strip().split(sep)

                score = 0
                for i in range(2, len(row)):
                    if i in (12, 10, 11):
                        continue
                    value = float(row[i])
                    if i in (13, 14):
                        if value < -2:
                            score += weight
                    else:
                        if value > 2:
                            score += weight

                new_line = "%s\t%d\n" % (row[1], score)
                rating.append(new_line)

            fos_rating.writelines(rating)

        finally:
            fis.close()
            fos_rating.close()

    except Exception, e:
        print(e)


if __name__ == '__main__':
    # 1
    # prepare()
    # make_list()

    # 2
    # prepare2()
    # prepare3()
    make_list2()
    pass
